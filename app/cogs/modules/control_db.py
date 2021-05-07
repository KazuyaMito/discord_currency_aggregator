import pymysql.cursors
from urllib.parse import urlparse
import os

url = urlparse(os.environ['DATABASE_URL'])
conn = pymysql.connect(
    host=url.hostname,
    user=url.username,
    password=url.password,
    db=url.path[1:],
    charset='utf8mb4',
    cursorclass=pymysql.cursors.DictCursor)


def get_user_use_count(user_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT use_count FROM users WHERE user_id = %s", user_id)
            result = cursor.fetchall()

            return result[0] if len(result) > 0 else None
    finally:
        cursor.close()


def add_user(user_id, mention_name, use_count):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO users (user_id, user_name, use_count) VALUES (%s, %s, %s)", (user_id, mention_name, use_count))
            conn.commit()

    finally:
        cursor.close()


def update_user_use_count(user_id, mention_name, use_count):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_id FROM users WHERE user_id = %s", (user_id, ))
            result = cursor.fetchall()

            if len(result) <= 0:
                cursor.execute("INSERT INTO users (user_id, user_name, use_count) VALUES (%s, %s, %s)", (user_id, mention_name, use_count))
                conn.commit()
            else:
                cursor.execute("UPDATE user SET use_count = %s WHERE user_id = %s", (user_id, use_count))
                conn.commit()
    finally:
        cursor.close()


def get_users():
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT user_name, use_count FROM users")
            return cursor.fetchall()
    finally:
        cursor.close()


def delete_all_users():
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("TRUNCATE TABLE users")
            conn.commit()
    finally:
        cursor.close()


def get_guild(guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT is_multi_line_read, is_name_read FROM guilds WHERE id = %s", (guild_id, ))
            result = cursor.fetchall()

            return result[0] if len(result) > 0 else None
    finally:
        cursor.close()


def add_guild(guild_id, name):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("INSERT INTO guilds (id, name) VALUES (%s, %s)", (guild_id, name))
            conn.commit()
    finally:
        cursor.close()


def set_read_name(readable, guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE guilds SET is_name_read = %s WHERE id = %s", (readable, guild_id))
            conn.commit()
    finally:
        cursor.close()


def set_read_multi_line(readable, guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("UPDATE guilds SET is_multi_line_read = %s WHERE id = %s", (readable, guild_id))
            conn.commit()
    finally:
        cursor.close()


def get_dictionary(word, guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM dictionaries WHERE word = %s AND guild_id = %s", (word, guild_id))
            result = cursor.fetchall()

            return result[0] if len(result) > 0 else None
    finally:
        cursor.close()


def get_dictionaries(guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT dictionaries.word, dictionaries.read FROM dictionaries WHERE dictionaries.guild_id = %s", (guild_id, ))
            result = cursor.fetchall()

            return result if len(result) > 0 else {}
    finally:
        cursor.close()


def add_dictionary(word, read, guild_id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT id FROM dictionaries WHERE word = %s", (word, ))
            result = cursor.fetchall()

            if len(result) > 0:
                cursor.execute("UPDATE dictionaries SET dictionaries.read = %s WHERE dictionaries.id = %s", (read, result[0]["id"]))
                conn.commit()
            else:
                cursor.execute("INSERT INTO dictionaries (dictionaries.word, dictionaries.read, dictionaries.guild_id) VALUES (%s, %s, %s)", (word, read, guild_id))
                conn.commit()
    finally:
        conn.close()


def delete_dictionary(id):
    conn.ping(reconnect=True)

    try:
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM dictionaries WHERE id = %s", (id, ))
            conn.commit()
    finally:
        cursor.close()