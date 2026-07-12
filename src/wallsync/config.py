from dataclasses import dataclass, field
from pathlib import Path

from .platform.paths import (
    wallpaper_dir,
    cache_dir,
    config_dir,
    data_dir,
)


@dataclass
class Config:
    wallpaper_dir: Path = field(default_factory=wallpaper_dir)

    cache_dir: Path = field(default_factory=cache_dir)

    database: Path = field(
        default_factory=lambda: data_dir() / "wallsync.db"
    )

    credentials: Path = field(
        default_factory=lambda: config_dir() / "credentials.json"
    )

    token: Path = field(
        default_factory=lambda: config_dir() / "token.json"
    )

    provider: str = "local"

    drive_folder_id: str = ""

    avoid_repeats: bool = True

    change_interval: int = 60