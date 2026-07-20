# Hva må gjøres på Raspberry Pien?

1. Koble til wifi 'infoskjerm' eller 'NAV-infoskjerm'
    - passord for dette mm. i Google Secret Manager
    - 'infoskjerm' gir også tilgang til grafana, men wifi-kortet til Rpien må whitelistes
        - skriv `ifconfig` i terminalen og send det etter "ether" under "wlan0" til Trond Aker (#tech-nettverk)
2. Pass på at RPIen bruker X11 og ikke Wayland
    - `sudo raspi-config` og velg "Advanced Options" -> "Wayland" -> velg X11, så reboot
3. `sudo apt-get install xscreensaver`
4. `curl -LsSf https://astral.sh/uv/install.sh | sh` for å installere uv
4. `sudo raspi-config` og skru av "screen blanking" under "display settings"
5. Logg inn på AD-brukeren 'srvdevinfoskjerm111@nav.no'
    - Logg feks inn på: https://data.ansatt.nav.no/quarto/0b700511-f50c-4059-b519-32fb19637bae
6. `git clone http://github.com/navikt/infoskjerm-karusell-ung.git`
10. `sudo nano /etc/xdg/lxsession/LXDE-pi/autostart` og legg til følgende linjer:
    ````bash
    ... # to linjer som allerede er der

    # skrur av skjermsparer og flytter vekk muspekeren
    @xscreensaver -no-splash
    @xset s off
    @xset -dpms
    @xset s noblank

    # starter bash-script i infoskjerm-karusell-ung
    @lxterminal -t fra_autostart -e ~/Desktop/infoskjerm-karusell-ung/karusell.sh
    ````
11. `sudo reboot`
12. Sett opp daglig reboot av RPIen, med logg av rebooten:
    - `sudo crontab -e` og legg til linjen:
    ```
    0 6 * * * sudo reboot && echo "$(date) - Planlagt omstart av RPI med cron" >> /var/log/reboot.log
    ```
13. Dersom et grafanadasbord skal vises:
    - se https://docs.nais.io/observability/metrics/how-to/grafana-from-infoscreen
    - last ned Modify Header Value browser extension i Firefox (tror ikke det funker i chromium)
    - hent token (Bearer) fra GoogleSecretManager
    - se RPI "pensjonskalkulator" hvis det ikke funker
Husk å zoome i nettleseren til passe størrelse. Det blir laget ved reboot.


Gammel guide med mer tekst tilgjenglig i canvaset i kanalen `#infoskjerm` på slack
