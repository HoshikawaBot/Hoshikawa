import discord
from settings import prefix

client = discord.client(command_prefix=prefix)

@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))

def run():
    client.run()