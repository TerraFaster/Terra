import discord

from discord.ext import commands


class HelpCategoriesDropdown(discord.ui.Select):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

        # Filter out cogs that only have hidden commands.
        cogs = [
            cog for cog in bot.cogs.values() 
            if not all(cmd.hidden for cmd in cog.get_commands())
        ]

        options = [
            discord.SelectOption(label=cog.qualified_name)
            for cog in cogs
        ]

        super().__init__(
            placeholder="🔍 Select a category...", 
            options=options
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        cog = self.bot.get_cog(self.values[0])

        embed = discord.Embed(
            title=f"{cog.qualified_name} commands", 
            description=(
                f"Use **`<>help <command>`** for more info on a command."
                f"\n**`<option>`** — **required** ` | ` **`[option]`** — **optional**"
            )
        )

        embed.add_field(
            name="", 
            value="\n\n".join([
                f"<>{cmd.name}" + " ".join([
                    "**` " + (f"<{param.name}>" if param.required else f"[{param.name}]") + " `**"
                    for param in cmd.clean_params.values()
                ]) +
                f"\n ᠌᠌  ᠌᠌ {cmd.help}" + (
                    "\n ᠌᠌  ᠌᠌ `――――――――――――――――――――――――――――――――――――――`"
                    f"\n ᠌᠌  ᠌᠌ Aliases:**` {' ` | ` '.join(cmd.aliases)} `**" 
                    if cmd.aliases else ""
                )
                for cmd in cog.get_commands()
                if not cmd.hidden
            ])
        )

        await interaction.response.send_message(
            embed=embed, ephemeral=True
        )


class HelpView(discord.ui.View):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        
        self.add_item(HelpCategoriesDropdown(bot))
