from discord.ext import commands
import os

bot = commands.Bot(command_prefix='&')

@bot.event
async def on_ready():
    bot.load_extension("cogs.aggregator")
    bot.load_extension("cogs.tts")


bot.run(os.environ['DISCORD_BOT_TOKEN'])
