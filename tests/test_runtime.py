from infoskjerm.carousel import run_carousel
from infoskjerm.close_temp_pages import close_temp_pages
from infoskjerm.config import ScreenConfig
from infoskjerm.open_pages import open_pages


class FakeKeyboard:
    def __init__(self) -> None:
        self.hotkeys: list[tuple[str, ...]] = []

    def hotkey(self, *keys: str) -> None:
        self.hotkeys.append(keys)


def test_open_pages_preserves_order() -> None:
    config = ScreenConfig(
        "ung",
        "firefox",
        60,
        ("https://example.com/1", "https://example.com/2"),
    )
    opened: list[str] = []
    sleeps: list[float] = []

    def opener(_config: ScreenConfig, url: str) -> None:
        opened.append(url)

    open_pages(config, opener=opener, sleep=sleeps.append, delay=3)

    assert opened == list(config.pages)
    assert sleeps == [3, 3]


def test_close_temp_page_selects_first_tab() -> None:
    keyboard = FakeKeyboard()

    close_temp_pages(keyboard=keyboard, sleep=lambda _: None)

    assert keyboard.hotkeys == [("ctrl", "1"), ("ctrl", "w")]


def test_carousel_enters_fullscreen_and_rotates() -> None:
    config = ScreenConfig("ung", "firefox", 60, ("https://example.com",))
    keyboard = FakeKeyboard()
    sleeps: list[float] = []

    run_carousel(
        config,
        keyboard=keyboard,
        sleep=sleeps.append,
        max_rotations=2,
    )

    assert keyboard.hotkeys == [
        ("f11",),
        ("ctrl", "pgdn"),
        ("ctrl", "pgdn"),
    ]
    assert sleeps == [60, 60]
