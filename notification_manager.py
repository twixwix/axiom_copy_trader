import asyncio
from discord_bot import send_notification as discord_send_notification, is_enabled as discord_is_enabled
from telegram_bot import send_notification as telegram_send_notification, is_enabled as telegram_is_enabled, initialize_bot as initialize_telegram_bot

async def initialize():
    """Initialisiert alle Benachrichtigungsdienste."""
    # Initialisiere Telegram Bot
    telegram_initialized = await initialize_telegram_bot()
    
    # Prüfe, ob mindestens ein Dienst aktiviert ist
    discord_enabled = discord_is_enabled()
    
    if not discord_enabled and not telegram_initialized:
        print("Warnung: Keine Benachrichtigungsdienste sind aktiviert!")
        print("Bitte aktivieren Sie mindestens einen Dienst in der .env Datei.")
        print("  - DISCORD_NOTIFICATIONS=true")
        print("  - TELEGRAM_NOTIFICATIONS=true")
    else:
        if discord_enabled:
            print("Discord Benachrichtigungen sind aktiviert.")
        if telegram_initialized:
            print("Telegram Benachrichtigungen sind aktiviert.")

async def send_notification(message):
    """Sendet eine Benachrichtigung an alle aktivierten Dienste."""
    tasks = []
    
    # Sende an Discord, wenn aktiviert
    if discord_is_enabled():
        tasks.append(discord_send_notification(message))
    
    # Sende an Telegram, wenn aktiviert
    if telegram_is_enabled():
        tasks.append(telegram_send_notification(message))
    
    # Führe alle Aufgaben parallel aus
    if tasks:
        await asyncio.gather(*tasks) 