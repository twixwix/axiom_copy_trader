import os
import asyncio
from dotenv import load_dotenv
from telegram import Bot
from telegram.error import TelegramError
from datetime import datetime

# Lade Umgebungsvariablen
load_dotenv()

# Bot Konfiguration
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
NOTIFICATION_ENABLED = os.getenv('TELEGRAM_NOTIFICATIONS', 'false').lower() == 'true'

# Bot-Instanz
bot = None

async def initialize_bot():
    """Initialisiert den Telegram Bot."""
    global bot
    if TELEGRAM_TOKEN and TELEGRAM_CHAT_ID and NOTIFICATION_ENABLED:
        try:
            bot = Bot(token=TELEGRAM_TOKEN)
            # Teste die Verbindung
            await bot.get_me()
            print("Telegram Bot erfolgreich initialisiert!")
            return True
        except TelegramError as e:
            print(f"Fehler beim Initialisieren des Telegram Bots: {e}")
            return False
    return False

async def send_notification(message):
    """Sendet eine Benachrichtigung an den konfigurierten Telegram Chat."""
    if not bot or not TELEGRAM_CHAT_ID or not NOTIFICATION_ENABLED:
        return
    
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_message = f"🔔 *Aktivitätsbenachrichtigung*\n\n{message}\n\n_{timestamp}_"
        
        await bot.send_message(
            chat_id=TELEGRAM_CHAT_ID,
            text=formatted_message,
            parse_mode='Markdown'
        )
    except TelegramError as e:
        print(f"Fehler beim Senden der Telegram-Benachrichtigung: {e}")

def is_enabled():
    """Prüft, ob Telegram-Benachrichtigungen aktiviert sind."""
    return NOTIFICATION_ENABLED and TELEGRAM_TOKEN and TELEGRAM_CHAT_ID 