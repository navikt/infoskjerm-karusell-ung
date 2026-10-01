import time
from collections.abc import Callable
from typing import Protocol

from infoskjerm.logging_config import get_logger


class KeyboardController(Protocol):
    def hotkey(self, *keys: str) -> None: ...


def close_temp_pages(
    *,
    keyboard: KeyboardController,
    sleep: Callable[[float], None] = time.sleep,
) -> None:
    keyboard.hotkey("ctrl", "1")
    sleep(1)
    keyboard.hotkey("ctrl", "w")


def main() -> None:
    import pyautogui

    pyautogui.FAILSAFE = False
    close_temp_pages(keyboard=pyautogui)
    get_logger(__name__).info("Lukket den midlertidige NAV-fanen")


if __name__ == "__main__":
    main()
