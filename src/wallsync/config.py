from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    wallpaper_dir: Path = Path.home() / "Pictures/random/wallpaper_repo"
    cache_dir: Path = Path.home() / ".cache/wallsync"
    database: Path = Path.home() / ".local/share/wallsync/wallsync.db"

    provider: str = "local"

    change_interval: int = 60

    avoid_repeats: bool = True
