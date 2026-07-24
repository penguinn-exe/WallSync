from wallsync.config import get_config
from wallsync.db import Database

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run(force: bool = False):
    config = get_config()
    if not force:
        ans = input("Are you sure you want to reset WallSync database and cache? [y/N]: ").strip().lower()
        if ans not in ("y", "yes"):
            print("Reset cancelled.")
            return

    db = Database(config.database_file)
    db.reset()

    if config.cache_dir.exists():
        for item in config.cache_dir.iterdir():
            if item.is_file():
                item.unlink(missing_ok=True)

    print(f"{GREEN}[✓]{RESET} WallSync cache and database reset complete.")
