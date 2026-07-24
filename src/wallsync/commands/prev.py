from wallsync.config import get_config
from wallsync.db import Database
from wallsync.wallpaper_manager import set_wallpaper

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run():
    config = get_config()
    db = Database(config.database_file)
    history = db.get_history(limit=5)

    if len(history) < 2:
        print(f"{YELLOW}[i]{RESET} No previous wallpaper in history.")
        return

    # history[0] is current, history[1] is previous
    prev_item = history[1]
    wallpaper_id = prev_item["wallpaper_id"]
    filename = prev_item["filename"]

    cache_file = None
    for f in config.cache_dir.iterdir():
        if f.is_file() and f.name.startswith(wallpaper_id):
            cache_file = f
            break

    if not cache_file or not cache_file.exists():
        print(f"{RED}[✗]{RESET} Previous wallpaper file not found in local cache.")
        return

    success, de_name = set_wallpaper(
        str(cache_file),
        desktop=config.desktop_environment,
        light_dark=config.light_dark_sync,
        lock_screen=config.lock_screen_sync,
    )

    if success:
        db.record_view(wallpaper_id, filename)
        print(f"{GREEN}[✓]{RESET} Reverted to previous wallpaper: {CYAN}{filename}{RESET} [{de_name}]")
    else:
        print(f"{RED}[✗]{RESET} Failed to set previous wallpaper.")
