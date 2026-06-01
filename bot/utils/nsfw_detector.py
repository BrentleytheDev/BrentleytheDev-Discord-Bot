import os
import tempfile
import discord
import re
import aiohttp
import io
import imagehash
import cv2
import hashlib
from html.parser import HTMLParser
from urllib.parse import urljoin

from nudenet import NudeDetector
from utils.log import send_log
from PIL import Image
from transformers import pipeline

detector = NudeDetector()

URL_REGEX = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
PROCESSED_MESSAGE_IDS = set()
PROCESSED_IMAGE_DIGESTS = set()
NSFW_IMAGE_HASHES = set()

MAX_DOWNLOAD_BYTES = 50 * 1024 * 1024
VIDEO_FRAME_COUNT = 12
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")
VIDEO_EXTENSIONS = (".mp4", ".mov", ".webm", ".m4v")
PREVIEW_META_NAMES = {
    "og:image",
    "og:video",
    "twitter:image",
    "twitter:player:stream"
}

class PreviewMetaParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "meta":
            return

        values = dict(attrs)
        name = values.get("property") or values.get("name")
        content = values.get("content")

        if name and content and name.lower() in PREVIEW_META_NAMES:
            self.urls.append(content)

anime_nsfw_classifier = pipeline(
    "image-classification",
    model="prithivMLmods/Mature-Content-Detection"
)

def is_anime_nsfw(image_path: str) -> bool:
    results = anime_nsfw_classifier(image_path)

    for result in results:
        label = result["label"].lower().strip()
        score = result["score"]

        if label == "hentai" and score >= 0.45:
            return True 

        if label == "pornography" and score >= 0.60:
            return True 

        if label == "enticing or sensual" and score >= 0.80:
            return True 

    return False

def clear_message_cache(message_id: int):
    PROCESSED_MESSAGE_IDS.discard(message_id)

def get_image_hash(data: bytes)-> str:

    img = Image.open(io.BytesIO(data)).convert("RGB")
    return str(imagehash.phash(img))

def get_image_digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def extract_gif_frames(data: bytes, max_frames: int = 20):
    img = Image.open(io.BytesIO(data))

    frames = []
    i = 0

    try:
        while i < max_frames:
            img.seek(i)

            frame = img.convert("RGB")

            buf = io.BytesIO()
            frame.save(buf, format="JPEG")

            frames.append(buf.getvalue())
            i += 1

    except Exception:
        pass 

    return frames

def extract_video_frames(data: bytes, max_frames: int = VIDEO_FRAME_COUNT):
    video = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    video.write(data)
    video.close()

    frames = []

    try:
        cap = cv2.VideoCapture(video.name)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        if total_frames <= 0:
            return frames

        step = max(total_frames // max_frames, 1)
        frame_index = 0

        while len(frames) < max_frames and frame_index < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, frame_index)
            success, frame = cap.read()

            if success:
                success, buf = cv2.imencode(".jpg", frame)

                if success:
                    frames.append(buf.tobytes())

            frame_index += step

    finally:
        if "cap" in locals():
            cap.release()

        if os.path.exists(video.name):
            os.remove(video.name)

    return frames

def extract_preview_urls(html: str):
    parser = PreviewMetaParser()
    parser.feed(html)

    return [
        url.strip()
        for url in parser.urls
    ]

def is_nsfw(results) -> bool:
    NSFW_KEYWORDS = [
        "breast",
        "genital",
        "anus",
        "buttock",
        "penis",
        "vagina"
    ]

    strong_hits = 0
    max_score = 0.0

    for result in results:
        label = result["class"].lower()
        score = result["score"]

        max_score = max(max_score, score)

        if score >= 0.55 and any(
            keyword in label
            for keyword in NSFW_KEYWORDS
        ):
          strong_hits += 1

    return strong_hits >= 1 or max_score >= 0.70

async def download_url(session, url: str):
    async with session.get(url, timeout=10) as resp:
        if resp.status != 200:
            return None, None

        content_length = resp.headers.get("Content-Length")

        if content_length and int(content_length) > MAX_DOWNLOAD_BYTES:
            print(f"Skipping large media: {url}")
            return None, None

        data = await resp.read()

        if len(data) > MAX_DOWNLOAD_BYTES:
            print(f"Skipping large media: {url}")
            return None, None

        content_type = resp.headers.get("Content-Type", "").lower().split(";")[0]

        return data, content_type

async def resolve_target_media(session, url: str):
    data, content_type = await download_url(session, url)

    if not data:
        return []

    clean_url = url.lower().split("?")[0]

    if content_type.startswith("image/") or clean_url.endswith(IMAGE_EXTENSIONS):
        return [(url, data, content_type)]

    if content_type.startswith("video/") or clean_url.endswith(VIDEO_EXTENSIONS):
        return [(url, data, content_type)]

    if "html" in content_type:
        html = data.decode("utf-8", errors="ignore")
        media = []

        for preview_url in extract_preview_urls(html):
            preview_url = urljoin(url, preview_url)
            preview_data, preview_type = await download_url(session, preview_url)
            clean_preview_url = preview_url.lower().split("?")[0]

            if preview_data and (
                preview_type.startswith("image/")
                or preview_type.startswith("video/")
                or clean_preview_url.endswith(IMAGE_EXTENSIONS)
                or clean_preview_url.endswith(VIDEO_EXTENSIONS)
            ):
                media.append((preview_url, preview_data, preview_type))

        return media

    return []

async def remove_nsfw_message(message: discord.Message, source_type: str):
    embed = discord.Embed(
        title="🔞 Adult Content Detected",
        color=discord.Color.red()
    )

    embed.add_field(
        name="User",
        value=message.author.mention,
        inline=False
    )

    embed.add_field(
        name="Source",
        value=source_type,
        inline=False
    )

    embed.add_field(
        name="Message",
        value=f"[Jump]({message.jump_url})",
        inline=False
    )

    await send_log(
        message.guild,
        "adult-content-logging",
        embed
    )

    await message.delete()

    try:
        await message.author.send(
            "Your content was removed due to NSFW detection."
        )
    except discord.Forbidden:
        pass

async def scan_frame(frame: bytes):
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=".jpg")
    temp.write(frame)
    temp.close()

    try:
        results = detector.detect(temp.name)
        print(f"Scanning: {temp.name}")
        print(f"Results: {results}")

        return is_nsfw(results) or is_anime_nsfw(temp.name)

    finally:
        if os.path.exists(temp.name):
            os.remove(temp.name)

async def nsfw_detect(message: discord.Message) -> bool:
    print(f"NSFW scan triggered for message {message.id}")

    if message.author.bot:
        return False 

    if message.id in PROCESSED_MESSAGE_IDS:
        return False

    PROCESSED_MESSAGE_IDS.add(message.id)

    targets = []

    for a in message.attachments:
        targets.append(("attachment", a.url))

    for url in URL_REGEX.findall(message.content or ""):
        targets.append(("url", url.rstrip(".,!?)]}")))

    print(f"Targets found: {targets}")

    if not targets:
        return False

    async with aiohttp.ClientSession() as session:

        for source_type, url in targets:

            try:
                media_items = await resolve_target_media(session, url)

                for media_url, data, content_type in media_items:
                    frames = []
                    clean_media_url = media_url.lower().split("?")[0]

                    if content_type == "image/gif" or clean_media_url.endswith(".gif"):
                        frames = extract_gif_frames(data)
                    elif content_type.startswith("video/") or clean_media_url.endswith(VIDEO_EXTENSIONS):
                        frames = extract_video_frames(data)
                    else:
                        frames = [data]

                    for frame in frames:
                        img_hash = get_image_hash(frame)

                        if img_hash in NSFW_IMAGE_HASHES:
                            await remove_nsfw_message(message, source_type)
                            return True

                        img_digest = get_image_digest(frame)

                        if img_digest in PROCESSED_IMAGE_DIGESTS:
                            continue

                        PROCESSED_IMAGE_DIGESTS.add(img_digest)

                        if await scan_frame(frame):
                            NSFW_IMAGE_HASHES.add(img_hash)
                            await remove_nsfw_message(message, source_type)
                            return True

            except Exception as e:
                print(f"NSFW Pipeline error: {e}")

    return False
