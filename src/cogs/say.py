from discord.ext import commands

class Say(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def say(self, ctx):
        """say something to bot."""
        await ctx.send(ctx.message)
        return
    
    @commands.command()
    async def sayd(self, ctx):
        """say something to bot and remove message."""
        await ctx.send(ctx.message)
        await ctx.message.delete()
        return

def setup(bot):
    bot.add_cog(Say(bot))