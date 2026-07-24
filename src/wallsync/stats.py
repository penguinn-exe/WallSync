import json
import subprocess
import time
from pathlib import Path
from typing import Any, Dict

from wallsync.config import Config
from wallsync.db import Database


def human_size(size_bytes: int) -> str:
    if size_bytes >= 1024 * 1024 * 1024:
        return f"{size_bytes / (1024 * 1024 * 1024):.2f} GB"
    elif size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.2f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.2f} KB"
    return f"{size_bytes} B"


def get_full_stats(config: Config) -> Dict[str, Any]:
    db = Database(config.database_file)
    db_stats = db.get_stats()

    # Cache statistics
    cache_files = []
    if config.cache_dir.exists():
        cache_files = [
            f for f in config.cache_dir.iterdir()
            if f.is_file() and f.name not in ("state.json", "queue.json")
        ]

    cache_bytes = sum(f.stat().st_size for f in cache_files)

    # State & DB size
    db_bytes = config.database_file.stat().st_size if config.database_file.exists() else 0
    state_bytes = config.state_file.stat().st_size if config.state_file.exists() else 0
    config_bytes = config.config_file.stat().st_size if config.config_file.exists() else 0
    total_data_bytes = db_bytes + state_bytes + config_bytes

    # Queue info
    queue_count = 0
    if config.queue_file.exists():
        try:
            queue_data = json.loads(config.queue_file.read_text())
            queue_count = len(queue_data)
        except Exception:
            pass

    # Systemd Timer Interval
    timer_interval = f"{config.sync_interval_minutes} minutes"
    try:
        res = subprocess.run(
            ["systemctl", "--user", "show", "wallsync.timer", "--property=OnUnitActiveUSec", "--value"],
            capture_output=True, text=True
        )
        if res.stdout.strip():
            timer_interval = res.stdout.strip()
    except Exception:
        pass

    # Formatting Last Sync
    last_sync_str = "Never"
    if db_stats.get("last_sync"):
        elapsed = int(time.time() - db_stats["last_sync"])
        if elapsed < 60:
            last_sync_str = f"{elapsed}s ago"
        elif elapsed < 3600:
            last_sync_str = f"{elapsed // 60}m ago"
        else:
            last_sync_str = f"{elapsed // 3600}h ago"

    return {
        "total_wallpapers": db_stats["total"],
        "never_shown": db_stats["never_shown"],
        "most_shown": db_stats["most_shown"],
        "least_shown": db_stats["least_shown"],
        "last_sync": last_sync_str,
        "cache_count": len(cache_files),
        "cache_size_str": human_size(cache_bytes),
        "database_size_str": human_size(total_data_bytes),
        "queue_count": queue_count,
        "queue_size_max": config.queue_size,
        "interval": timer_interval,
    }
