import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
import package.db as db

from package.settings import prefix
from package.commandHandler import cutHead

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def post(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send('post create|update|delete|read')

    @post.command()
    async def create(self, ctx):
        """create post"""
        await ctx.send("create")
        return
    
    @post.command()
    async def update(self, ctx):
        """update post"""
        await ctx.send("update")
        return
    
    @post.command()
    async def delete(self, ctx):
        """delete post"""
        await ctx.send("delete")
        return
    
    @post.command()
    async def read(self, ctx):
        """read post"""
        await ctx.send("read")
        return

def setup(bot):
    bot.add_cog(Post(bot))