import discord, gtts
from discord.ext import commands

class TtsCommands(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def tts(self, ctx, *, text):
        if ctx.author.voice is None:
            await ctx.channel.send("Not in a voice Channel")
            return
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)
        if ctx.voice_client.is_playing():
            ctx.voice_client.stop()

        language = "en"
        tts = gtts.gTTS(text=text, lang=language)
        tts.save("tts/tts.mp3")

        vc = ctx.voice_client
        audio_source = discord.FFmpegPCMAudio("tts/tts.mp3")
        vc.play(audio_source, after=None)

def setup(client):
    client.add_cog(TtsCommands(client))