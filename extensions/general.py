from discord.ext import commands

from extensions._base_types import BaseCog


class GeneralCog(BaseCog):
    ...


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))