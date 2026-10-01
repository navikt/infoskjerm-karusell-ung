# Hva må gjøres på Raspberry Pien?

1. Koble til wifi 'infoskjerm' eller 'NAV-infoskjerm'
    - passord for dette mm. i Google Secret Manager
    - 'infoskjerm' gir også tilgang til grafana, men wifi-kortet til Rpien må whitelistes
        - skriv `ifconfig` i terminalen og send det etter "ether" under "wlan0" til Trond Aker (#tech-nettverk)
2. Kontroller skrivebordsmiljøet med `echo $XDG_CURRENT_DESKTOP`.
    - På dagens infoskjerm gir kommandoen `LXDE`. Det betyr at RPI-en bruker X11,
      som karusellen trenger fordi `pyautogui` ikke støtter Wayland.
    - Ikke bruk den gamle autostart-fila
      `/etc/xdg/lxsession/LXDE-pi/autostart`. Nyere OS-oppdateringer kan endre
      hvilken LXDE-session som brukes, slik at denne fila ikke blir lest.
3. `curl -LsSf https://astral.sh/uv/install.sh | sh` for å installere uv
4. `sudo raspi-config` og skru av "screen blanking" under "display settings"
5. Logg inn på AD-brukeren 'srvdevinfoskjerm111@nav.no'
    - Logg feks inn på: https://data.ansatt.nav.no/quarto/0b700511-f50c-4059-b519-32fb19637bae
6. `git clone http://github.com/navikt/infoskjerm-karusell-ung.git`
7. Sett opp autostart som brukeren som skal vise infoskjermen:
    - Finn brukerens hjemmemappe med `echo $HOME`, for eksempel `/home/pi`.
    - Opprett den standardiserte XDG-autostartmappa:
      ```bash
      mkdir -p ~/.config/autostart
      ```
    - Opprett en autostart-oppføring:
      ```bash
      nano ~/.config/autostart/infoskjerm.desktop
      ```
    - Legg inn dette, men erstatt `/home/pi` med resultatet fra `echo $HOME`:
      ```ini
      [Desktop Entry]
      Type=Application
      Name=Infoskjerm-karusell
      Exec=lxterminal -t fra_autostart -e /home/pi/Desktop/infoskjerm-karusell-ung/karusell.sh
      Terminal=false
      ```
      LXDE leser `.desktop`-filer fra `~/.config/autostart` når brukeren logger
      inn. Dette er ikke avhengig av om session-navnet er `LXDE` eller `LXDE-pi`.
      Fila er brukerspesifikk, så ikke bruk `sudo` når den opprettes.
8. Kontroller at skriptet er kjørbart:
    ```bash
    chmod +x ~/Desktop/infoskjerm-karusell-ung/karusell.sh
    chmod +x ~/.config/autostart/infoskjerm.desktop
    ```
9. `sudo reboot`
10. Sett opp daglig reboot av RPIen, med logg av rebooten:
    - `sudo crontab -e` og legg til linjen:
    ```bash
    0 6 * * * sudo reboot && echo "$(date) - Planlagt omstart av RPI med cron" >> /var/log/reboot.log
    ```
11. Dersom et grafanadasbord skal vises:
    - se https://docs.nais.io/observability/metrics/how-to/grafana-from-infoscreen
    - last ned Modify Header Value browser extension i Firefox (tror ikke det funker i chromium)
    - hent token (Bearer) fra GoogleSecretManager
    - se RPI "pensjonskalkulator" hvis det ikke funker

Husk å zoome i nettleseren til passe størrelse. Det blir laget ved reboot.

Hvis `echo $XDG_CURRENT_DESKTOP` viser `labwc` i stedet for `LXDE`, er RPI-en
byttet til Wayland. Da må autostart legges i `~/.config/labwc/autostart`, og
karusellens bruk av `pyautogui` må tilpasses før oppsettet kan brukes.


Gammel guide med mer tekst tilgjenglig i canvaset i kanalen `#infoskjerm` på slack
