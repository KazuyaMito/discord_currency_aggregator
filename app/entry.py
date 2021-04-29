from discord.ext import commands
import discord
import os
import control_db

bot = commands.Bot(command_prefix='%')

@bot.event
async def on_ready():
    print('on_ready')


@bot.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith('!use ブースト'):
        user_id = message.author.id
        mention_name = message.author.name
        use_count = 0

        user = control_db.get_user(user_id)
        if user is None:
            use_count = 1
            control_db.add_user(user_id, mention_name, use_count)
        else:
            use_count = user.use_count + 1
            control_db.update_user_use_count(user, use_count)

    await bot.process_commands(message)


@bot.command()
async def aggregate(ctx):
    embed = discord.Embed(title="Aggregate Result", description="The result of counting the number of times the \"use\" command was used in MEE6.", color=0xff0000)
    users = control_db.get_users()
    for user in users:
        embed.add_field(name=user.user_name, value=user.use_count, inline=False)

    await ctx.send(embed=embed)


@bot.command()
async def clear(ctx):
    control_db.delete_all_users()
    embed = discord.Embed(title="Use Count Clear is Completed.")
    await ctx.send(embed=embed)


bot.run(os.environ['DISCORD_BOT_TOKEN'])