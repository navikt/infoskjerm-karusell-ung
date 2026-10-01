import time
from collections.abc import Callable

from infoskjerm.close_temp_pages import KeyboardController
from infoskjerm.config import ScreenConfig, load_config
from infoskjerm.logging_config import get_logger


def run_carousel(
    config: ScreenConfig,
    *,
    keyboard: KeyboardController,
    sleep: Callable[[float], None] = time.sleep,
    max_rotations: int | None = None,
) -> None:
    logger = get_logger(__name__)
    keyboard.hotkey("f11")
    rotations = 0

    while max_rotations is None or rotations < max_rotations:
        keyboard.hotkey("ctrl", "pgdn")
        sleep(config.tab_duration)
        rotations += 1
        if rotations % 100 == 0:
            logger.info("Karusellen har rullet %d ganger", rotations)


def main() -> None:
    import pyautogui

    pyautogui.FAILSAFE = False
    logger = get_logger(__name__)
    config = load_config()
    logger.info("Starter karusell for %s", config.screen_id)
    try:
        run_carousel(config, keyboard=pyautogui)
    except KeyboardInterrupt:
        logger.info("Karusellen ble avbrutt manuelt")


if __name__ == "__main__":
    main()
