import sys
from pathlib import Path


def racine() -> Path:
    """Retourne la racine du projet, compatible .exe PyInstaller."""
    if getattr(sys, "frozen", False):
        # Mode .exe : PyInstaller extrait dans sys._MEIPASS
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parent.parent.parent


def chemin_data(nom: str) -> Path:
    return racine() / "data" / nom