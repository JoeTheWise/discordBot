import discord
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# Import the os module.
import os
# Import load_dotenv function from dotenv module.
from dotenv import load_dotenv
# Loads the .env file that resides on the same level as the script.
load_dotenv()
# Grab the API token from the .env file.
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CLIENT_ID = os.getenv('SPOTIFY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIFY_CLIENT_SECRET')
# Create an instance of a Discord client.
intents = discord.Intents.all()
client = discord.Client(intents=intents)
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET))
results = spotify.artist("https://open.spotify.com/artist/0nmQIMXWTXfhgOBdNzhGOs?si=_plv8o58Tly8g8AkFP99-A")
print(results)
@client.event
async def on_ready():
    print(f'{client.user.name} has connected to Discord!')

@client.event
async def on_message(message):
    username = str(message.author)
    user_message = str(message.content)
    channel = str(message.channel)
    print(f'{username}: {user_message} ({channel})')
    if message.author == client.user:
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
            await message.channel.send("The client is not connected to a voice channel.")

    # if message.content.startswith('!play_song'):
        # song_title = user_message.split(" ",1)[1]
        # print(song_title)
        # try :
        #     server = message.guild
        #     voice_channel = server.voice_client
        #     filename = YouTube(song_title).streams.filter(only_audio=True).first().download()
        #     print(filename)
        #     voice_channel.play(discord.FFmpegPCMAudio(executable="/Users/txs3293/private_repos/discordclient/ffmpeg.exe", source=filename))
        #     await message.channel.send('**Now playing:** {}'.format(filename))
        # except:
        #     await message.channel.send("The client is not connected to a voice channel.")
client.run(DISCORD_TOKEN)
