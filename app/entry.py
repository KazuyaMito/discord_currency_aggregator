from discord.ext import commands
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
    conn.ping(reconnect=True)
    cur = conn.cursor(buffered=True)

    if message.content.startswith('!use ブースト'):
        user_id = message.author.id
        use_count = 0

        cur.execute("SELECT user_id, use_count FROM users WHERE user_id = %s", (user_id,))
        if cur.rowcount >= 1:
            for row in cur:
                use_count = row[1] + 1
        else:
            use_count += 1

        cur.execute("INSERT INTO users (user_id, use_count) VALUES (%s, %s) ON DUPLICATE KEY UPDATE use_count = %s", (user_id, use_count, use_count))
        conn.commit()


bot.run("")