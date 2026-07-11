import json
import random
from pathlib import Path

from wallsync.providers.gdrive import GoogleDriveProvider
from wallsync.wallpaper_manager import set_wallpaper

CACHE = Path.home() / ".cache" / "wallsync"
STATE = CACHE / "state.json"
QUEUE = CACHE / "queue.json"
QUEUE_SIZE = 3

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())

    return {
        "current": {},
        "shown": [],
    }


def save_state(state):
    STATE.write_text(json.dumps(state, indent=4))


def load_queue():
    if QUEUE.exists():
        return json.loads(QUEUE.read_text())

    return []


def save_queue(queue):
    QUEUE.write_text(json.dumps(queue, indent=4))


def fill_queue(provider, queue, state):
    wallpapers = provider.list_wallpapers()

    while len(queue) < QUEUE_SIZE:
        queued = {item["id"] for item in queue}
        shown = set(state["shown"])

        available = [
            w for w in wallpapers if w["id"] not in queued and w["id"] not in shown
        ]

        if not available:
            state["shown"] = []

            available = [w for w in wallpapers if w["id"] not in queued]

        if not available:
            break

        wallpaper = random.choice(available)

        filename = f"{wallpaper['id']}{Path(wallpaper['name']).suffix}"
        destination = CACHE / filename

        if not destination.exists():
            try:
                provider.download_wallpaper(
                    wallpaper["id"],
                    destination,
                )
            except Exception as e:
                print(f"{RED}[✗]{RESET} Failed to download {wallpaper['name']}")
                print(e)
                continue

        queue.append(
            {
                "id": wallpaper["id"],
                "name": wallpaper["name"],
                "file": filename,
            }
        )


def run():
    CACHE.mkdir(parents=True, exist_ok=True)

    provider = GoogleDriveProvider()

    state = load_state()
    queue = load_queue()

    fill_queue(provider, queue, state)

    if not queue:
        print(f"{RED}[✗]{RESET} No wallpapers available.")
        return

    current = queue.pop(0)

    wallpaper = CACHE / current["file"]

    try:
        set_wallpaper(str(wallpaper))
    except Exception as e:
        print(f"{RED}[✗]{RESET} Failed to set wallpaper")
        print(e)
        return

    state["current"] = current

    if current["id"] not in state["shown"]:
        state["shown"].append(current["id"])

    save_state(state)

    fill_queue(provider, queue, state)

    save_queue(queue)

    size = wallpaper.stat().st_size

    if size >= 1024 * 1024:
        size_str = f"{size / (1024 * 1024):.2f} MB"
    else:
        size_str = f"{size / 1024:.2f} KB"

    print(f"{GREEN}[✓]{RESET} Applied: {CYAN}{current['name']}{RESET} ({size_str})")

    print(f"{YELLOW}[i]{RESET} Cache: {len(queue)}/{QUEUE_SIZE}")
