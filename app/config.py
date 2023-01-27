import os

from discord.ext.commands import when_mentioned_or

DB_URL = "sqlite://db.sqlite3"
DB_MODELS_DIR = "app/models"

TORTOISE_ORM = {
    "connections": {
        "default": DB_URL
    }, 
    "apps": {
        "contact": {
            "models": [
                f"{root}.{file[:-3]}".replace("\\", ".").replace("/", ".")
                for root, dirs, files in os.walk(DB_MODELS_DIR) 
                for file in files 
                if file.endswith(".py") and not file.startswith("_")
            ] + ["aerich.models"], 
            "default_connection": "default"
        }
    }
}

EXTENSIONS_DIR = "extensions"

BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "YOUR_TOKEN_HERE")
BOT_PREFIXES = when_mentioned_or(
    ".", ">", "<>"
)