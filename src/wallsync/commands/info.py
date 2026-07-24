import json
from pathlib import Path

from wallsync.providers.gdrive import GoogleDriveProvider

CACHE = Path.home() / ".cache" / "wallsync"
STATE = CACHE / "state.json"
QUEUE = CACHE / "queue.json"

CYAN = "\033[36m"
RED = "\033[31m"
RESET = "\033[0m"


def human_size(size):
    if size >= 1024 * 1024:
        return f"{size / (1024 * 1024):.2f} MB"
    return f"{size / 1024:.2f} KB"


def run():
    if not STATE.exists():
        print(f"{RED}[✗]{RESET} No wallpaper selected.")
        return

    state = json.loads(STATE.read_text())
    current = state.get("current", {})

    if not current:
        print(f"{RED}[✗]{RESET} No wallpaper selected.")
        return

    wallpaper = CACHE / current["file"]

    if wallpaper.exists():
        size = human_size(wallpaper.stat().st_size)
    else:
        size = "Unknown"

    queue = json.loads(QUEUE.read_text()) if QUEUE.exists() else []

    cache_files = [
        f
        for f in CACHE.iterdir()
        if f.is_file() and f.name not in ("state.json", "queue.json")
    ]

    cache_size = human_size(sum(f.stat().st_size for f in cache_files))

    provider = GoogleDriveProvider()
    drive_count = len(provider.list_wallpapers())

    print(f"{CYAN}WallSync Status{RESET}")
    print("──────────────────────────────")
    print(f"Current : {current['name']}")
    print(f"Size    : {size}")
    print(f"Drive   : {drive_count} wallpapers")
    print(f"Cache   : {len(queue)} wallpapers • {cache_size}")
