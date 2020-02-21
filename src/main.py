import discord
import package.settings as settings
import asyncio
import package.db as db
import package.dcinside as dcinside

client = discord.Client(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print('logged in as {0.user}!'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author.id in settings.USERID:
        if message.content.startswith("{0}{1}".format(settings.prefix, "갤러리추가")):
            gallName = message.content.replace("{0}{1}".format(settings.prefix, "갤러리추가"), "").strip()
            dcinside.appendGallIdByName(gallName)
            await message.channel.send('등록 완료.')
        if message.content.startswith("{0}{1}".format(settings.prefix, "파싱")):
            nameList = message.content.replace("{0}{1}".format(settings.prefix, "파싱"), "").strip().split(" ")
            for name in nameList:
                res = dcinside.searchParse(name)
                for gall in res:
                    await message.channel.send(f'{name}: {gall}')
                    for post in res[gall]:
                        embed = discord.Embed(title=post["name"], url=post["link"], description=post["date"])
                        await message.channel.send(embed=embed)
                        db.appendPost(name, gall, int(post["number"]))
            await message.channel.send('파싱 끝났습니다.')
    else:
        await message.channel.send('허가받은 사용자만 사용 가능합니다.')
        return

def run():
    client.run(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    run()