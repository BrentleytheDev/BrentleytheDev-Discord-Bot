import json
from pathlib import Path

CONFIG_PATH = Path(__file__).resolve().parent.parent / "config" / "automod" / "config.json"

async def open_config():
    with open(CONFIG_PATH, "r") as file:
        config = json.load(file)
        return config

async def write_config(config: dict):
    with CONFIG_PATH.open("w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)