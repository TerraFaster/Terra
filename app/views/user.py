import discord

from discord.ext import commands

from app._base_types import BaseView
from app.models.user import User
from app.util import get_most_freq_colour


class LeaderboardView(BaseView):
    def __init__(self, *, bot: commands.Bot, caller: discord.Member, page: int = 1, **kwargs):
        super().__init__(
            bot=bot, caller=caller, **kwargs
        )

        self.page = page
        self.USER_PER_PAGE = 10

    async def get_leaderboard(self, guild: discord.Guild, page: int = 1) -> discord.Embed:
        users = await User.filter(guild_id=guild.id).order_by("-level", "-exp")
        icon = guild.icon.url if guild.icon else self.bot.user.display_avatar.url

        embed = discord.Embed(
            title="🏆 Leaderboard", 
            description=f"**Page `{page}` of `{len(users) // self.USER_PER_PAGE + 1}` — Total members: `{len(users)}`**", 
            colour=await get_most_freq_colour(icon)
        )

        embed.set_thumbnail(url=icon)
        embed.set_author(name=guild.name, icon_url=icon)

        for i, user in enumerate(users[self.USER_PER_PAGE * (page - 1):self.USER_PER_PAGE * page]):
            member = guild.get_member(user.user_id)

            embed.add_field(
                name=f"#{self.USER_PER_PAGE * (page - 1) + i + 1}. " + (
                    member.display_name if member else f"Unknown user (`{user.user_id}`)"
                ), 
                value=(
                    f"⭐ Level: **`{user.level}`** (**`{user.exp}`/`{user.level_up_exp}`** xp)"
                    f"**` | `**:coin: Coins: **`{user.coins}`**"
                ), 
                inline=False
            )

        return embed

    @discord.ui.button(label="◀ Previous", style=discord.ButtonStyle.primary)
    async def previous_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.page == 1:
            return await interaction.response.send_message(
                "❌ You are already on the first page!", 
                ephemeral=True
            )

        self.page -= 1

        await interaction.response.edit_message(
            embed=await self.get_leaderboard(interaction.guild, self.page), 
            view=self
        )
    
    @discord.ui.button(label="Next ▶", style=discord.ButtonStyle.primary)
    async def next_page(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        if self.page == len(await User.filter(guild_id=interaction.guild.id)) // self.USER_PER_PAGE + 1:
            return await interaction.response.send_message(
                "❌ You are already on the last page!", 
                ephemeral=True
            )

        await interaction.response.edit_message(
            embed=await self.get_leaderboard(interaction.guild, self.page + 1), 
            view=self
        )

    @discord.ui.button(label="❌ Close", style=discord.ButtonStyle.danger)
    async def close(self, interaction: discord.Interaction, button: discord.ui.Button) -> None:
        await interaction.response.defer()

        await self.parent_message.add_reaction("✅")
        await interaction.delete_original_response()
