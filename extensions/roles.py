import discord

from discord.ext import commands

from app._base_types import BaseCog
from app.models.guild import Guild
from app.models.user import User
from app.views import RolesView


class RolesCog(BaseCog, name="Roles"):
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member):
        guild_db = (await Guild.get_or_create(id=member.guild.id))[0]
        await User.get_or_create(user_id=member.id, guild_id=member.guild.id)
        
        await guild_db.validate_roles(member.guild)

        await member.add_roles(*[
            member.guild.get_role(role_id)
            for role_id in guild_db.newcomer_roles
        ])

    @commands.command(name="newcomer-roles", aliases=["nc-roles", "ncr"])
    @commands.has_permissions(manage_roles=True)
    @commands.bot_has_permissions(manage_roles=True)
    async def newcomer_roles(self, ctx: commands.Context):
        """Manage the roles that are given to new members."""
        view = RolesView(
            bot=self.bot, 
            caller=ctx.author
        )

        msg = await ctx.reply(
            embed=await view.get_newcomer_roles(ctx.guild), 
            view=view, 
            allowed_mentions=discord.AllowedMentions(roles=False)
        )

        view.post_init(
            parent_message=ctx.message, 
            message=msg
        )


async def setup(bot: commands.Bot):
    await bot.add_cog(RolesCog(bot))
