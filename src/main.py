import discord
import package.settings as settings
import asyncio
import package.db as db
import argparse
import sys
from discord.ext import commands

bot = commands.Bot(command_prefix=settings.prefix)

@bot.event
async def on_ready():
    print('logged in as {0.user}!'.format(bot))
    # if Test Mode
    if args.test == True:
        # Exit
        sys.exit()

def run():
    if not settings.DISCORD_TOKEN:
        print('no token!')
        return
    bot.load_extension("cogs.say")
    bot.load_extension("cogs.post")
    bot.run(settings.DISCORD_TOKEN)


if __name__ == "__main__":
    # Test Execution Handling Start
    parser = argparse.ArgumentParser()
    parser.add_argument('-test', help='exit after ready', action='store_true')
    parser.set_defaults(test=False)
    args = parser.parse_args()
    # Test Execution Handling End
    db.setup()
    run()