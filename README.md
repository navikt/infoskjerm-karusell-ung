## Hva er greia?

- En Raspberry Pi er koblet til en TV, og rullerer mellom ulike nettsider
- Alt skal funke automatisk ved oppstart og oppdateres minst en gang i døgnet

## Hvordan legge til flere nettsider?

Det er mulig å legge til flere nettsider i rotasjonslisten til en RPi på følgende måte:

- Legg til ny url i `nettsider.yaml` i dette github-repoet
- Restart RPi-en, så blir endringene hentet fra github.com
- Hver RPi har en egen id for å skille dem fra hverandre (fila `INFOSKJERM_ID`)
- Alle åpne nettsider kan vises, samt Metabase, Grafana og datafortellinger

## Kommandoer

Repoet bruker [`just`](https://just.systems/) til oppstart og vedlikehold.
Kjør `just` eller `just --list` for å se alle kommandoene.

| Kommando | Hva den gjør |
| --- | --- |
| `just start` | Kjører hele oppstarten og starter fanerotasjonen |
| `just wait-for-network` | Venter til RPI-en har internett |
| `just update-repo` | Henter siste commit med fast-forward-only |
| `just sync` | Synkroniserer Python-miljøet mot `uv.lock` |
| `just setup-firefox` | Oppretter/oppdaterer den dedikerte Firefox-profilen |
| `just open-temp-pages` | Åpner NAV-siden som etablerer innlogget sesjon |
| `just open-pages` | Åpner nettsidene fra `nettsider.yaml` |
| `just close-temp-pages` | Lukker den midlertidige NAV-fanen |
| `just carousel` | Går i fullskjerm og bytter mellom åpne faner |
| `just maintenance` | Oppdaterer Raspberry Pi OS og `uv` manuelt |
| `just check` | Kjører lint og tester uten å åpne en nettleser |

`just start` stopper dersom Git-oppdateringen, miljøsynkroniseringen eller
konfigurasjonen feiler. Ved automatisk oppstart brukes `just autostart`, som
beholder terminalen åpen slik at feilen er synlig.

## Hvordan oppstarten henger sammen

`just start` utfører disse stegene i rekkefølge:

1. Vent på internett.
2. Kjør `git pull --ff-only`.
3. Synkroniser avhengigheter fra den inncheckede låsefila.
4. Start den dedikerte nettleserprofilen med en midlertidig NAV-side.
5. Åpne de konfigurerte nettsidene.
6. Lukk den midlertidige fanen.
7. Gå i fullskjerm og roter faner til prosessen stoppes med `Ctrl+C`.

OS-oppdateringer er med vilje ikke en del av vanlig oppstart. Kjør
`just maintenance` eksplisitt når RPI-en skal vedlikeholdes.

Python-koden ligger i `infoskjerm/`. Konfigurasjonslesing, nettleseroppstart,
sideåpning og fanerotasjon er skilt slik at hvert steg kan feilsøkes separat.
Driftsloggen skrives til `karusell.log`.

Hvis du er usikker, så bare snakk med Brynjar
