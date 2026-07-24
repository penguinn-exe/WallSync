import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List


@dataclass
class Config:
    config_dir: Path = Path.home() / ".config" / "wallsync"
    cache_dir: Path = Path.home() / ".cache" / "wallsync"
    data_dir: Path = Path.home() / ".local" / "share" / "wallsync"
    log_dir: Path = Path.home() / ".local" / "state" / "wallsync"

    provider: str = "composite"
    drive_folder_name: str = "Wallsync_repo"
    queue_size: int = 3
    desktop_environment: str = "auto"
    enable_notifications: bool = True
    sync_interval_minutes: int = 30
    light_dark_sync: bool = True
    lock_screen_sync: bool = True
    repositories: List[Dict[str, Any]] = field(
        default_factory=lambda: [
            {"name": "Google Drive Main", "type": "gdrive", "enabled": True, "folder": "Wallsync_repo"},
            {"name": "Local Wallpapers", "type": "local", "enabled": True, "path": "~/Pictures/Wallpapers"},
        ]
    )

    @property
    def config_file(self) -> Path:
        return self.config_dir / "config.json"

    @property
    def credentials_file(self) -> Path:
        return self.config_dir / "credentials.json"

    @property
    def token_file(self) -> Path:
        return self.config_dir / "token.json"

    @property
    def database_file(self) -> Path:
        return self.data_dir / "wallsync.db"

    @property
    def state_file(self) -> Path:
        return self.cache_dir / "state.json"

    @property
    def queue_file(self) -> Path:
        return self.cache_dir / "queue.json"

    @property
    def log_file(self) -> Path:
        return self.log_dir / "wallsync.log"

    def ensure_directories(self) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.log_dir.mkdir(parents=True, exist_ok=True)

    def load(self) -> "Config":
        self.ensure_directories()
        if self.config_file.exists():
            try:
                data = json.loads(self.config_file.read_text())
                for key, val in data.items():
                    if hasattr(self, key) and not key.endswith("_dir") and not key.endswith("_file"):
                        setattr(self, key, val)
            except Exception:
                pass
        return self

    def save(self) -> None:
        self.ensure_directories()
        data = {
            "provider": self.provider,
            "drive_folder_name": self.drive_folder_name,
            "queue_size": self.queue_size,
            "desktop_environment": self.desktop_environment,
            "enable_notifications": self.enable_notifications,
            "sync_interval_minutes": self.sync_interval_minutes,
            "light_dark_sync": self.light_dark_sync,
            "lock_screen_sync": self.lock_screen_sync,
            "repositories": self.repositories,
        }
        self.config_file.write_text(json.dumps(data, indent=4))

    def to_dict(self) -> Dict[str, Any]:
        return {
            "provider": self.provider,
            "drive_folder_name": self.drive_folder_name,
            "queue_size": self.queue_size,
            "desktop_environment": self.desktop_environment,
            "enable_notifications": self.enable_notifications,
            "sync_interval_minutes": self.sync_interval_minutes,
            "light_dark_sync": self.light_dark_sync,
            "lock_screen_sync": self.lock_screen_sync,
            "repositories_count": len(self.repositories),
            "config_dir": str(self.config_dir),
            "cache_dir": str(self.cache_dir),
            "database_file": str(self.database_file),
        }


def get_config() -> Config:
    config = Config()
    config.load()
    return config
