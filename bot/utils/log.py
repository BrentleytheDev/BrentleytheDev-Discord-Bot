import discord 
import json 
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "automod" / "config.json"

async def setup_logging(key: str, channel_id: int):
    with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)
                
            if "logging" not in data:
                data["logging"] = {}
            
            data["logging"][key] = channel_id

            with CONFIG_PATH.open("w", encoding="utf-8") as f:
                json.dump(data, f, indent=2)

async def send_log(
    guild: discord.Guild,
    log_type: str,
    embed: discord.Embed
):

    try:
        with CONFIG_PATH.open("r", encoding="utf-8") as f:
            data = json.load(f)

    except (FileNotFoundError, json.JSONDecodeError):
        return 

    logging_data = data.get("logging", {})

    print(logging_data)

    channel_id = logging_data.get(log_type)

    print(f"channel_id = {channel_id}")

    if not channel_id:
        channel_id = logging_data.get("general-server-logging")

    if not channel_id:
        print("No logging channel found")
        return 

    #Get Discord channel
    channel = guild.get_channel(channel_id)

    if not channel:
        print("Channel object not found")
        return 

    print("Sending embed")

    await channel.send(embed=embed)