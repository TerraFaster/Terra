import discord

from typing import Optional

from discord.ext import commands

from extensions._base_types import BaseCog
from app.views import HelpView


class GeneralCog(BaseCog, name="📋 General"):
    @commands.command()
    async def help(self, ctx: commands.Context, command: Optional[str] = None) -> None:
        """Shows this message. Use `<>help <command>` for more info on a command."""
        # Show all available categories and their commands.
        if command is None:
            # Filter out cogs that only have hidden commands.
            cogs = [
                cog for cog in self.bot.cogs.values() 
                if not all(cmd.hidden for cmd in cog.get_commands())
            ]

            embed = discord.Embed(
                title="Available categories and commands", 
                description=(
                    f"Use **`<>help <command>`** for more info on a command."
                    f"\n**`<option>`** — **required** ` | ` **`[option]`** — **optional**"
                )
            )

            for cog in cogs:
                embed.add_field(
                    name=f"**{cog.qualified_name}**", 
                    value="`" + "`, `".join([
                        f"<>{cmd.name}" for cmd in cog.get_commands() if not cmd.hidden
                    ]) + "`", 
                    inline=False
                )

            await ctx.reply(
                embed=embed, 
                view=HelpView(self.bot)
            )

        # Show help for a specific command.
        else:
            cmd = self.bot.get_command(command)

            if cmd is None:
                await ctx.reply(f"❌ Requested command **\"{command}\"** was not found.")
                return

            # Create aliases list with all possible command names
            # and remove the command name from the list.
            aliases = cmd.aliases + [cmd.name]

            if command in aliases:
                aliases.pop(aliases.index(command))

            embed = discord.Embed(
                title=f"Help for command \"**{command}**\"", 
                description=f"**`<option>`** — **required** ` | ` **`[option]`** — **optional**"
            )

            embed.add_field(
                name="📋 Description", 
                value=f" ᠌᠌  ᠌᠌ {cmd.help}", 
                inline=False
            )

            embed.add_field(
                name="📚 Usage", 
                value=f" ᠌᠌  ᠌᠌ <>**{cmd.name}** " + " ".join([
                    f"**` <{param.name}> `**" if param.required else f"**` [{param.name}] `**"
                    for param in cmd.clean_params.values()
                ]), 
                inline=False
            )

            if aliases:
                embed.add_field(
                    name="🔗 Aliases", 
                    value=f" ᠌᠌  ᠌᠌ **`{' ` | ` '.join(aliases)} `**", 
                    inline=False
                )

            await ctx.reply(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(GeneralCog(bot))
