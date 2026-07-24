import json
from wallsync.config import get_config
from wallsync.db import Database
from wallsync.providers.gdrive import GoogleDriveProvider
from wallsync.stats import get_full_stats

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run():
    config = get_config()
    stats = get_full_stats(config)
    state = json.loads(config.state_file.read_text()) if config.state_file.exists() else {}
    current = state.get("current", {})

    print(f"{CYAN}WallSync Status & Wallpaper Metrics{RESET}")
    print("──────────────────────────────────────────────────────")
    if current and "name" in current:
        print(f"Current      : {GREEN}{current['name']}{RESET}")
    else:
        print(f"Current      : None selected")

    print(f"Total Drive  : {stats['total_wallpapers']} wallpapers")
    print(f"Never Shown  : {stats['never_shown']} wallpapers")

    if stats["most_shown"]:
        most = stats["most_shown"][0]
        print(f"Most Shown   : {most['filename']} ({most['view_count']} views)")
    else:
        print(f"Most Shown   : N/A")

    if stats["least_shown"]:
        least = stats["least_shown"][0]
        print(f"Least Shown  : {least['filename']} ({least['view_count']} views)")
    else:
        print(f"Least Shown  : N/A")

    print(f"Last Sync    : {stats['last_sync']}")
    print(f"Cache        : {stats['cache_count']} files • {stats['cache_size_str']}")
    print(f"Database     : {stats['database_size_str']}")
    print(f"Interval     : {stats['interval']}")
