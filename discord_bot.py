import os
import discord
from dotenv import load_dotenv
from log_manager import log_info, log_error, log_warning

load_dotenv()

# Konfigurationsvariablen mit Fehlerbehandlung
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
CHANNEL_ID = None
NOTIFICATIONS_ENABLED = os.getenv('DISCORD_NOTIFICATIONS', 'false').lower() == 'true'

# Versuche Channel ID zu konvertieren
try:
    channel_id = os.getenv('DISCORD_CHANNEL_ID')
    if channel_id and channel_id != 'your_channel_id_here':
        CHANNEL_ID = int(channel_id)
except ValueError:
    log_error(f"Ungültige DISCORD_CHANNEL_ID: {channel_id}")

def is_enabled():
    """Überprüft, ob der Discord-Bot aktiviert und korrekt konfiguriert ist."""
    if not NOTIFICATIONS_ENABLED:
        return False
    if not DISCORD_TOKEN or DISCORD_TOKEN == 'your_discord_bot_token_here':
        return False
    if not CHANNEL_ID:
        return False
    return True

# Discord Client
client = discord.Client(intents=discord.Intents.default())

@client.event
async def on_ready():
    """Wird aufgerufen, wenn der Bot erfolgreich verbunden ist."""
    if CHANNEL_ID and NOTIFICATIONS_ENABLED:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send("🤖 Discord Bot ist online und bereit!")
            log_info("Discord Bot ist online und bereit!")
        else:
            log_error(f"Discord Kanal mit ID {CHANNEL_ID} wurde nicht gefunden!")
    else:
        log_warning("Discord Bot ist online, aber Benachrichtigungen sind deaktiviert oder Channel ID fehlt.")

async def send_notification(message: str):
    """Sendet eine Nachricht an den konfigurierten Discord-Kanal."""
    if not is_enabled():
        return False
    
    try:
        channel = client.get_channel(CHANNEL_ID)
        if channel:
            await channel.send(message)
            return True
        else:
            log_error(f"Discord Kanal mit ID {CHANNEL_ID} wurde nicht gefunden!")
            return False
    except Exception as e:
        log_error(f"Fehler beim Senden der Discord-Nachricht: {str(e)}")
        return False

def run_bot():
    """Startet den Discord Bot."""
    if not is_enabled():
        log_warning("Discord Bot ist deaktiviert oder nicht korrekt konfiguriert.")
        return
    
    if not DISCORD_TOKEN or DISCORD_TOKEN == 'your_discord_bot_token_here':
        log_error("Discord Token fehlt oder ist nicht konfiguriert!")
        return
        
    try:
        client.run(DISCORD_TOKEN)
    except Exception as e:
        log_error(f"Fehler beim Starten des Discord Bots: {str(e)}")

if __name__ == "__main__":
    run_bot() 