import time
from collections.abc import Callable

from infoskjerm.browser import ensure_browser_ready, open_url
from infoskjerm.config import ScreenConfig, load_config
from infoskjerm.logging_config import get_logger

PAGE_OPEN_DELAY_SECONDS = 30


def open_pages(
    config: ScreenConfig,
    *,
    opener: Callable[..., None] = open_url,
    sleep: Callable[[float], None] = time.sleep,
    delay: float = PAGE_OPEN_DELAY_SECONDS,
) -> None:
    for page in config.pages:
        opener(config, page)
        sleep(delay)


def main() -> None:
    logger = get_logger(__name__)
    config = load_config()
    ensure_browser_ready(config)
    open_pages(config)
    logger.info("Åpnet %d nettsider", len(config.pages))


if __name__ == "__main__":
    main()
