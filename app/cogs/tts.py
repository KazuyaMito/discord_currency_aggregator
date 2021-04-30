import discord
import re
import asyncio
import os
from discord.ext import commands
from .modules import control_db, jtalk

class TTS(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.voice_channels = {}
        self.text_channels = {}


    @commands.Cog.listener(name='on_message')
    async def on_message(self, message):
        if message.author.bot or isinstance(message.guild, type(None)) or message.content.startswith('&'):
            return

        guild_id = message.guild.id
        if message.channel.id == self.text_channels[guild_id]:
            get_msg  = re.sub(r'http(s)?://([\w-]+\.)+[\w-]+(/[-\w ./?%&=]*)?', 'URL省略', message.content)
            get_msg  = get_msg .replace('<:', '')
            get_msg  = re.sub(r':[0-9]*>', '', get_msg )

            mention_list = message.raw_mentions
            channel_list = message.raw_channel_mentions
            mention_dict = {}
            channel_dict = {}
            for ment in mention_list:
                if ment == message.author.id:
                    mention_dict['<@!{}>'.format(str(ment))] = message.guild.get_member(ment).name
                else:
                    mention_dict['<@{}>'.format(str(ment))] = message.guild.get_member(ment).name

            for cnls in channel_list:
                channel_dict['<#{}>'.format(str(cnls))] = message.guild.get_channel(cnls).name

            for me_key in mention_dict.keys():
                get_msg = get_msg.replace(me_key, mention_dict[me_key], 1)

            for ch_key in channel_dict.keys():
                get_msg = get_msg.replace(ch_key, channel_dict[ch_key], 1)

            words = control_db.get_dictionary(str(guild_id))
            for word in words:
                get_msg  = get_msg .replace(word.word, word.read)
            get_msg = get_msg.replace('<', '').replace('>', '')

            is_nameread = control_db.get_guild(str(guild_id)).is_name_read
            print(is_nameread)
            if is_nameread == True:
                get_msg = "{}、{}".format(message.author.display_name, get_msg)

            try:
                rawfile_name = jtalk.jtalk(get_msg)
            except:
                embed = discord.Embed(title="エラー", description="読み上げ時にエラーが発生しました。")
                await message.channel.send(embed=embed)

            rawfile_path = rawfile_name
            self.voice_channels[guild_id].play(discord.FFmpegPCMAudio(rawfile_path, options="-af \"volume=0.1\""))
            await asyncio.sleep(0.5)
            os.remove(rawfile_path)


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

        self.add_guild_db(ctx.guild)

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