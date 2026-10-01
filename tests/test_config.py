from pathlib import Path

import pytest

from infoskjerm.config import ConfigError, load_config


def write_config(root: Path, yaml_content: str, screen_id: str | None = None) -> None:
    (root / "nettsider.yaml").write_text(yaml_content, encoding="utf-8")
    if screen_id is not None:
        (root / "INFOSKJERM_ID").write_text(screen_id, encoding="utf-8")


BASE_CONFIG = """
infoskjermer:
  standard:
    browser: firefox
    fanetid: 30
    vis_standardnettsider: true
    nettsider:
      - https://example.com/standard
  ung:
    fanetid: 60
    nettsider:
      - https://example.com/ung
"""


def test_selected_screen_inherits_standard_pages(tmp_path: Path) -> None:
    write_config(tmp_path, BASE_CONFIG, "ung")

    config = load_config(tmp_path)

    assert config.browser == "firefox"
    assert config.tab_duration == 60
    assert config.pages == (
        "https://example.com/standard",
        "https://example.com/ung",
    )


def test_standard_fallback_does_not_duplicate_pages(tmp_path: Path) -> None:
    write_config(tmp_path, BASE_CONFIG)

    config = load_config(tmp_path)

    assert config.screen_id == "standard"
    assert config.pages == ("https://example.com/standard",)


def test_unknown_screen_fails_clearly(tmp_path: Path) -> None:
    write_config(tmp_path, BASE_CONFIG, "ukjent")

    with pytest.raises(ConfigError, match="ukjent"):
        load_config(tmp_path)


def test_invalid_tab_duration_fails(tmp_path: Path) -> None:
    write_config(tmp_path, BASE_CONFIG.replace("fanetid: 30", "fanetid: 0"))

    with pytest.raises(ConfigError, match="større enn 0"):
        load_config(tmp_path)
