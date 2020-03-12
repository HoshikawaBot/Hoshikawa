import discord
import package.settings as settings
import asyncio
import package.db as db
import argparse
import sys

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
        return

def run():
    client.run(settings.DISCORD_TOKEN)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', help='exit after ready', action='store_true')
    parser.set_defaults(test=False)
    args = parser.parse_args()
    if args.test == True:
        sys.exit()
    run()