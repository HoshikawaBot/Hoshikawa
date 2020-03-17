import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from package.settings import prefix
from package.commandHandler import cutHead

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx):
        """say something to bot."""
        await ctx.send(cutHead(ctx.message.content, "say"))
        return
    
    @commands.command()
    async def sayd(self, ctx):
        """say something to bot and remove message."""
        await ctx.send(cutHead(ctx.message.content, "sayd"))
        await ctx.message.delete()
        return

def setup(bot):
    bot.add_cog(Say(bot))