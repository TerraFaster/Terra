import discord

from typing import Optional
from discord.ext import commands


class BaseCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.active = True


class BaseView(discord.ui.View):
    def __init__(self, *, bot: commands.Bot, caller: discord.Member, timeout: Optional[float] = 180):
        super().__init__(timeout=timeout)

        self.bot = bot
        self.caller = caller

        self.parent_message: discord.Message = None
        self.message: discord.Message = None

    def post_init(self, parent_message: discord.Message, message: discord.Message) -> None:
        """
        This method should be called after message containing this view is sent.

        Args:
            parent_message (discord.Message): Message that triggered this view.
            message (discord.Message): Message containing this view.
        """
        self.parent_message = parent_message
        self.message = message

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        if interaction.user != self.caller:
            await interaction.response.send_message(
                "❌ You do not have permission to interact with this view.", 
                ephemeral=True
            )
            return False

        return True

    async def on_timeout(self) -> None:
        for child in self.children:
            child.disabled = True

        try:
            await self.message.edit(view=self)

        except discord.NotFound:
            pass

        except:
            raise
