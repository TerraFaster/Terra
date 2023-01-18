import os
import random
import discord

from discord.ext import commands
from tortoise import Tortoise
from loguru import logger

from app import config
from app.util import get_most_freq_colour
from app.models.user import User


class Client(commands.Bot):
    def __init__(self, *, prefixes: list[str], intents: discord.Intents) -> None:
        super().__init__(
            command_prefix=prefixes, 
            intents=intents
        )

    async def load_extensions(self) -> None:
        """
        Load all extensions from the extensions folder.
        """
        for root, dirs, files in os.walk(config.EXTENSIONS_DIR):
            for file in files:
                if file.endswith(".py") and not file.startswith("_"):
                    cog = f"{root}.{file[:-3]}".replace(os.sep, ".")

                    try:
                        await self.load_extension(cog)

                    except Exception as e:
                        logger.error(f"[Cog] {cog} cannot be loaded: {e}")

    async def connect_db(self) -> None:
        """
        Connect to the database.
        Load all models from the models folder and its subfolders.
        """
        await Tortoise.init(
            db_url=config.DB_URL,
            modules={
                "models": [
                    f"{root}.{file[:-3]}".replace("\\", ".").replace("/", ".")
                    for root, dirs, files in os.walk(config.DB_MODELS_DIR) 
                    for file in files 
                    if file.endswith(".py") and not file.startswith("_")
                ]
            }
        )
        await Tortoise.generate_schemas()

    async def on_ready(self) -> None:
        await self.connect_db()
        await self.load_extensions()

        print(
            f"\nLogged in as {self.user.name}#{self.user.discriminator} ({self.user.id})"
            f"\nGuilds: {len(self.guilds)} | Users: {len(self.users)}"
            f"\nLoaded: {len(self.extensions)} extensions | {len(self.cogs)} cogs | {len(self.commands)} commands"
            "\nInvite URL: https://discord.com/oauth2/authorize?client_id="
                f"{self.user.id}&scope=bot&permissions={self.intents.value}"
        )

    async def close(self) -> None:
        await Tortoise.close_connections()

        try:
            await super().close()

        except RuntimeError:
            # Ignore because bot is already closed
            pass

        except Exception as e:
            logger.error(f"Error while closing bot: {e}")

    async def on_message(self, msg: discord.Message, /) -> None:
        author = msg.author

        if author.bot:
            return

        user_db = (await User.get_or_create(
            user_id=author.id, guild_id=msg.guild.id
        ))[0]

        if user_db.blocked:
            return

        # Code from discord.ext.commands.Bot.process_commands(message)
        # But with check if message is a command otherwise it will process raw message
        ctx = await self.get_context(msg)
        
        if ctx.command is not None:
            await self.invoke(ctx)
            return

        # Change user's experience
        if 5 > len(msg.content) >= 100:
            return

        user_db.exp += random.randint(
            len(msg.content) // 4, 
            len(msg.content) // 2
        )

        # Level up user
        # XP to level up formula: req_exp + req_exp * 1.1 * (cur_level - 1)
        if user_db.exp >= user_db.level_up_exp:
            user_db.level += 1
            user_db.coins += 1

            await user_db.save()

            embed = discord.Embed(
                title=f"{author}'s profile", 
                color=await get_most_freq_colour(author.display_avatar.url)
            )

            embed.set_thumbnail(url=author.display_avatar.url)
            embed.set_author(name=author.name, icon_url=author.display_avatar.url)

            embed.add_field(
                name="Stats", 
                value=(
                    "🌟 Level:\n"
                    f" ᠌᠌ ᠌᠌• **`{user_db.level - 1}`** ➜ **`{user_db.level}`** (**`{user_db.exp}`/`{user_db.level_up_exp}`** xp)\n"
                    "\n\n💰 Coins:\n"
                    f" ᠌᠌ ᠌᠌• **`{user_db.coins}`**"
                )
            )

            await msg.reply(embed=embed)

        else:
            await user_db.save()


if __name__ == "__main__":
    intents = discord.Intents.all()

    bot = Client(
        prefixes=config.BOT_PREFIXES, 
        intents=intents
    )
    bot.run(config.BOT_TOKEN)
