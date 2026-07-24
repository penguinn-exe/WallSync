from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    wallpaper_dir: Path = Path.home() / "Pictures/random/wallpaper_repo"

    cache_dir: Path = Path.home() / ".cache/wallsync"

    database: Path = Path.home() / ".local/share/wallsync/wallsync.db"

    credentials: Path = Path.home() / ".config/wallsync/credentials.json"

    token: Path = Path.home() / ".config/wallsync/token.json"

    provider: str = "local"

    drive_folder_id: str = ""

    avoid_repeats: bool = True

    change_interval: int = 60
