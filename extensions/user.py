import discord

from typing import Optional

from discord.ext import commands

from extensions._base_types import BaseCog
from app.util import get_most_freq_colour
from app.models.user import User


class UserCog(BaseCog):
    @commands.command()
    async def profile(self, ctx: commands.Context, user: Optional[commands.MemberConverter] = None):
        user: discord.Member = user or ctx.author

        user_db = (await User.get_or_create(
            user_id=user.id, guild_id=ctx.guild.id
        ))[0]

        embed = discord.Embed(
            title=f"{user}'s profile", 
            color=await get_most_freq_colour(user.display_avatar.url)
        )

        embed.set_thumbnail(url=user.display_avatar.url)
        embed.set_author(name=user.name, icon_url=user.display_avatar.url)

        embed.add_field(
            name="Stats", 
            value=(
                "🌟 Level:\n"
                f" ᠌᠌ ᠌᠌• **`{user_db.level}`** (**`{user_db.exp}`/`{user_db.level_up_exp}`** xp)"
                "\n\n💰 Coins:\n"
                f" ᠌᠌ ᠌᠌• **`{user_db.coins}`**"
            )
        )

        await ctx.reply(
            embed=embed, 
            allowed_mentions=discord.AllowedMentions.none()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UserCog(bot))
