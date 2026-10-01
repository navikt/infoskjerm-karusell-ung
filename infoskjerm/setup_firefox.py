from pathlib import Path

from infoskjerm.browser import FIREFOX_PROFILE

PREFERENCES = {
    "browser.sessionstore.resume_from_crash": "false",
    "browser.startup.page": "0",
    "browser.startup.homepage": '"about:blank"',
    "privacy.clearOnShutdown.cookies": "false",
    "privacy.sanitize.sanitizeOnShutdown": "false",
}


def update_user_js(profile: Path = FIREFOX_PROFILE) -> Path:
    profile.mkdir(parents=True, exist_ok=True)
    user_js = profile / "user.js"
    existing_lines = (
        user_js.read_text(encoding="utf-8").splitlines() if user_js.exists() else []
    )
    managed_prefixes = tuple(f'user_pref("{name}",' for name in PREFERENCES)
    retained_lines = [
        line for line in existing_lines if not line.strip().startswith(managed_prefixes)
    ]
    managed_lines = [
        f'user_pref("{name}", {value});' for name, value in PREFERENCES.items()
    ]
    content = "\n".join([*retained_lines, *managed_lines]).strip() + "\n"
    user_js.write_text(content, encoding="utf-8")
    return user_js


def main() -> None:
    user_js = update_user_js()
    print(f"Firefox-profilen er klar: {user_js.parent}")
    print("Start Firefox med 'just open-temp-pages' og logg inn i NAV manuelt.")


if __name__ == "__main__":
    main()
