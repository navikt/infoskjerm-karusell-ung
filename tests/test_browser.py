from pathlib import Path

from infoskjerm.browser import build_open_command
from infoskjerm.config import ScreenConfig


def test_firefox_command_uses_dedicated_profile() -> None:
    config = ScreenConfig("ung", "firefox", 60, ("https://example.com",))

    command = build_open_command(
        config,
        "https://example.com",
        new_window=True,
        firefox_profile=Path("/tmp/profile"),
    )

    assert command == [
        "firefox",
        "--profile",
        "/tmp/profile",
        "--new-window",
        "https://example.com",
    ]


def test_other_browser_opens_new_tab_without_firefox_profile() -> None:
    config = ScreenConfig("standard", "chromium-browser", 30, ("https://example.com",))

    command = build_open_command(
        config,
        "https://example.com",
        new_window=False,
    )

    assert command == ["chromium-browser", "https://example.com"]
