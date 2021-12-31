import discord, youtube_dl, youtube_search, validators
from discord.ext import commands

color = 0xAAA9AD

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.channel.send("Not in a voice Channel")
            return
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command()
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
    
    @commands.command()
    async def leave(self, ctx):
        await ctx.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *url):
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
        FFMPEG_OPTIONS = {"before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5", "options": "-vn"}
        YDL_OPTIONS = {"format": "bestaudio"}
        vc = ctx.voice_client
        url = " ".join(url)

        if not validators.url(url):
            video = youtube_search.YoutubeSearch(url, max_results=1).to_dict()[0]
            url = f"https://www.youtube.com/watch?v={video['id']}"
            videoData = {"title": video["title"], "views": video["views"], "duration": video["duration"], "thumbnail": video["thumbnails"][0]}
        else:
            video = youtube_search.YoutubeSearch(url, max_results=1).to_dict()[0]
            videoData = {"title": video["title"], "views": video["views"], "duration": video["duration"], "thumbnail": video["thumbnails"][0]}
        
        embed = discord.Embed(title=videoData["title"], color=color)

        for key in videoData.keys():
            if key == "thumbnail":
                embed.set_thumbnail(url=videoData[key])
            else:
                embed.add_field(name=key.capitalize(), value=videoData[key])

        await ctx.channel.send(embed=embed)

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info["formats"][0]["url"]
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def stop(self, ctx):
        ctx.voice_client.stop()

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
    
    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()


def setup(client):
    client.add_cog(music(client))
