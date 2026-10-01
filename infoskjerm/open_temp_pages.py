import time

from infoskjerm.browser import ensure_browser_ready, open_url
from infoskjerm.config import load_config
from infoskjerm.logging_config import get_logger

NAV_BOOTSTRAP_URL = (
    "https://data.ansatt.nav.no/quarto/"
    "0b700511-f50c-4059-b519-32fb19637bae/bemanning.html"
)
AUTH_WAIT_SECONDS = 2


def main() -> None:
    logger = get_logger(__name__)
    config = load_config()
    ensure_browser_ready(config)
    logger.info("Åpner midlertidig NAV-side med profil for %s", config.screen_id)
    open_url(config, NAV_BOOTSTRAP_URL, new_window=True)
    time.sleep(AUTH_WAIT_SECONDS)


if __name__ == "__main__":
    main()
