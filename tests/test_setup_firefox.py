from pathlib import Path

from infoskjerm.setup_firefox import PREFERENCES, update_user_js


def test_setup_firefox_is_idempotent_and_preserves_other_preferences(
    tmp_path: Path,
) -> None:
    user_js = tmp_path / "user.js"
    user_js.write_text(
        'user_pref("custom.preference", true);\n'
        'user_pref("browser.startup.page", 3);\n',
        encoding="utf-8",
    )

    assert update_user_js(tmp_path) == user_js
    update_user_js(tmp_path)

    content = user_js.read_text(encoding="utf-8")
    assert 'user_pref("custom.preference", true);' in content
    assert 'user_pref("browser.startup.page", 0);' in content
    assert content.count('user_pref("browser.startup.page",') == 1
    for preference in PREFERENCES:
        assert content.count(f'user_pref("{preference}",') == 1
