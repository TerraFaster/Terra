import discord

from tortoise.models import Model
from tortoise import fields


class Guild(Model):
    id = fields.IntField(pk=True)
    prefix = fields.CharField(max_length=5, default="!")
    newcomer_roles = fields.JSONField(default=[])
    
    class Meta:
        table = "guilds"

    async def validate_roles(self, guild: discord.Guild) -> None:
        """Validates guild roles and removes invalid."""
        has_invalid_roles = False

        # Validate newcomer roles
        for role_id in self.newcomer_roles:
            role = guild.get_role(role_id)

            if role is None:
                self.newcomer_roles.remove(role_id)
                has_invalid_roles = True

        if has_invalid_roles:
            await self.save()
