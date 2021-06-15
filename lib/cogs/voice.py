from discord import PCMAudio, FFmpegOpusAudio, FFmpegPCMAudio, FFmpegAudio
from discord.ext.commands import Cog, command
from io import BytesIO
from discord.player import FFmpegPCMAudio
from gtts import gTTS

class MomoVoice(Cog):
    """comandos relacionados al chat de voz"""

    def __init__(self, bot):
        self.name = "voice"
        self.aliases = ["voz", "voice"]
        self.bot = bot
        self.connection = None


    @command()
    async def play(self, ctx, *, words="Hi"):
        """Se une a un chat de voz y pone musica"""
        if not self.connection:
            self.connection = await self.bot.get_channel(778978050926444548).connect()
            # mp3 = BytesIO()
        tts = gTTS(words, lang="en")
        with open("./data/audio.mp3", "wb") as mp3:
            tts.write_to_fp(mp3)
        self.connection.play(FFmpegOpusAudio("./data/audio.mp3"))


    @command()
    async def play2(self, ctx, *, words="Hi"):
        """Se une a un chat de voz y pone musica"""
        if not self.connection:
            self.connection = await self.bot.get_channel(778978050926444548).connect()
            mp3 = BytesIO()
            tts = gTTS(words, lang="en")
            tts.write_to_fp(mp3)
            self.connection.play(FFmpegOpusAudio(mp3))


    @command()
    async def leave(self, ctx):
        if self.connection:
            await self.connection.disconnect()
            self.connection = None
