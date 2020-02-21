import discord
import package.settings as settings
import asyncio
import package.db as db

client = discord.Client(command_prefix=settings.prefix)

@client.event
async def on_ready():
    print('logged in as {0.user}!'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.author in settings.USERID:
        if message.content.startswith("{0}{1}".format(settings.prefix, "갤러리추가")):
            IdList = message.content.replace("{0}{1}".format(settings.prefix, "갤러리추가"), "").split(" ")
            for id in IdList:
                db.appendGallIdList(id)
            await message.channel.send('등록 완료.')
    else:
        await message.channel.send('허가받은 사용자만 사용 가능합니다.')
        return

def run():
    client.run(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    run()