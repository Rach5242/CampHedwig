import discord, typing, random, datetime, asyncio
from discord.ext import tasks, commands
from discord.ext.commands import has_permissions, has_guild_permissions, MissingPermissions
from random import choice
from typing import Optional
from Cogs import database as db


class Drops(commands.Cog):
    """<a:jumpys:871708733355474964> Smores Season Commands<a:jumpys:871708733355474964>
    """
    def __init__(self, bot):
        self.bot = bot

    async def send_drop(self, drop):
        guild = self.bot.get_guild(int(drop[0]))
        channel = guild.get_channel(int(drop[1]))
        emoji_id = drop[2].strip("<>").split(":")
        emoji = self.bot.get_emoji(id=int(emoji_id[1] if emoji_id[0] != 'a' else emoji_id[2]))
        embed = discord.Embed(
            description=drop[3],
            color=discord.Colour.random()
        )
        if drop[4] is not None:
            embed.set_thumbnail(url=drop[4])
        
        msg = await channel.send(embed=embed)
        await msg.add_reaction(emoji)

        def check(reaction, user):
            return reaction.messageid == msg and user != user.bot and str(reaction.emoji) == emoji
        
        try:
            reaction, user = await self.bot.wait_for('reaction_add', check=check, timeout=300)
            print("waiting for reaction")
            if str(reaction.emoji) == emoji:
                print("Caught Reaction")
                count = await db.fetch_user(guild.id, user.id)
                count = count[2]
                await msg.edit(embed = discord.Embed(description=f"{user.mention} has claimed the {emoji}! They now have {emoji}`{int(count) + 1}`"), delete_after=5)
                await db.update_count(guild.id, user.id)
        
        except asyncio.TimeoutError:
            try:
                message = await channel.fetch_message(msg.id)
                await message.delete()
            except discord.Forbidden:
                pass
            
    @tasks.loop(seconds = 30)
    async def auto_message(self, guild):
        timenow = datetime.datetime.utcnow().strftime('%m %d, %Y %H:%M:%S')
        drops = await db.fetch_all_drops()
        for drop in drops:
            Delta = datetime.timedelta(seconds=int(drop[5]))
            Last = datetime.datetime.strptime(drop[6], "%m %d, %Y %H:%M:%S")
            Now = datetime.datetime.utcnow().strptime(timenow, '%m %d, %Y %H:%M:%S')
            Next = Last + Delta
            if Next <= Now:
                await Drops.send_drop(self, drop)
                await db.set_last_drop(int(drop[0]))
            else:
                pass

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.__class__.__name__} is Ready!")

    @commands.command(description="See your personal Smores' Count")
    async def smores(self, ctx, member: Optional[discord.Member]=None):
        if member is None:
            member = ctx.author

        result = await db.fetch_user(ctx.guild.id, member.id)

        embed = discord.Embed(
            description="{member.mention} has claimed `{result[2]}`<a:jumpys:871708733355474964> smores!",
            color=discord.Colour.random()
        )
        await ctx.send(embed=embed)

    @commands.command(aliases=['lb', 'top'], description="See who has collected the most <a:jumpys:871708733355474964> in the Server")
    async def leaderboard(self, ctx):
        """|<a:jumpys:871708733355474964> Leaderboards <a:jumpys:871708733355474964>"""
        results = await db.fetch_all(ctx.guild.id)
        leaderboards = []
        leaderboards.append("{:^4} | {:^5} | {:^16}".format("NO.#", "Count", "Member"))
        n = 1
        for result in results[0:9]: 
            member = ctx.guild.get_member(int(result[1]))
            leaderboards.append("{:^4} | {:^5} | {:^16} ".format(n, result[2], member.display_name if not len(str(member.display_name)) > 16 else str(member.display_name)[:13] + "..."))
            n += 1

        embed = discord.Embed(
            title=f"{ctx.guild.name.title()}'s Leaders",
            description="```{}```".format('\n'.join(leaderboards)),
            color=discord.Colour.random()
        )
        embed.set_thumbnail(url=ctx.guild.icon_url)
        await ctx.send(embed=embed)

    @commands.command(name="stop", description="Must have Manage Server Permissions to use.", hidden=True)
    async def _stop(self, ctx):
        """|<a:jumpys:871708733355474964> Stops <a:jumpys:871708733355474964> Auto-Messages <a:jumpys:871708733355474964>"""
        if ctx.author.id not in self.bot.user_ids:
            await ctx.reply("You are not one of the accepted users of that command.", delete_after=5)
        
        else:
            self.auto_message.cancel()
            await ctx.send(f"<a:846056333668122634:875460650762113064> Message has been stopped. To start type `{ctx.prefix}run`.")
            print("Task Stopped")

    @commands.command(name="run", description="Must have Manage Server Permissions to use.", hidden=True)
    async def _run(self, ctx):
        """|<a:jumpys:871708733355474964> Starts <a:jumpys:871708733355474964> Auto-Messages <a:jumpys:871708733355474964>"""
        if ctx.author.id not in self.bot.user_ids:
            await ctx.reply("You are not one of the accepted users of that command.", delete_after=5)
        
        else:
            self.auto_message.start(ctx.guild)
            await ctx.send(f"<a:846056333668122634:875460650762113064> Message has been started! To stop type: `{ctx.prefix}stop`.")
            print("Task Started")

def setup(bot):
    bot.add_cog(Drops(bot))