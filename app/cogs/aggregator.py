import discord
from discord.ext import commands
from .modules import control_db

class Aggregator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
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

    @commands.command()
    async def aggregate(self, ctx):
        embed = discord.Embed(title="Aggregate Result", description="The result of counting the number of times the \"use\" command was used in MEE6.", color=0xff0000)
        users = control_db.get_users()
        for user in users:
            embed.add_field(name=user.user_name, value=user.use_count, inline=False)

        await ctx.send(embed=embed)

    @commands.command()
    async def clear(self, ctx):
        control_db.delete_all_users()
        embed = discord.Embed(title="Use Count Clear is Completed.")
        await ctx.send(embed=embed)

def setup(bot):
    return bot.add_cog(Aggregator(bot))