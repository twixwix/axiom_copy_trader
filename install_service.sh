#!/bin/bash

# Farben für die Ausgabe
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Funktion zum Anzeigen von Nachrichten
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Prüfe, ob das Skript als Root ausgeführt wird
if [ "$EUID" -ne 0 ]; then
    print_error "Bitte führen Sie dieses Skript als Root aus (mit sudo)"
    exit 1
fi

# Hole den aktuellen Benutzer und das Verzeichnis
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

print_message "Installation des Axiom Trade Bot Services wird gestartet..."
print_message "Benutzer: $CURRENT_USER"
print_message "Verzeichnis: $CURRENT_DIR"

# Prüfe, ob Python installiert ist
if ! command -v python3 &> /dev/null; then
    print_warning "Python3 ist nicht installiert. Installiere Python3..."
    apt-get update
    apt-get install -y python3 python3-pip
fi

# Prüfe, ob pip installiert ist
if ! command -v pip3 &> /dev/null; then
    print_warning "pip3 ist nicht installiert. Installiere pip3..."
    apt-get install -y python3-pip
fi

# Installiere die Abhängigkeiten
print_message "Installiere Python-Abhängigkeiten..."
pip3 install -r "$CURRENT_DIR/requirements.txt"

# Erstelle Log-Verzeichnis
print_message "Erstelle Log-Verzeichnis..."
mkdir -p "$CURRENT_DIR/logs"
chown -R "$CURRENT_USER:$CURRENT_USER" "$CURRENT_DIR/logs"

# Ersetze Platzhalter in der Service-Datei
print_message "Konfiguriere den Service..."
sed -i "s|YOUR_USERNAME|$CURRENT_USER|g" "$CURRENT_DIR/axiom_trade_bot.service"
sed -i "s|/path/to/your/project|$CURRENT_DIR|g" "$CURRENT_DIR/axiom_trade_bot.service"

# Kopiere die Service-Datei in das systemd-Verzeichnis
print_message "Installiere den Service..."
cp "$CURRENT_DIR/axiom_trade_bot.service" /etc/systemd/system/

# Lade die systemd-Konfiguration neu
systemctl daemon-reload

# Aktiviere den Service, damit er beim Systemstart gestartet wird
systemctl enable axiom_trade_bot.service

# Starte den Service
print_message "Starte den Service..."
systemctl start axiom_trade_bot.service

# Prüfe den Status
if systemctl is-active --quiet axiom_trade_bot.service; then
    print_message "Service wurde erfolgreich gestartet!"
else
    print_error "Service konnte nicht gestartet werden. Bitte überprüfen Sie die Logs."
fi

print_message "Installation abgeschlossen!"
print_message "Status des Services:"
systemctl status axiom_trade_bot.service

print_message ""
print_message "Nützliche Befehle:"
print_message "  systemctl status axiom_trade_bot.service  # Status anzeigen"
print_message "  systemctl stop axiom_trade_bot.service    # Service stoppen"
print_message "  systemctl start axiom_trade_bot.service   # Service starten"
print_message "  systemctl restart axiom_trade_bot.service # Service neu starten"
print_message "  journalctl -u axiom_trade_bot.service     # System-Logs anzeigen"
print_message "  tail -f $CURRENT_DIR/logs/axiom_trade_bot.log  # Anwendungs-Logs anzeigen" 