import discord

from discord.ext import commands

from extensions._base_types import BaseCog


class UtilCog(BaseCog, name="🔧 Util"):
    @commands.command(name="first-message", aliases=["firstmsg", "fmsg"])
    async def first_message(self, ctx: commands.Context):
        """Shows first message in channel."""
        msg: discord.Message = await ctx.channel.history(limit=1, oldest_first=True).first()
        
        await msg.reply(
            f"First message in this channel.",
            allowed_mentions=discord.AllowedMentions.none()
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(UtilCog(bot))
