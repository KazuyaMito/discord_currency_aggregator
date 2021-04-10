from discord.ext import commands
import discord
import mysql.connector
from urllib.parse import urlparse
import os

bot = commands.Bot(command_prefix='%')
url = urlparse(os.environ['DATABASE_URL'])
conn = mysql.connector.connect(
    host = url.hostname,
    port = 3306,
    user = url.username,
    password = url.password,
    database = url.path[1:]
)


@bot.event
async def on_ready():
    conn.ping(reconnect=True)
    print(conn.is_connected())
    print('on_ready')


@bot.event
async def on_message(message):
    if message.author.bot:
        return
    conn.ping(reconnect=True)

    if message.content.startswith('!use ブースト'):
        cur = conn.cursor(buffered=True)
        user_id = message.author.id
        mention_name = message.author.name
        use_count = 0

        cur.execute("SELECT user_id, use_count FROM users WHERE user_id = %s", (user_id,))
        if cur.rowcount >= 1:
            for row in cur:
                use_count = row[1] + 1
        else:
            use_count += 1

        cur.execute("INSERT INTO users (user_id, user_name, use_count) VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE use_count = %s", (user_id, mention_name, use_count, use_count))
        conn.commit()

    await bot.process_commands(message)


@bot.command()
async def aggregate(ctx):
    conn.ping(reconnect=True)
    cur = conn.cursor()

    embed = discord.Embed(title="Aggregate Result", description="The result of counting the number of times the \"use\" command was used in MEE6.", color=0xff0000)
    cur.execute("SELECT user_name, use_count FROM users")
    for row in cur:
        embed.add_field(name=row[0], value=row[1], inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    conn.ping(reconnect=True)
    cur = conn.cursor()

    cur.execute("DELETE FROM users")
    conn.commit()
    embed = discord.Embed(title="Use Count Clear is Completed.")
    await ctx.send(embed=embed)


bot.run(os.environ['DISCORD_BOT_TOKEN'])