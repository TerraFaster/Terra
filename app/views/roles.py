import discord

from discord.ext import commands

from app._base_types import BaseView
from app.util import get_most_freq_colour
from app.models.guild import Guild


class RolesDropdown(discord.ui.RoleSelect):
    def __init__(self) -> None:
        super().__init__(
            placeholder="🔍 Select a role...", 
            max_values=15
        )

    async def callback(self, interaction: discord.Interaction) -> None:
        guild = interaction.guild
        guild_db = (await Guild.get_or_create(id=guild.id))[0]
        icon = guild.icon.url if guild.icon else self.bot.user.display_avatar.url
        selected_roles = self.values.copy()

        updated_roles = {
            "added": [], 
            "removed": [], 
            "invalid": {}
        }

        # Remove roles if they were already selected
        for role in selected_roles:
            if role.id in guild_db.newcomer_roles:
                guild_db.newcomer_roles.remove(role.id)
                updated_roles["removed"].append(role)
                selected_roles.remove(role)

        # Add remaining roles
        for role in selected_roles:
            if role.is_bot_managed():
                updated_roles["invalid"][role] = \
                    "Role is managed by an integration."

            elif not role.is_assignable():
                updated_roles["invalid"][role] = \
                    f"Role is higher than {guild.me.mention}'s highest role OR is default role."

            elif len(guild_db.newcomer_roles) >= self.view.MAX_NEWCOMER_ROLES:
                updated_roles["invalid"][role] = \
                    f"Maximum number of roles reached ({self.view.MAX_NEWCOMER_ROLES})."

            else:
                guild_db.newcomer_roles.append(role.id)
                updated_roles["added"].append(role)

        await guild_db.save()
        
        # Update roles in embed
        await interaction.response.edit_message(
            embed=await self.view.get_newcomer_roles(interaction.guild)
        )

        # Send summary message
        embed = discord.Embed(
            title="ℹ Newcomer roles updated", 
            description=(
                f"**Added `{len(updated_roles['added'])}` | "
                f"Removed `{len(updated_roles['removed'])}` | "
                f"Invalid `{len(updated_roles['invalid'])}`**"
            ), 
            colour=await get_most_freq_colour(icon)
        )

        if updated_roles["added"]:
            embed.add_field(
                name="**➕ Added roles:**", 
                value=", ".join(role.mention for role in updated_roles["added"]) or "None", 
                inline=False
            )

        if updated_roles["removed"]:
            embed.add_field(
                name="**➖ Removed roles:**", 
                value=", ".join(role.mention for role in updated_roles["removed"]) or "None", 
                inline=False
            )

        if updated_roles["invalid"]:
            embed.add_field(
                name="**❌ Unable to add the following roles:**", 
                value="\n".join(
                    f"{role.mention}** - {reason}**"
                    for role, reason in updated_roles["invalid"].items()
                ), 
                inline=False
            )

        await interaction.followup.send(embed=embed, ephemeral=True)


class RolesView(BaseView):
    def __init__(self, *, bot: commands.Bot, caller: discord.Member, **kwargs):
        super().__init__(bot=bot, caller=caller, **kwargs)

        self.add_item(RolesDropdown())

        self.MAX_NEWCOMER_ROLES = 15

    async def get_newcomer_roles(self, guild: discord.Guild) -> discord.Embed:
        guild_db = (await Guild.get_or_create(id=guild.id))[0]
        icon = guild.icon.url if guild.icon else self.bot.user.display_avatar.url

        await guild_db.validate_roles(guild)

        embed = discord.Embed(
            title="Newcomer Roles", 
            description="Select the roles you want to give to new members when they join the server.", 
            colour=await get_most_freq_colour(icon)
        )

        embed.set_thumbnail(url=icon)

        embed.add_field(
            name=f"**Current newcomer roles (`{len(guild_db.newcomer_roles)}`/`{self.MAX_NEWCOMER_ROLES}`)**", 
            value="\n".join(
                f"• {guild.get_role(role_id).mention}"
                for role_id in guild_db.newcomer_roles
            ) or "⚠️ No roles have been set."
        )

        return embed
