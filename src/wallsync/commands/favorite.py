from typing import Optional
from wallsync.config import get_config
from wallsync.db import Database

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run(action: str = "list", wallpaper_id: Optional[str] = None):
    config = get_config()
    db = Database(config.database_file)

    if action == "list":
        favs = db.list_favorites()
        if not favs:
            print(f"{YELLOW}[i]{RESET} No favorite wallpapers saved yet.")
            return
        print(f"{CYAN}Favorite Wallpapers ({len(favs)}){RESET}")
        print("──────────────────────────────────────────────────────")
        for f in favs:
            print(f"★ {f['filename']} (ID: {f['id']})")

    elif action == "add":
        if not wallpaper_id:
            # use current wallpaper
            if config.state_file.exists():
                import json
                state = json.loads(config.state_file.read_text())
                wallpaper_id = state.get("current", {}).get("id")
        if not wallpaper_id:
            print(f"{RED}[✗]{RESET} No wallpaper specified or selected.")
            return
        db.set_favorite(wallpaper_id, True)
        print(f"{GREEN}[✓]{RESET} Added wallpaper {wallpaper_id} to favorites.")

    elif action == "remove":
        if not wallpaper_id:
            print(f"{RED}[✗]{RESET} Usage: wallsync favorite remove <wallpaper_id>")
            return
        db.set_favorite(wallpaper_id, False)
        print(f"{GREEN}[✓]{RESET} Removed wallpaper {wallpaper_id} from favorites.")
