import os, requests, discord, music, tts
from discord.ext import commands

color = 0xAAA9AD
api_key = os.environ['api_key']
token = os.environ['token']
prefix = "."

bot = commands.Bot(command_prefix=prefix, case_insensitive=True)
bot.remove_command("help")

tts.setup(bot)
music.setup(bot)

@bot.event
async def on_ready():
    print("Logged in")


@bot.command()
async def test(ctx):
    await ctx.channel.send("Im Working")


@bot.command()
async def cat(ctx):
    r = requests.get("https://api.thecatapi.com/v1/images/search").json()
    await ctx.channel.send(r[0]["url"])


@bot.command()
async def show(ctx, query, amount="1"):
    max = 5

    try:
        amount = int(amount)
    except:
        await ctx.channel.send(f"{amount} is not a valid number!")
        return

    if amount > max:
        await ctx.channel.send(f"The maximum amount is {max}")
        return

    images = requests.get(
        f"https://serpapi.com/search.json?engine=google&q={query}&tbm=isch&api_key={api_key}"
    ).json()["images_results"]

    for x in range(0, amount):
        await ctx.channel.send(images[x]["original"])

@bot.command()
async def translate(ctx, targetLanguage, *, data):
    sourceLanguageRequest = requests.post(f"https://libretranslate.de/detect?q={data}")
    sourceLanguage = sourceLanguageRequest.json()[0]["language"]
    targetLanguage = targetLanguage.lower()
    translateJSON = requests.post(f"https://libretranslate.de/translate?q={data}&source={sourceLanguage}&target={targetLanguage}").json()
    if "error" in translateJSON.keys():
        await ctx.channel.send(f"```{targetLanguage} is not a valid Language!\nType {prefix}languages for a list of languages!```")
        return
    embed = discord.Embed(color=color, title=f"Translation from {sourceLanguage} to {targetLanguage}", description=f"{translateJSON['translatedText']}")
    await ctx.channel.send(embed=embed)

@bot.command()
async def languages(ctx):
    languagesList = requests.get("https://libretranslate.de/languages").json()
    embed = discord.Embed(color=color)
    for language in languagesList:
        embed.add_field(name=language["name"], value=f"Code: **{language['code']}**")
    await ctx.channel.send(embed=embed)

@bot.command()
async def source_code(ctx):
    await ctx.channel.send(f"```Github Repository (source code):```\nhttps://github.com/totensee/YavuzhanBot")

@bot.command()
async def github(ctx):
    await ctx.channel.send(f"```Github Repository (source code):```\nhttps://github.com/totensee/YavuzhanBot")

bot.run(token)