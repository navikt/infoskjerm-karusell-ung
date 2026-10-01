# Hva må gjøres på Raspberry Pien?

1. Koble til wifi 'infoskjerm' eller 'NAV-infoskjerm'
    - passord for dette mm. i Google Secret Manager
    - 'infoskjerm' gir også tilgang til grafana, men wifi-kortet til Rpien må whitelistes
        - skriv `ifconfig` i terminalen og send det etter "ether" under "wlan0" til Trond Aker (#tech-nettverk)
2. Kontroller skrivebordsmiljøet med `echo $XDG_CURRENT_DESKTOP`.
    - På dagens infoskjerm gir kommandoen `LXDE`. Det betyr at RPI-en bruker X11,
      som karusellen trenger fordi `pyautogui` ikke støtter Wayland.
3. Installer `git`, `just` og X11-verktøyene som holder skjermen våken:
    ```bash
    sudo apt update
    sudo apt install git just xscreensaver x11-xserver-utils
    ```
4. Installer `uv`:
    ```bash
    curl -LsSf https://astral.sh/uv/install.sh | sh
    ```
    Start terminalen på nytt dersom `uv` ikke blir funnet med én gang.
5. Klon repoet til skrivebordet og velg konfigurasjonen for denne skjermen:
    ```bash
    cd ~/Desktop
    git clone https://github.com/navikt/infoskjerm-karusell-ung.git
    cd infoskjerm-karusell-ung
    echo ung > INFOSKJERM_ID
    just sync
    ```
    Kopier aliasene til RPI-brukerens hjemmemappe og last dem inn:
    ```bash
    cp .bash_aliases ~/.bash_aliases
    source ~/.bash_aliases
    ```
    Dette gjør blant annet kommandoen `karusell` tilgjengelig, slik at
    `just start` kan kjøres fra hvilken som helst mappe. `cp` overskriver en
    eventuell eksisterende `~/.bash_aliases`; slå sammen filene manuelt dersom
    RPI-brukeren allerede har egne aliaser.
6. Opprett en egen, persistent Firefox-profil:
    ```bash
    just setup-firefox
    just open-temp-pages
    ```
    - Logg inn på AD-brukeren 'srvdevinfoskjerm111@nav.no' i Firefox-vinduet.
    - Kontroller for eksempel innloggingen på
      https://data.ansatt.nav.no/quarto/0b700511-f50c-4059-b519-32fb19637bae
    - Profilen ligger i `~/.mozilla/firefox/infoskjerm` og skal ikke sjekkes
      inn i Git. Den beholder cookies, men NAV kan fortsatt kreve ny innlogging
      når Azure AD-sesjonen utløper.
    - Lukk Firefox på vanlig måte etter at innloggingen er kontrollert.
7. Test hele oppstarten:
    ```bash
    just start
    ```
    Kontroller at riktige faner åpnes, at `about:sessionrestore` ikke vises,
    at skjermen ikke blankes, og at `Ctrl+C` stopper karusellen. Ved feil
    finnes detaljer i `karusell.log`. Skjermspareroppsettet kan testes separat
    med `just disable-screen-blanking`.
8. Skru av screen blanking med `sudo raspi-config` under "Display Options".
9. Sett opp autostart som brukeren som skal vise infoskjermen:
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
      Exec=lxterminal --title=Infoskjerm --working-directory=/home/pi/Desktop/infoskjerm-karusell-ung --command="just autostart"
      Terminal=false
      ```
      LXDE leser `.desktop`-filer fra `~/.config/autostart` når brukeren logger
      inn. Dette er ikke avhengig av om session-navnet er `LXDE` eller `LXDE-pi`.
      Fila er brukerspesifikk, så ikke bruk `sudo` når den opprettes. Kommandoen
      starter en terminal og beholder den åpen dersom oppstarten feiler.
10. Gjør autostart-fila kjørbar:
    ```bash
    chmod +x ~/.config/autostart/infoskjerm.desktop
    ```
11. `sudo reboot`
12. Sett opp daglig reboot av RPIen:
    - `sudo crontab -e` og legg til linjen:
    ```bash
    0 6 * * * /sbin/reboot
    ```
13. Kjør vedlikehold manuelt ved behov:
    ```bash
    cd ~/Desktop/infoskjerm-karusell-ung
    just maintenance
    ```
    OS- og `uv`-oppdateringer kjøres ikke under automatisk oppstart, slik at
    skjermen ikke blir stående og vente på `sudo` eller en pakkeoppdatering.
14. Dersom et grafanadasbord skal vises:
    - se https://docs.nais.io/observability/metrics/how-to/grafana-from-infoscreen
    - last ned Modify Header Value browser extension i Firefox (tror ikke det funker i chromium)
    - hent token (Bearer) fra GoogleSecretManager
    - se RPI "pensjonskalkulator" hvis det ikke funker

Husk å zoome i Firefox til passe størrelse. Innstillingen lagres i den
dedikerte profilen.

Hvis `echo $XDG_CURRENT_DESKTOP` viser `labwc` i stedet for `LXDE`, er RPI-en
byttet til Wayland. Da må autostart legges i `~/.config/labwc/autostart`, og
karusellens bruk av `pyautogui` må tilpasses før oppsettet kan brukes.

Gammel guide med mer tekst tilgjenglig i canvaset i kanalen `#infoskjerm` på slack
