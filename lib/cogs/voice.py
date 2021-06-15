from discord import PCMAudio, FFmpegOpusAudio, FFmpegPCMAudio, FFmpegAudio, PCMVolumeTransformer
from discord.ext.commands import Cog, command, errors
import asyncio
from io import BytesIO
from discord.ext.commands.core import is_owner
from discord.player import FFmpegPCMAudio
from gtts import gTTS
import os
import dotenv
import openai
import re
import youtube_dl
dotenv.load_dotenv("./.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------------------------------------------------------------


# Suppress noise about console usage from errors
youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(FFmpegPCMAudio(filename, **ffmpeg_options), data=data)


# ----------------------------------------------------------------------------
# https://github.com/Rapptz/discord.py/blob/master/examples/basic_voice.py






class MomoVoice(Cog):
    """comandos relacionados al chat de voz"""

    def __init__(self, bot):
        self.name = "voice"
        self.aliases = ["voz", "voice"]
        self.bot = bot
        self.connection = None
        self.conversation = ""
        self.max_convo_length = 120


    @command()
    async def join(self, ctx):
        """Se une al canal de voz donde está el usuario"""
        voice = ctx.author.voice
        if voice and voice.channel:
            if self.connection: 
                if self.connection.channel != voice.channel:
                    await self.connection.move_to(voice.channel)
            else:
                self.connection = await voice.channel.connect()
                self.connection.stop()
            return True
        else:
            if ctx.command.name != "momo":
                await ctx.send("Unite a un canal de voz primero!")
            return False


    @command(usage="<texto>")
    async def say(self, ctx, *, words=None):
        """Dice lo que escribas a través de voz"""
        if words is None:
            await ctx.send("Uso correcto: `say <texto>`")
            return
        if await self.join(ctx):
            tts = gTTS(words, lang="es")
            with open("./data/audio.mp3", "wb") as mp3:
                tts.write_to_fp(mp3)
            self.connection.play(FFmpegOpusAudio("./data/audio.mp3"))
            return True
        else:
            return False


    @command(usage="(<link>)", aliases=["p"])
    async def play(self, ctx, link=None):
        """Reproduce o despausa el contenido del link de Youtube en directo, sin predescargar"""
        if self.connection and self.connection.is_paused():
            self.connection.resume()
            return
        elif link is None:
            await ctx.send("Reproducí audio con `play <link>`")
            return
        if await self.join(ctx):
            async with ctx.typing():
                player = await YTDLSource.from_url(link, loop=self.bot.loop, stream=True)
                self.connection.play(player, after=lambda e: print(f'Error: {e}') if e else None)

            await ctx.send(f'Reproduciendo: {player.title}')


    @command(usage="<link>")
    async def stream(self, ctx, link=None):
        """Reproduce el contenido del link de Youtube luego de predescargar el audio (mayor calidad)"""
        if self.connection and self.connection.is_paused():
            self.connection.resume()
            return
        elif link is None:
            await ctx.send("Reproducí audio con `stream <link>`")
            return
        if await self.join(ctx):
            async with ctx.typing():
                song_there = os.path.isfile("song.mp3")
                try:
                    if song_there:
                        os.remove("./song.mp3")
                except PermissionError:
                    await ctx.send("Esperá a que termine este audio o frenalo con `stop`")
                    return

                # loading = await ctx.send("Cargando...")

                ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
                }
                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([link])
                for file in os.listdir("./"):
                    if file.endswith(".mp3"):
                        old_filename = file[:-16]
                        os.rename(file, "song.mp3")
                self.connection.play(FFmpegOpusAudio("./song.mp3"))
            await ctx.send(f'Reproduciendo: {old_filename}')
            return True
        else:
            return False


    @command()
    async def pause(self, ctx):
        """Frena la reproducción de audio temporalmente"""
        if self.connection:
            self.connection.pause()
            

    @command()
    async def stop(self, ctx):
        """Frena la reproducción de audio"""
        if self.connection:
            self.connection.stop()


    @command()
    @is_owner()
    async def momo(self, ctx, *, words=None):
        """Responde a lo que digas a través de voz o texto"""
        if words is not None:
            voice = ctx.author.voice
            async with ctx.typing():
                self.conversation += "\n" + words
                if len(self.conversation) > self.max_convo_length:
                    self.conversation = self.conversation[-self.max_convo_length:]
                response = openai.Completion.create(
                    engine="davinci",
                    prompt=self.conversation,
                    temperature=0.9,
                    max_tokens=len(words)*3 if len(words) <= 20 else 60,
                    top_p=1,
                    frequency_penalty=0.0,
                    presence_penalty=0.6,
                    
                )
                restext = response["choices"][0]["text"]
                self.conversation += "\n" + restext
                self.conversation = re.sub("\n+", "\n", self.conversation)
                if not await self.say(ctx, words=restext):
                    await ctx.send(restext)
        else:
            await ctx.send("Uso correcto: `momo <texto>`")


    """
    @command()
    async def play2(self, ctx, *, words="Hi"):
        \"""Se une a un chat de voz y pone musica\"""
        if not self.connection:
            self.connection = await self.bot.get_channel(778978050926444548).connect()
            mp3 = BytesIO()
            tts = gTTS(words, lang="en")
            tts.write_to_fp(mp3)
            self.connection.play(FFmpegOpusAudio(mp3))
    """

    @command()
    async def leave(self, ctx):
        """Sale del canal de voz"""
        if self.connection:
            await self.connection.disconnect()
            self.connection = None
