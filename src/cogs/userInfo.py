import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from discord import Embed
import time
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

        currentyear = time.strftime("%Y")

        ymd = str(person.created_at).split(" ")[0].split("-")
        ymdString = f"{ymd[0]}년 {ymd[1]}월 {ymd[2]}일"

        embed = Embed(title="%s님 유저 정보" % (name),
            color=0xE0FFFF)
        embed.set_image(url=avatar)
        embed.add_field(name="이름", value=f"{name}#{discriminator}")
        embed.add_field(name="아이디:", value=id)
        embed.add_field(name="계정 생성일:", value=ymdString)
        embed.set_footer(text=f"{currentyear} HoshikawaBot, MIT License")
        await ctx.send("", embed=embed)

def setup(bot):
    bot.add_cog(UserInfo(bot))