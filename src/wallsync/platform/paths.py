import os
import platform
from pathlib import Path


def config_dir() -> Path:
    if platform.system() == "Windows":
        return Path(os.environ["APPDATA"]) / "WallSync"

    return Path.home() / ".config" / "wallsync"


def data_dir() -> Path:
    if platform.system() == "Windows":
        return Path(os.environ["LOCALAPPDATA"]) / "WallSync"

    return Path.home() / ".local" / "share" / "wallsync"


def cache_dir() -> Path:
    if platform.system() == "Windows":
        return Path(os.environ["LOCALAPPDATA"]) / "WallSync" / "cache"

    return Path.home() / ".cache" / "wallsync"


def wallpaper_dir() -> Path:
    if platform.system() == "Windows":
        return Path(os.environ["LOCALAPPDATA"]) / "WallSync" / "wallpapers"

    return Path.home() / "Pictures" / "random" / "wallpaper_repo"