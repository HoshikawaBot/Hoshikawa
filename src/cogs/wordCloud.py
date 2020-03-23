import os
import sys
from discord.ext import commands
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__)))) # 상위 경로 import 가능
from package.commandHandler import cutHead
import package.db as db
from functools import reduce
from package.settings import prefix
import requests
import traceback
from wordcloud import WordCloud, ImageColorGenerator
import matplotlib.pyplot as plt 
import numpy as np
from PIL import Image
import discord

class WordCloud_(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    async def getAllMessagesFromGuild(self, server, filterFunc=lambda x: x):
        channels = [x for x in server.text_channels]
        result = []
        for channel in channels:
            result += await self.getMessagesFromChannel(channel, filterFunc=filterFunc)
        return result

    async def getMessagesFromChannel(self, channel, limit=1000, filterFunc=lambda x: x):
        result = []
        async for msg in channel.history(limit=limit):
            if filterFunc(msg):
                result.append(msg)
        return result
    
    def getImgByUrl(self, url, fileID):
        response = requests.get(url)
        if response.status_code == 200:
            with open(f"db/{fileID}.png", 'wb') as f:
                f.write(response.content)
        return f"db/{fileID}.png"
    
    def parseMessagesContent(self, msgs):
        return [x.content for x in msgs]

    @commands.group()
    async def wordcloud(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(prefix+"wordcloud -channel| -server| -me")
    
    @wordcloud.command(name="-channel")
    async def wordcloudChannel(self, ctx):
        msgs = await self.getMessagesFromChannel(ctx.channel)
        msg_contents = self.parseMessagesContent(msgs)
        await self.generateCloud(ctx, msg_contents)

    @wordcloud.command(name="-server")
    async def wordcloudServer(self, ctx):
        msgs = await self.getAllMessagesFromGuild(ctx.guild)
        msg_contents = self.parseMessagesContent(msgs)
        await self.generateCloud(ctx, msg_contents)

    @wordcloud.command(name="-me")
    async def wordcloudMe(self, ctx):
        filterFunc = lambda x: x.author.id == ctx.author.id
        msgs = await self.getAllMessagesFromGuild(ctx.guild, filterFunc)
        msg_contents = self.parseMessagesContent(msgs)
        await self.generateCloud(ctx, msg_contents)
    
    async def generateCloud(self, ctx, msg_contents):
        await ctx.send("사진을 올리실건가요? (예|아니오|취소)")

        def checkfn(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

        try:
            msg = await self.bot.wait_for('message', timeout=1000.0, check=checkfn)
            if msg.content == "예":
                await ctx.send("사진을 올려주세요.")
                picture_msg = await self.bot.wait_for('message', timeout=1000.0, check=checkfn)
                if picture_msg.attachments[0].url:
                    await ctx.send("사진의 모양으로 만듭니다...")
                    imgPath = self.getImgByUrl(picture_msg.attachments[0].url, str(ctx.author.id))
                    resultPath = self.generateCloud_core(ctx, msg_contents, imgPath)
                    await self.sendWCImagesAndRemove(ctx, resultPath)
                else:
                    await ctx.send("사진이 아닙니다! 취소합니다...")
                    return
            elif msg.content == "아니오":
                await ctx.send("정사각형 모양으로 만듭니다...")
                resultPath = self.generateCloud_core(ctx, msg_contents)
                await self.sendWCImagesAndRemove(ctx, resultPath)
            else:
                await ctx.send("취소 되었습니다.")
                return
        except:
            traceback.print_exc(file=sys.stdout)
            await ctx.send("타임아웃!")
            return
    
    def generateCloud_core(self, ctx, msgcontents, imgPath=""):
        string = (" ").join(msgcontents)
        mask = None
        image_colors = None

        if imgPath:
            mask = np.array(Image.open(imgPath))
            image_colors = ImageColorGenerator(mask)
        
        fontPath = "fonts/malgun.ttf"
        
        wordcloud = None

        if imgPath:
            wordcloud = WordCloud(
                font_path=fontPath,
                max_words=2000,
                background_color="white",
                mask=mask).generate(string)
        else:
            wordcloud = WordCloud(
                font_path=fontPath,
                width=1000,
                height=500,
                background_color="white",
                max_words=2000).generate(string)

        plt.figure(figsize=(15,8))
        if imgPath:
            plt.imshow(wordcloud.recolor(color_func=image_colors))
        else:
            plt.imshow(wordcloud)
        plt.axis("off")

        resultPath = ""
        if imgPath:
            resultPath = f"{imgPath}".replace(".png", "-wc.png")
        else:
            resultPath = f"db/{ctx.author.id}-wc.png"
        if imgPath:
            plt.savefig(resultPath, bbox_inches='tight')
        else:
            plt.savefig(resultPath, bbox_inches='tight')
        plt.close()

        return resultPath
    
    async def sendWCImagesAndRemove(self, ctx, resultPath):
        await ctx.send(file = discord.File(resultPath))
        try:
            os.remove(resultPath)
        except:
            pass
        try:
            os.remove(resultPath.replace("-wc", ""))
        except:
            pass



        

def setup(bot):
    bot.add_cog(WordCloud_(bot))