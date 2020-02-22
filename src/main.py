import discord
import package.settings as settings
import asyncio
import package.db as db
import package.dcinside as dcinside
from discord.ext import tasks

client = discord.Client(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print('logged in as {0.user}!'.format(client))

async def updateNameList(nameList, channel):
    for name in nameList:
        db.appendNameIfNotExists(name)
        res = dcinside.searchParse(name)
        for gall in res:
            await channel.send(f'{name}: {gall}')
            for post in res[gall]:
                embed = discord.Embed(title=post["name"], url=post["link"], description="{0}\n{1} 작성\n{2}".format(gall, name, post["date"]))
                await channel.send(embed=embed)
                await channel.send(file=discord.File(post["file"], filename="{0}.html".format(post["number"])))
                db.appendPost(name, gall, int(post["number"]))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith(settings.prefix):
        if message.author.id in settings.USERID:
            if message.content.startswith("{0}{1}".format(settings.prefix, "갤러리추가")):
                gallName = message.content.replace("{0}{1}".format(settings.prefix, "갤러리추가"), "").strip()
                id = dcinside.appendGallIdByName(gallName)
                if id is None:
                    await message.channel.send('등록 실패.')
                    return
                await message.channel.send('{0} 등록 완료.'.format(id))
            elif message.content.startswith("{0}{1}".format(settings.prefix, "파싱")):
                nameList = message.content.replace("{0}{1}".format(settings.prefix, "파싱"), "").strip().split(" ")
                await updateNameList(nameList, message.channel)
                await message.channel.send('파싱 끝났습니다.')
            else:
                await message.channel.send('잘못된 명령어입니다.')
        else:
            await message.channel.send('허가받은 사용자만 사용 가능합니다.')
            return

def run():
    client.loop.create_task(updateAllAuthors())
    client.run(settings.DISCORD_TOKEN)

async def updateAllAuthors():
    while True:
        channel = client.get_channel(settings.CHANNEL_ID)
        if channel is None:
            await asyncio.sleep(1)
            continue
        names = db.getNames()
        await updateNameList(names, channel)
        await asyncio.sleep(60)

if __name__ == "__main__":
    run()