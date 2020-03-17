import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from discord import Embed

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def userinfo(self, ctx):
        person = ctx.message.mentions[0].id
        person = await self.bot.get_user_info(person)
        name = person.name
        discriminator = person.discriminator
        avatar = person.avatar_url
        id = person.id
        embed = Embed(title="%s#%s" % (name, discriminator),
            description="id:%s" % (id),
            color=0xE0FFFF)
        embed.set_thumbnail(url=avatar)
        await self.bot.send_message(ctx.message.channel, embed=embed)

def setup(bot):
    bot.add_cog(Say(bot))