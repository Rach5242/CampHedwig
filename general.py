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

    @commands.command(name='set', description="Set prefix, dropdchannel, dropmessage, dropimage, droptime, dropemoji")
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
                print("Made it inside Elif")
                await db.set_drop_channel(ctx.guild.id, setting.id)
                print("added to DB")
                response = f"Drops will now spawn in {setting.mention}"
                print("response sent")
                
            elif marker.lower() == 'dropmessage':
                await db.set_drop_msg(ctx.guild.id, setting)
                response = "Added drop message to database."
            
            elif marker.lower() == 'dropimage':
                await db.set_drop_image(ctx.guild.id, setting)
                response = "Added drop image to database."
            
            elif marker.lower() == 'dropemoji':
                try:
                    EMOJI_ID = setting.id
                except Exception:
                    EMOJI_COMPS =  setting.strip("<>").split(':')
                    EMOJI_ID = EMOJI_COMPS[1]
                
                await db.set_drop_emoji(ctx.guild.id, setting)
                response = "Added drop emoji to database."
            
            elif marker.lower() == 'droptime':
                if isinstance(setting, int):
                    time = setting * 120
                
                elif isinstance(setting, str):
                    time_convert = {"s":1, "m":60, "h":3600,"d":86400}
                    time= int(setting[0]) * time_convert[str(setting[-1])]

                await db.set_msg_time(ctx.guild.id, time)
                response = f"Set Drop time at {setting}"

            await ctx.send(embed=discord.Embed(description=response, color=discord.Colour.random()), delete_after=10)

def setup(bot):
    bot.add_cog(General(bot))