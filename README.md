## Hva er greia?

- En Raspberry Pi er koblet til en TV, og rullerer mellom ulike nettsider
- Alt skal funke automatisk ved oppstart og oppdateres minst en gang i døgnet


## Hvordan legge til flere nettsider?

Det er mulig å legge til flere nettsider i rotasjonslisten til en RPi på følgende måte:

- Legg til ny url i `nettsider.yaml` i dette github-repoet
- Restart RPi-en, så blir endringene hentet fra github.com
- Hver RPi har en egen id for å skille dem fra hverandre (fila `INFOSKJERM_ID`)
- Alle åpne nettsider kan vises, samt Metabase, Grafana og datafortellinger


Hvis du er usikker, så bare snakk med Brynjar
