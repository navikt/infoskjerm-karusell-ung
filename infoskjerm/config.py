from dataclasses import dataclass
from pathlib import Path
from typing import Any

import yaml

REPO_ROOT = Path(__file__).resolve().parent.parent


class ConfigError(ValueError):
    """Configuration that cannot safely start the infoscreen."""


@dataclass(frozen=True)
class ScreenConfig:
    screen_id: str
    browser: str
    tab_duration: int
    pages: tuple[str, ...]


def _read_screen_id(path: Path) -> str:
    try:
        screen_id = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError:
        return "standard"
    if not screen_id:
        raise ConfigError(f"{path.name} er tom")
    return screen_id


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
    except FileNotFoundError as error:
        raise ConfigError(f"Fant ikke {path}") from error
    except yaml.YAMLError as error:
        raise ConfigError(f"Ugyldig YAML i {path}: {error}") from error

    if not isinstance(data, dict) or not isinstance(data.get("infoskjermer"), dict):
        raise ConfigError(f"{path} må inneholde en 'infoskjermer'-mapping")
    return data["infoskjermer"]


def _require_mapping(value: Any, name: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise ConfigError(f"Konfigurasjonen '{name}' må være en mapping")
    return value


def _require_pages(value: Any, name: str) -> list[str]:
    if not isinstance(value, list) or not all(
        isinstance(page, str) and page.strip() for page in value
    ):
        raise ConfigError(f"'{name}' må være en liste med URL-er")
    return value


def load_config(repo_root: Path = REPO_ROOT) -> ScreenConfig:
    screens = _load_yaml(repo_root / "nettsider.yaml")
    standard = _require_mapping(screens.get("standard"), "standard")
    screen_id = _read_screen_id(repo_root / "INFOSKJERM_ID")

    if screen_id not in screens:
        raise ConfigError(f"Konfigurasjonen '{screen_id}' finnes ikke")
    selected = _require_mapping(screens[screen_id], screen_id)

    browser = selected.get("browser", standard.get("browser"))
    if not isinstance(browser, str) or not browser.strip():
        raise ConfigError("'browser' må være en kommando")

    tab_duration = selected.get("fanetid", standard.get("fanetid"))
    if not isinstance(tab_duration, int) or isinstance(tab_duration, bool):
        raise ConfigError("'fanetid' må være et heltall")
    if tab_duration <= 0:
        raise ConfigError("'fanetid' må være større enn 0")

    standard_pages = _require_pages(standard.get("nettsider"), "standard.nettsider")
    selected_pages = _require_pages(
        selected.get("nettsider", []), f"{screen_id}.nettsider"
    )
    show_standard = selected.get(
        "vis_standardnettsider", standard.get("vis_standardnettsider")
    )
    if not isinstance(show_standard, bool):
        raise ConfigError("'vis_standardnettsider' må være true eller false")

    if screen_id == "standard":
        pages = standard_pages
    elif show_standard:
        pages = [*standard_pages, *selected_pages]
    else:
        pages = selected_pages
    if not pages:
        raise ConfigError(f"Konfigurasjonen '{screen_id}' har ingen nettsider")

    return ScreenConfig(
        screen_id=screen_id,
        browser=browser,
        tab_duration=tab_duration,
        pages=tuple(pages),
    )
