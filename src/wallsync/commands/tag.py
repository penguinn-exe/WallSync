from typing import Optional
from wallsync.config import get_config
from wallsync.db import Database

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run(action: str = "list", tag_name: Optional[str] = None, wallpaper_id: Optional[str] = None):
    config = get_config()
    db = Database(config.database_file)

    if action == "add":
        if not tag_name or not wallpaper_id:
            print(f"{RED}[✗]{RESET} Usage: wallsync tag add <tag_name> <wallpaper_id>")
            return
        db.add_tag(wallpaper_id, tag_name)
        print(f"{GREEN}[✓]{RESET} Added tag '{tag_name}' to wallpaper {wallpaper_id}.")

    elif action == "remove":
        if not tag_name or not wallpaper_id:
            print(f"{RED}[✗]{RESET} Usage: wallsync tag remove <tag_name> <wallpaper_id>")
            return
        db.remove_tag(wallpaper_id, tag_name)
        print(f"{GREEN}[✓]{RESET} Removed tag '{tag_name}' from wallpaper {wallpaper_id}.")

    elif action == "list":
        if wallpaper_id:
            tags = db.get_tags(wallpaper_id)
            print(f"{CYAN}Tags for wallpaper {wallpaper_id}:{RESET} {', '.join(tags) if tags else 'None'}")
        else:
            print(f"{CYAN}WallSync Tag System active.{RESET}")
