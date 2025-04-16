import os
import logging
import time
from datetime import datetime, timedelta
from logging.handlers import RotatingFileHandler
import glob

# Logging-Konfiguration
LOG_DIR = "logs"
LOG_FILE = os.path.join(LOG_DIR, "axiom_trade_bot.log")
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5
LOG_RETENTION_DAYS = 7  # Logs älter als 7 Tage werden gelöscht

def setup_logging():
    """Richtet das Logging-System ein."""
    # Erstelle Log-Verzeichnis, falls es nicht existiert
    if not os.path.exists(LOG_DIR):
        os.makedirs(LOG_DIR)
    
    # Konfiguriere den Logger
    logger = logging.getLogger("axiom_trade_bot")
    logger.setLevel(logging.INFO)
    
    # Formatiere die Log-Nachrichten
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # Datei-Handler mit Rotation
    file_handler = RotatingFileHandler(
        LOG_FILE, 
        maxBytes=MAX_LOG_SIZE, 
        backupCount=BACKUP_COUNT
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    # Konsolen-Handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    return logger

def cleanup_old_logs():
    """Bereinigt alte Log-Dateien."""
    try:
        # Finde alle Log-Dateien
        log_files = glob.glob(os.path.join(LOG_DIR, "*.log*"))
        
        # Aktuelles Datum
        now = datetime.now()
        
        # Prüfe jede Log-Datei
        for log_file in log_files:
            # Hole das Erstellungsdatum der Datei
            file_time = datetime.fromtimestamp(os.path.getctime(log_file))
            
            # Berechne das Alter in Tagen
            age_days = (now - file_time).days
            
            # Lösche Dateien, die älter als LOG_RETENTION_DAYS sind
            if age_days > LOG_RETENTION_DAYS:
                os.remove(log_file)
                print(f"Alte Log-Datei gelöscht: {log_file}")
    except Exception as e:
        print(f"Fehler beim Bereinigen der Log-Dateien: {e}")

# Erstelle den Logger
logger = setup_logging()

# Bereinige alte Logs beim Start
cleanup_old_logs()

# Funktion zum Loggen von Nachrichten
def log_info(message):
    """Loggt eine Info-Nachricht."""
    logger.info(message)

def log_error(message):
    """Loggt eine Fehlermeldung."""
    logger.error(message)

def log_warning(message):
    """Loggt eine Warnung."""
    logger.warning(message)

def log_debug(message):
    """Loggt eine Debug-Nachricht."""
    logger.debug(message) 