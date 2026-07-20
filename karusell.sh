#!/bin/bash

# OBS! Ved endring av denne fila må du etterpå også kjøre `chmod +x karusell.sh` og committe det!

LOG_FILE=~/Desktop/infoskjerm-karusell-ung/karusell.log

# Starter logging
echo "" | tee -a "$LOG_FILE"
echo "$(date +%Y-%m-%d_%H:%M:%S) - Starter opp karusell for infoskjerm" | tee -a "$LOG_FILE"

# Sjekker om internett er tilgjengelig
while true; do
    if ping -c 1 -q google.com &>/dev/null; then
        echo "Internett er tilgjengelig :party:" | tee -a "$LOG_FILE"
        break
    else
        echo "Ingen internett, prøver igjen om 20 sekunder" | tee -a "$LOG_FILE"
        sleep 20
    fi
done

# Oppdater rasberry pi
echo "$(date +%Y-%m-%d_%H:%M:%S) - Oppdaterer Raspberry Pi" | tee -a "$LOG_FILE"
sudo apt-get update >> "$LOG_FILE" 2>&1
sudo apt-get upgrade -y
sudo apt-get autoremove -y

# oppdater uv
uv self update >> "$LOG_FILE" 2>&1

# Starter infoskjerm-karusell-ung
sleep 5
lxterminal -t Karusellen -e 'sleep 2; cd ~/Desktop/infoskjerm-karusell-ung; git pull; sleep 2; 
uv sync; uv run python infoskjerm_karusell.py; exec bash' >> "$LOG_FILE" 2>&1