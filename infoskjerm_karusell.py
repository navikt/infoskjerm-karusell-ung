import sys
import yaml
import time
import logging
import pyautogui
import webbrowser

pyautogui.FAILSAFE = False  # pyautogui stopper ikke pga musepeker i hjørnet
logging.basicConfig(
    filename="karusell.log", level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)
logging.info("Kjører infoskjerm_karusell.py")

try:  # hent valgt config fra fila INFOSKJERM_ID
    with open("INFOSKJERM_ID", "r") as f:
        infoskjerm_id = f.read().strip()
        logging.info(f"Valgt konfigurasjon: {infoskjerm_id}")
except FileNotFoundError:
    logging.error("Filen INFOSKJERM_ID ble ikke funnet. Bruker standardkonfigurasjon")
    infoskjerm_id = "standard"
try:  # last inn konfigurasjon fra YAML-fil
    with open("nettsider.yaml", "r") as f:
        yamlconfig = yaml.safe_load(f)
        yamlconfig = yamlconfig["infoskjermer"]
except FileNotFoundError:
    logging.error("Filen nettsider.yaml ble ikke funnet. Avslutter karusellen")
    sys.exit(1)

# sjekk om infoskjerm_id finnes i YAML-fila
if infoskjerm_id not in yamlconfig:
    logging.error(
        f"Konfigurasjon '{infoskjerm_id}' finnes ikke i nettsider.yaml. Avslutter karusellen"
    )
    sys.exit(1)

# hent nettsider, fanetid, browser, vis_standardnettsider. format:
# standard
standard_browser = yamlconfig["standard"]["browser"]
standard_fanetid = yamlconfig["standard"]["fanetid"]
standard_vis_standardnettsider = yamlconfig["standard"]["vis_standardnettsider"]
standard_nettsider = yamlconfig["standard"]["nettsider"]

# hent konfigurasjon for valgt infoskjerm
browser = yamlconfig[infoskjerm_id].get("browser", standard_browser)
fanetid = yamlconfig[infoskjerm_id].get("fanetid", standard_fanetid)
vis_standardnettsider = yamlconfig[infoskjerm_id].get(
    "vis_standardnettsider", standard_vis_standardnettsider
)
nettsider = yamlconfig[infoskjerm_id].get("nettsider", [])

if vis_standardnettsider:
    nettsider = standard_nettsider + nettsider

# skiller mellom ctrl og command på unix og mac
ctrl = "ctrl" if infoskjerm_id != "lokalmac" else "command"


# to midlertidige faner
#   - google.com for å slippe meldingen "vil du gjenåpne faner"
#   - en innlogget nav-side som lukkes etter litt. Det løser redirect ved AD-innlogging
webbrowser.get(browser).open("https://www.google.com")
time.sleep(1)
webbrowser.get(browser).open(
    "https://data.ansatt.nav.no/quarto/0b700511-f50c-4059-b519-32fb19637bae/bemanning.html"
)
time.sleep(2)
pyautogui.hotkey(ctrl, "w")
time.sleep(2)
pyautogui.hotkey(ctrl, "w")
time.sleep(2)
pyautogui.hotkey(ctrl, "w")
time.sleep(2)

# åpne alle faner. RPIen trenger litt tid til å åpne hver fane riktig
for fane in nettsider:
    webbrowser.get(browser).open(fane)
    time.sleep(30)
logging.info("Åpnet alle faner")
if infoskjerm_id != "lokalmac":
    pyautogui.hotkey("f11")  # f11 er ikke fullskjerm på mac


loop = 0
try:
    while True:
        pyautogui.hotkey(ctrl, "pgdn")
        time.sleep(fanetid)
        loop += 1
        if loop % 100 == 0 and loop > 0:
            logging.info(f"Karusellen har rullet {loop} ganger")
except KeyboardInterrupt:
    logging.info("Karusellen ble avbrutt manuelt")
except Exception as e:  # noqa: BLE001
    logging.error(f"En feil oppstod {e}")
finally:
    logging.info("Avslutter karusellen")
