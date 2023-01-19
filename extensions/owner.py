from typing import Optional

from discord.ext import commands

from extensions._base_types import BaseCog


class OwnerCog(BaseCog, name="Owner"):
    @commands.is_owner()
    @commands.command(hidden=True)
    async def close(self, ctx: commands.Context):
        await ctx.reply("⛔ Closing...")
        await self.bot.close()

    @commands.is_owner()
    @commands.command(hidden=True)
    async def reload(self, ctx: commands.Context, ext: Optional[str] = None):
        # Reload all extensions if no cog is specified.
        if ext is None:
            errored = []

            for ext in list(self.bot.extensions.keys()):
                try:
                    await self.bot.reload_extension(ext)

                except commands.ExtensionNotFound:
                    errored.append(ext)

            await ctx.reply(
                f"✅ Reloaded `{len(self.bot.extensions) - len(errored)}`/`{len(self.bot.extensions)}` extensions." + 
                (("🔴 Failed to reload:\n• `" + "`\n• `".join(errored) + "`") if errored else ""), 
                delete_after=10
            )
            return

        # Reload a single extension if specified.
        try:
            await self.bot.reload_extension(ext)

        except commands.ExtensionNotFound:
            await ctx.reply(
                f"❌ Extension `{ext}` doesn't exist.", 
                delete_after=5
            )

        finally:
            await ctx.reply(
                f"✅ Reloaded `{ext}`.", 
                delete_after=5
            )

    @commands.is_owner()
    @commands.command(hidden=True)
    async def cogs(self, ctx: commands.Context):
        await ctx.reply(
            "\n".join(
                [
                    f"`{index + 1}`. **{cog.qualified_name}** {'✅' if cog.active else '❌'}"
                    for index, cog in enumerate(self.bot.cogs.values())
                ]
            ), 
            delete_after=15
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(OwnerCog(bot))
