import discord
from discord.ext import commands
from . import control_db

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}
        self.text_channels = {}


    @commands.command()
    async def tts(self, ctx, *args):
        if len(args) == 0:
            embed = discord.Embed(title="Text To Speach", description="チャットの読み上げ機能が利用できます。", color=0x00bfff)
            embed.add_field(name="join", value="コマンドを実行したユーザーがいるボイスチャンネルにBotが入室します。\nボイスチャンネルが特定できない場合は、エラーになります。", inline=False)
            embed.add_field(name="end", value="読み上げを終了し、Botがボイスチャンネルから退出します。\n読み上げが開始されていない場合は、エラーになります。", inline=False)
            await ctx.send(embed=embed)
            return

        if args[0] == "join":
            await self.join(ctx)
        elif args[0] == "end":
            await self.end(ctx)


    async def join(self, ctx):
        guild_id = ctx.guild.id
        voice_channel = ctx.author.voice

        if guild_id in self.voice_channels:
            await self.voice_channels[guild_id].disconnect()
            del self.voice_channels[guild_id]
            del self.text_channels[guild_id]
        if not isinstance(voice_channel, type(None)):
            self.voice_channels[guild_id] = await voice_channel.channel.connect()
            self.text_channels[guild_id] = ctx.channel.id

            embed = discord.Embed(title="接続完了", description="読み上げを開始します。\n読み上げを終了したい場合は、 `&tts end` と入力してください。", color=0x00ff00)
            embed.add_field(name="読み上げ対象", value=ctx.channel.mention, inline=True)
            embed.add_field(name="読み上げボイスチャンネル", value=ctx.author.voice.channel.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="エラー", description="ボイスチャンネルに接続してからコマンドを実行してください", color=0xff0000)
            await ctx.send(embed=embed)


    async def end(self, ctx):
        guild_id = ctx.guild.id
        voice_channel = ctx.author.voice

        if not isinstance(voice_channel, type(None)):
            if guild_id in self.voice_channels:
                await self.voice_channels[guild_id].disconnect()
                embed = discord.Embed(title="読み上げ終了", description="読み上げを終了しました。")
                await ctx.send(embed=embed)
                del self.voice_channels[guild_id]
                del self.text_channels[guild_id]
            else:
                embed = discord.Embed(title="エラー", description="読み上げが開始されていません", color=0xff0000)
                await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="エラー", description="ボイスチャンネルに接続してからコマンドを実行してください", color=0xff0000)
            await ctx.send(embed=embed)


    def add_guild_db(self, guild):
        guild_id_str = str(guild.id)
        guild = control_db.get_guild(guild_id_str)

        if isinstance(guild, type(None)):
            control_db.add_guild(guild_id_str, guild.name)


def setup(bot):
    return bot.add_cog(TTS(bot))