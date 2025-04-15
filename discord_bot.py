import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import asyncio
from datetime import datetime

# Lade Umgebungsvariablen
load_dotenv()

# Bot Konfiguration
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = int(os.getenv('DISCORD_CHANNEL_ID', '0'))  # Channel ID für Benachrichtigungen

# Bot Setup
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'{bot.user} ist online und bereit!')
    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("🤖 Bot ist online und überwacht die Aktivitäten!")

async def send_notification(message):
    """Sendet eine Benachrichtigung an den konfigurierten Discord Channel."""
    if CHANNEL_ID:
        channel = bot.get_channel(CHANNEL_ID)
        if channel:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            embed = discord.Embed(
                title="🔔 Aktivitätsbenachrichtigung",
                description=message,
                color=discord.Color.blue(),
                timestamp=datetime.now()
            )
            await channel.send(embed=embed)

def run_bot():
    """Startet den Discord Bot."""
    if not DISCORD_TOKEN:
        print("Fehler: DISCORD_TOKEN nicht gefunden in .env Datei!")
        return
    
    bot.run(DISCORD_TOKEN)

if __name__ == "__main__":
    run_bot() 