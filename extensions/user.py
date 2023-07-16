import discord

from typing import Optional

from discord.ext import commands

from app._base_types import BaseCog
from app.util import get_most_freq_colour
from app.views import LeaderboardView
from app.models.user import User


class UserCog(BaseCog, name="🏆 User"):
    @commands.command(aliases=["rank"])
    async def profile(self, ctx: commands.Context, user: Optional[commands.MemberConverter] = None):
        """
        Shows user profile.
        You can use command replying to a message to show profile of the user who sent the message.
        If no user is specified and no message is replied to, your profile will be shown.
        ⚠ You can't specify user and use reply at the same time.
        """
        if ctx.message.reference and user:
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "❌ You can't specify user and use reply at the same time.", 
                delete_after=5
            )
            return

        if ctx.message.reference:
            user = ctx.message.reference.resolved.author

        else:
            user = user or ctx.author

        if user.bot:
            await ctx.message.add_reaction("❌")
            await ctx.reply(
                "❌ Bots don't have profiles.", 
                delete_after=5
            )
            return

        user_db = (await User.get_or_create(
            user_id=user.id, guild_id=ctx.guild.id
        ))[0]

        embed = discord.Embed(
            title=f"{user}'s profile", 
            colour=await get_most_freq_colour(user.display_avatar.url)
        )

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)

        embed.add_field(
            name="⭐ Level", 
            value=(
                f" ᠌᠌  ᠌᠌ **`{user_db.level}`** (**`{user_db.exp}`/`{user_db.level_up_exp}`** xp)"
            ), 
            inline=False
        )

        embed.add_field(
            name=":coin: Coins", 
            value=(f" ᠌᠌  ᠌᠌ **`{user_db.coins}`**"), 
            inline=False
        )

        await ctx.reply(
            embed=embed, 
            allowed_mentions=discord.AllowedMentions.none()
        )

    @commands.command(aliases=["lb", "top"])
    async def leaderboard(self, ctx: commands.Context):
        """Shows users leaderboard."""
        view = LeaderboardView(
            bot=self.bot, 
            caller=ctx.author
        )

        msg = await ctx.reply(
            embed=await view.get_leaderboard(ctx.guild), 
            view=view, 
            allowed_mentions=discord.AllowedMentions.none()
        )

        view.post_init(
            parent_message=ctx.message, 
            message=msg
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UserCog(bot))
