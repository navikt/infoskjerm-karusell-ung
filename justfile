set shell := ["bash", "-eu", "-o", "pipefail", "-c"]

log_file := justfile_directory() + "/karusell.log"

# Vis tilgjengelige kommandoer
default:
    @just --list --unsorted

# Start hele infoskjermen
start: disable-screen-blanking wait-for-network update-repo sync open-temp-pages open-pages close-temp-pages carousel

# Start fra LXDE og behold terminalen åpen etter stopp eller feil
autostart:
    #!/usr/bin/env bash
    set +e
    just start
    status=$?
    if [ "$status" -ne 0 ]; then
        echo "Infoskjermen stoppet med feil (status $status)."
    else
        echo "Infoskjermen er stoppet."
    fi
    echo "Terminalen beholdes åpen for feilsøking."
    exec bash

# Deaktiver skjermsparer, DPMS og blanking for X11-sesjonen
disable-screen-blanking:
    #!/usr/bin/env bash
    set -euo pipefail
    if ! pgrep -x xscreensaver >/dev/null; then
        xscreensaver -no-splash >/dev/null 2>&1 &
    fi
    xset s off
    xset -dpms
    xset s noblank

# Vent til internett er tilgjengelig
wait-for-network:
    @while ! ping -c 1 -q google.com >/dev/null 2>&1; do \
        echo "Ingen internett, prøver igjen om 20 sekunder" | tee -a "{{ log_file }}"; \
        sleep 20; \
    done
    @echo "Internett er tilgjengelig" | tee -a "{{ log_file }}"

# Hent siste versjon uten å overskrive lokale endringer
update-repo:
    @echo "$(date +%Y-%m-%d_%H:%M:%S) - Oppdaterer repoet" | tee -a "{{ log_file }}"
    git pull --ff-only 2>&1 | tee -a "{{ log_file }}"

# Synkroniser Python-miljøet mot låsefila
sync:
    uv sync --locked 2>&1 | tee -a "{{ log_file }}"

# Opprett eller oppdater den dedikerte Firefox-profilen
setup-firefox:
    uv run python -m infoskjerm.setup_firefox

# Åpne midlertidig NAV-side for innlogging og redirect
open-temp-pages:
    uv run python -m infoskjerm.open_temp_pages

# Åpne alle konfigurerte nettsider
open-pages:
    uv run python -m infoskjerm.open_pages

# Lukk de kjente midlertidige fanene
close-temp-pages:
    uv run python -m infoskjerm.close_temp_pages

# Start fullskjerm og bytt kontinuerlig mellom fanene
carousel:
    uv run python -m infoskjerm.carousel

# Oppdater RPI-operativsystemet og uv manuelt
maintenance:
    sudo apt-get update
    sudo apt-get upgrade -y
    sudo apt-get autoremove -y
    uv self update

# Kjør lint og tester uten å starte nettleseren
check:
    uv run ruff check .
    uv run python -m pytest
