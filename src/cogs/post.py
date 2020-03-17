import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
import package.db as db
import traceback
from discord import Embed

from package.settings import prefix
from package.commandHandler import cutHead

class Post(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def post(self, ctx):
        if ctx.invoked_subcommand is None:
            if cutHead(ctx.message.content, "post") != "":
                await self.read_core(ctx, arg="post")
            else:
                await ctx.send("post create|update|delete|read")

    async def waitForMessage(self, ctx, timeout=1000.0):
        await ctx.send(f"<@{ctx.message.author.id}> message listening...")
        await ctx.send("type 'cancel' to cancel.")

        def checkfn(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', timeout=timeout, check=checkfn)
            if msg.content == "cancel":
                await ctx.send("canceled.")
                return None
        except:
            # traceback.print_exc(file=sys.stdout)
            await ctx.send("timeout!")
            return None
        else:
            await ctx.send(msg.content)
            return msg
        
    @post.command()
    async def create(self, ctx):
        """create post"""
        name = cutHead(ctx.message.content, "post create")

        if db.getPostByName(name):
            await ctx.send("post already exists")
            return

        await ctx.send(name)
        msg = await self.waitForMessage(ctx)
        db.appendPost(name, str(ctx.author.id), msg.content)
        await self.read_core(ctx, arg="post create")
        return
    
    @post.command()
    async def update(self, ctx):
        """update post"""
        name = cutHead(ctx.message.content, "post update")
        find = db.getPostByName(name)

        if not find:
            await ctx.send("message does not exists")
            return
        
        if ctx.author.id != int(find[1]):
            await ctx.send("message writer and post writer is not same")
            return
        
        await self.read_core(ctx, arg="post update")

        msg = await self.waitForMessage(ctx)
        db.updatePost(name, msg.content)
        await self.read_core(ctx, arg="post update")
        return
    
    @post.command()
    async def delete(self, ctx):
        """delete post"""
        name = cutHead(ctx.message.content, "post delete")

        if not db.getPostByName(name):
            await ctx.send("post does not exists")
            return

        db.deletePost(name)
        await ctx.send("message deleted!")
        return
    
    async def read_core(self, ctx, arg="post read"):
        name = ""
        name = cutHead(ctx.message.content, arg)
        res = db.getPostByName(name)
        if not res:
            await ctx.send("post does not exists")
            return
        author = self.bot.get_user(int(res[1]))
        embed = Embed(title=res[0], description=res[2], color=0x93faff)
        embed.set_footer(text=f"{author} 작성")
        await ctx.send("", embed=embed)
        return
    
    @post.command()
    async def read(self, ctx):
        """read post"""
        await self.read_core(ctx)

def setup(bot):
    bot.add_cog(Post(bot))