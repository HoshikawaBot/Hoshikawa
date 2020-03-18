import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from package.commandHandler import cutHead
import package.db as db
from package.tag import Tag as PackageTag

class Tag(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    async def tag(self, ctx):
        print(cutHead(ctx.message.content, "tag").split(" ")[1:])
        if ctx.invoked_subcommand is None:
            if cutHead(ctx.message.content, "tag") != "":
                await self.read_core(ctx, arg="tag",
                params=cutHead(ctx.message.content, "tag").split(" ")[1:],
                content=cutHead(ctx.message.content, "tag").split(" ")[0])
            else:
                await ctx.send("tag create|raw|update|delete|(tagname) for read")

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
    
    @tag.command()
    async def raw(self, ctx):
        """show raw tag"""
        name = cutHead(ctx.message.content, "tag raw")
        await self.read_core(ctx, "tag raw", eval=False)
        return

    @tag.command()
    async def create(self, ctx):
        """create tag"""
        name = cutHead(ctx.message.content, "tag create")

        if db.getTagByName(name):
            await ctx.send("tag already exists")
            return

        await ctx.send(name)
        msg = await self.waitForMessage(ctx)
        db.appendTag(name, str(ctx.author.id), msg.content)
        await self.read_core(ctx, arg="tag create")
        return
    
    @tag.command()
    async def update(self, ctx):
        """update tag"""
        name = cutHead(ctx.message.content, "tag update")
        find = db.getTagByName(name)

        if not find:
            await ctx.send("message does not exists")
            return
        
        if ctx.author.id != int(find[1]):
            await ctx.send("message writer and tag writer is not same")
            return

        await self.read_core(ctx, arg="tag update", eval=False)

        msg = await self.waitForMessage(ctx)
        db.updateTag(name, msg.content)
        await self.read_core(ctx, arg="tag update", eval=False)
        return
    
    @tag.command()
    async def delete(self, ctx):
        """delete tag"""
        name = cutHead(ctx.message.content, "tag delete")

        if not db.getTagByName(name):
            await ctx.send("tag does not exists")
            return

        db.deleteTag(name)
        await ctx.send("message deleted!")
        return
    
    async def read_core(self, ctx, arg="tag read", params=(), content="", eval=True):
        name = cutHead(ctx.message.content, arg)
        if content:
            name = content
        res = db.getTagByName(name)
        if not res:
            await ctx.send("tag does not exists")
            return
        if eval:
            await ctx.send(PackageTag.eval(res[2], params))
        else:
            await ctx.send(res[2])
        return
    
    @tag.command()
    async def read(self, ctx, *args):
        """read tag"""
        await self.read_core(ctx, params=args[1:])
        return

def setup(bot):
    bot.add_cog(Tag(bot))