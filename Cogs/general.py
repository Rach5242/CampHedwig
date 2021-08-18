import discord, typing, asyncio, random, datetime
from discord.ext import commands
from discord.ext.commands import has_any_role
from typing import Optional, Union
from random import choice, randint
from Cogs import database as db

class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is ready!")

    @commands.command(description="Shows command help")
    async def help(self, ctx):
        embed = discord.Embed(
            title="Command Help", 
            description="Anything in:\n`[]` is Optional \n`<>` is mandatory.",
            color=discord.Colour.dark_green()
        )
        embed.add_field(name=f"`{ctx.prefix}leaderboards` | Aliases: `{ctx.prefix}top`, `{ctx.prefix}lb` ", value="Displays the top ten members in the server.", inline=False)
        embed.add_field(name=f"`{ctx.prefix}claims [@Member]`| Aliases: `None`", value="Display's your personal marshmallow count, or that of the mentioned member.", inline=False)

        await ctx.message.delete()
        await ctx.send(embed=embed)

    @commands.command(name='set', description="Set prefix, dropdchannel, droptime, on,  off")
    async def _set(self, ctx, marker, *, setting: Union[discord.TextChannel, str, discord.Emoji]):
        if ctx.author.id not in self.bot.user_ids:
            await ctx.send("You are not one of the accepted users of that command.", delete_after=5)
        
        else:
            print("Passed User check")
            if marker.lower() == 'prefix' and isinstance(setting, str):
                prefix = setting.split(' ')
                await db.add_prefix(ctx.guild.id, prefix[0])
                response = f'Set `{prefix[0]}` as the server prefix'
            
            elif marker.lower() == 'dropchannel':
                await db.set_drop_channel(ctx.guild.id, setting.id)
                response = f"Drops will now spawn in {setting.mention}"
            
            elif marker.lower() == 'droptime':
                if isinstance(setting, int):
                    time = setting * 120
                
                elif isinstance(setting, str):
                    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
                    time= int(setting[0]) * time_convert[str(setting[-1])]

                await db.set_msg_time(ctx.guild.id, time)
                response = f"Set Drop time to `{setting}`"
            
            elif marker.lower() == 'drop':
                if setting.lower() == 'on':
                    await db.toggle_drop(ctx.guild.id, 'True')
                    response = "Drops `Enabled`"

                elif setting.lower() == "off":
                    await db.toggle_drop(ctx.guild.id, 'False')
                    response = "Drops `Disabled`"
            

            await ctx.message.delete()
            await ctx.send(embed=discord.Embed(description=response, color=discord.Colour.dark_green()), delete_after=10)

def setup(bot):
    bot.add_cog(General(bot))