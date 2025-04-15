#!/bin/bash

# Prüfe, ob das Skript als Root ausgeführt wird
if [ "$EUID" -ne 0 ]; then
  echo "Bitte führen Sie dieses Skript als Root aus (mit sudo)"
  exit 1
fi

# Hole den aktuellen Benutzer
CURRENT_USER=$(whoami)
CURRENT_DIR=$(pwd)

# Ersetze Platzhalter in der Service-Datei
sed -i "s|YOUR_USERNAME|$CURRENT_USER|g" axiom_trade_bot.service
sed -i "s|/path/to/your/project|$CURRENT_DIR|g" axiom_trade_bot.service

# Kopiere die Service-Datei in das systemd-Verzeichnis
cp axiom_trade_bot.service /etc/systemd/system/

# Lade die systemd-Konfiguration neu
systemctl daemon-reload

# Aktiviere den Service, damit er beim Systemstart gestartet wird
systemctl enable axiom_trade_bot.service

# Starte den Service
systemctl start axiom_trade_bot.service

echo "Axiom Trade Bot Service wurde erfolgreich installiert und gestartet!"
echo "Status:"
systemctl status axiom_trade_bot.service

echo ""
echo "Nützliche Befehle:"
echo "  systemctl status axiom_trade_bot.service  # Status anzeigen"
echo "  systemctl stop axiom_trade_bot.service    # Service stoppen"
echo "  systemctl start axiom_trade_bot.service   # Service starten"
echo "  systemctl restart axiom_trade_bot.service # Service neu starten"
echo "  journalctl -u axiom_trade_bot.service     # Logs anzeigen" 