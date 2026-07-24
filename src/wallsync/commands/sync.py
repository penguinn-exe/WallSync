from wallsync.config import get_config
from wallsync.db import Database
from wallsync.providers.gdrive import GoogleDriveProvider

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run():
    config = get_config()
    db = Database(config.database_file)
    print(f"{CYAN}[i]{RESET} Synchronizing wallpaper database with Google Drive...")

    try:
        provider = GoogleDriveProvider()
        wallpapers = provider.list_wallpapers()

        for w in wallpapers:
            db.upsert_wallpaper(
                wallpaper_id=w["id"],
                filename=w["name"],
                file_size=int(w.get("size", 0)),
                mime_type=w.get("mimeType"),
            )

        print(f"{GREEN}[✓]{RESET} Synchronization complete. Indexed {len(wallpapers)} wallpapers.")

    except Exception as e:
        print(f"{RED}[✗]{RESET} Sync failed: {e}")
