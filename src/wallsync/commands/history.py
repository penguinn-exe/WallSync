import time
from wallsync.config import get_config
from wallsync.db import Database

CYAN = "\033[36m"
RESET = "\033[0m"
YELLOW = "\033[33m"


def run(limit: int = 10):
    config = get_config()
    db = Database(config.database_file)
    history = db.get_history(limit=limit)

    if not history:
        print(f"{YELLOW}[i]{RESET} Wallpaper history is empty.")
        return

    print(f"{CYAN}WallSync Wallpaper History (Last {len(history)}){RESET}")
    print("──────────────────────────────────────────────────────")

    now = time.time()
    for idx, item in enumerate(history, 1):
        elapsed = int(now - item["viewed_at"])
        if elapsed < 60:
            time_str = f"{elapsed}s ago"
        elif elapsed < 3600:
            time_str = f"{elapsed // 60}m ago"
        else:
            time_str = f"{elapsed // 3600}h ago"

        prefix = "► " if idx == 1 else "  "
        print(f"{prefix}{idx}. {item['filename']} ({time_str})")
