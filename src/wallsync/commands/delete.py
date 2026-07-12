import json
from pathlib import Path

from wallsync.commands.next import run as next_wallpaper
from wallsync.providers.gdrive import GoogleDriveProvider

from wallsync.config import Config

config = Config()
CACHE = config.cache_dir
STATE = CACHE / "state.json"


def run(force=False):
    if not STATE.exists():
        print("No wallpaper selected.")
        return

    current = json.loads(STATE.read_text())["current"]

    if not force:
        answer = (
            input(f'Delete "{current["name"]}" from Google Drive? [y/N]: ')
            .strip()
            .lower()
        )

        if answer not in ("y", "yes"):
            print("Cancelled.")
            return

    provider = GoogleDriveProvider()

    provider.delete_wallpaper(current["id"])

    (CACHE / current["file"]).unlink(missing_ok=True)

    print(f"Deleted: {current['name']}")

    next_wallpaper()
