from discord.ext import commands
from package.settings import prefix

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx):
        """say something to bot."""
        await ctx.send(ctx.message.content[len(prefix)+3+1:])
        return
    
    @commands.command()
    async def sayd(self, ctx):
        """say something to bot and remove message."""
        await ctx.send(ctx.message.content[len(prefix)+4+1:])
        await ctx.message.delete()
        return

def setup(bot):
    bot.add_cog(Say(bot))