import discord
from discord.ext import commands

# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
# Loads the .env file that resides on the same level as the script.
import youtube_dl
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
# Create an instance of a Discord client.
intents = discord.Intents.all()
client = discord.Client(intents=intents)
ytdl = youtube_dl.YoutubeDL(ytdl_format_options)
class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)
        self.data = data
        self.title = data.get('title')
        self.url = ""

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))
        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]
        filename = data['title'] if stream else ytdl.prepare_filename(data)
        return filename

@bot.event
async def on_ready():
    print(f'{bot.user.name} has connected to Discord!')

@bot.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    print(f'{username}: {user_message} ({channel})')
    if message.author == bot.user:
        return
    if message.content.startswith('!whatsup'):
        await message.channel.send('Greg Likes Men!')
    if message.content.startswith('!join'):
        if not message.author.voice:
            await message.channel.send("{} is not connected to a voice channel".format(ctx.message.author.name))
            return
        else:
            await message.author.voice.channel.connect()
    if message.content.startswith('!leave'):
        voice_client = message.guild.voice_client
        if voice_client.is_connected():
            await voice_client.disconnect()
        else:
            await message.channel.send("The bot is not connected to a voice channel.")

    if message.content.startswith('!play_song'):
        song_title = user_message.split(" ",1)[1]
        print(song_title)
        try :
            server = message.guild
            voice_channel = server.voice_client
            filename = YouTube(song_title).streams.filter(only_audio=True).first().download()
            print(filename)
            voice_channel.play(discord.FFmpegPCMAudio(executable="/Users/txs3293/private_repos/discordBot/ffmpeg.exe", source=filename))
            await message.channel.send('**Now playing:** {}'.format(filename))
        except:
            await message.channel.send("The bot is not connected to a voice channel.")
bot.run(DISCORD_TOKEN)
