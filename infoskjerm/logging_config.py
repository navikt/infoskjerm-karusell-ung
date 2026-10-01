import logging

from infoskjerm.config import REPO_ROOT


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        filename=REPO_ROOT / "karusell.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    return logging.getLogger(name)
