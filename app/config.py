import os

from discord.ext.commands import when_mentioned_or

DB_URL = "sqlite://db.sqlite3"
DB_MODELS_DIR = "app/models"
EXTENSIONS_DIR = "extensions"

BOT_TOKEN = os.environ.get("DISCORD_BOT_TOKEN", "YOUR_TOKEN_HERE")
BOT_PREFIXES = when_mentioned_or(
    ".", ">", "<>"
)