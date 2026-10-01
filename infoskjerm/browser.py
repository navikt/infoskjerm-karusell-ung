import shutil
import subprocess
import time
from pathlib import Path

from infoskjerm.config import ConfigError, ScreenConfig

FIREFOX_PROFILE = Path.home() / ".mozilla" / "firefox" / "infoskjerm"


def is_firefox(browser: str) -> bool:
    return Path(browser).name.startswith("firefox")


def build_open_command(
    config: ScreenConfig,
    url: str,
    *,
    new_window: bool,
    firefox_profile: Path = FIREFOX_PROFILE,
) -> list[str]:
    if is_firefox(config.browser):
        action = "--new-window" if new_window else "--new-tab"
        return [
            config.browser,
            "--profile",
            str(firefox_profile),
            action,
            url,
        ]

    if new_window:
        return [config.browser, "--new-window", url]
    return [config.browser, url]


def ensure_browser_ready(config: ScreenConfig) -> None:
    if shutil.which(config.browser) is None:
        raise ConfigError(f"Fant ikke nettleserkommandoen '{config.browser}'")
    if is_firefox(config.browser) and not FIREFOX_PROFILE.is_dir():
        raise ConfigError(
            "Firefox-profilen mangler. Kjør 'just setup-firefox' først."
        )


def open_url(
    config: ScreenConfig,
    url: str,
    *,
    new_window: bool = False,
    startup_check_seconds: float = 1,
) -> None:
    command = build_open_command(config, url, new_window=new_window)
    process = subprocess.Popen(command)
    time.sleep(startup_check_seconds)
    status = process.poll()
    if status not in (None, 0):
        raise RuntimeError(
            f"Nettleseren avsluttet med status {status}: {' '.join(command)}"
        )
