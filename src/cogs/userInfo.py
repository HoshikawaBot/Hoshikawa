import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from discord import Embed
import datetime

class UserInfo(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def userinfo(self, ctx):
        person = ctx.message.mentions[0].id
        person = self.bot.get_user(person)
        name = person.name
        discriminator = person.discriminator
        avatar = person.avatar_url
        id = person.id

        currentyear = datetime.now().year

        embed = Embed(title="%s" % (name),
            description="%s#%s님 유저 정보" % (name, discriminator),
            color=0xE0FFFF)
        embed.add_field(name="아이디", value=id)
        embed.set_thumbnail(url=avatar)
        embed.set_footer(text=f"{currentyear} HoshikawaBot, MIT License")
        await ctx.send("", embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))