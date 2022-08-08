import inspect
import json
import os
from pydoc import describe
import sys
import asyncio
import discord
from discord import default_permissions
from discord.commands import slash_command, Option
from discord.ext import commands


sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))))
from modules.embed import embed

with open('config.json') as f:
    data = json.load(f)
    guilds = data["guilds"]


class Admin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @slash_command(name="mute", description="Mutes User", guild_ids=[703637471212077096])
    @default_permissions(mute_members=True)
    async def mute(self, ctx: commands.Context, user: Option(discord.User, "User", required=True), duration: Option(int, "Duration (s)", default="0"), reason: Option(str, "Reason", default="Muted")):
        prole = False
        for role in ctx.guild.roles:
            if role.name.lower() == "muted":
                prole = True
                break
            else:
                prole = False
        if not prole:
            await ctx.guild.create_role(name="Muted", permissions=discord.Permissions(permissions=2048), color=discord.Color(0x111111))
        role = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
        await user.add_roles(role, reason=reason)
        if duration == 0:
            await ctx.respond(embed=embed(ctx, title=f"Muted {user.name}", footer={"text": reason}))
        else:
            a=embed(ctx, title=f"Muted {user.name} for {(duration)} Seconds", footer=[{'text': f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | {duration}s | Reason = {reason}'}])
            b = await ctx.respond(embed=embed)
            for sec in range(duration):
                a.footer = [{'text': f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | {duration - sec}s'}]
                await b.edit_original_message(embed=a)
                await asyncio.sleep(1)
            a.footer= [{'text': f'{ctx.bot.user.name} | Requested By: {ctx.author.name} | Mute Finished | Reason = {reason}'}]
            await b.edit_original_message(embed=a)
            await user.remove_roles(role, reason="Auto Un Mute")

    @slash_command(name="unmute", description="Un Mutes User", guild_ids=[703637471212077096])
    @default_permissions(mute_members=True)
    async def unmute(self, ctx, user: Option(discord.User, "User", required=True), reason: Option(str, "Reason", default="Un-Muted")):
        role = discord.utils.find(lambda r: r.name == "Muted", ctx.guild.roles)
        if role in user.roles:
            await user.remove_roles(role, reason=reason)
            await ctx.respond(embed=embed(ctx, title=f"Un Muted {user.name}"))
        else:
            await ctx.respond(embed=embed(ctx, title=f"{user.name} is not muted"))



def setup(bot):
    bot.add_cog(Admin(bot))
