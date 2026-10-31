import discord
import requests
from discord.ext import commands, tasks

TOKEN = "PUT_YOUR_BOT_TOKEN_HERE"
CHANNEL_ID = 123456789012345678

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

last_games = []

@bot.event
async def on_ready():
    print(f"Bot connected: {bot.user}")
    check_games.start()

@tasks.loop(hours=1)
async def check_games():
    url = "https://store-site-backend-static.ak.epicgames.com/freeGamesPromotions"
    data = requests.get(url).json()

    games = data["data"]["Catalog"]["searchStore"]["elements"]
    channel = bot.get_channel(CHANNEL_ID)

    for game in games:
        if not game.get("promotions"):
            continue

        title = game["title"]

        if title in last_games:
            continue

        last_games.append(title)

        embed = discord.Embed(
            title="🎮 FREE GAME ON EPIC GAMES!",
            description=f"**{title}**\n\nClaim it free on Epic Games!",
            color=0x00FF00
        )

        embed.url = "https://store.epicgames.com/free-games"

        await channel.send(embed=embed)

bot.run(TOKEN)
