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
        # Self Executing
        return
    if message.content.startswith(settings.prefix):
        # TODO

def run():
    client.loop.create_task(updateAllAuthors())
    client.run(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    run()