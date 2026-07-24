import json
import random
import subprocess
from pathlib import Path

from wallsync.config import get_config
from wallsync.db import Database
from wallsync.providers.composite import CompositeProvider
from wallsync.wallpaper_manager import set_wallpaper

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def notify(title: str, message: str) -> None:
    try:
        subprocess.run(["notify-send", "-a", "WallSync", title, message], check=False)
    except Exception:
        pass


def load_state(state_file: Path) -> dict:
    if state_file.exists():
        try:
            return json.loads(state_file.read_text())
        except Exception:
            pass
    return {"current": {}, "shown": []}


def save_state(state_file: Path, state: dict) -> None:
    state_file.write_text(json.dumps(state, indent=4))


def load_queue(queue_file: Path) -> list:
    if queue_file.exists():
        try:
            return json.loads(queue_file.read_text())
        except Exception:
            pass
    return []


def save_queue(queue_file: Path, queue: list) -> None:
    queue_file.write_text(json.dumps(queue, indent=4))


def fill_queue(provider, queue, state, config, db):
    wallpapers = provider.list_wallpapers()
    for w in wallpapers:
        db.upsert_wallpaper(
            wallpaper_id=w["id"],
            filename=w["name"],
            provider=w.get("provider_type", "composite"),
            file_size=int(w.get("size", 0)),
            mime_type=w.get("mimeType"),
        )

    while len(queue) < config.queue_size:
        queued = {item["id"] for item in queue}
        shown = set(state.get("shown", []))

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
        destination = config.cache_dir / filename

        if not destination.exists():
            try:
                provider.download_wallpaper(wallpaper["id"], destination)
            except Exception as e:
                print(f"{RED}[✗]{RESET} Failed to download {wallpaper['name']} ({e})")
                continue

        queue.append(
            {
                "id": wallpaper["id"],
                "name": wallpaper["name"],
                "file": filename,
                "provider": wallpaper.get("provider_type", "composite"),
                "repo_name": wallpaper.get("repo_name", "Default"),
            }
        )


def run(preview: bool = False, dry_run: bool = False):
    config = get_config()
    db = Database(config.database_file)
    provider = CompositeProvider(config)

    state = load_state(config.state_file)
    queue = load_queue(config.queue_file)

    fill_queue(provider, queue, state, config, db)

    if not queue:
        print(f"{RED}[✗]{RESET} No wallpapers available in any active repository.")
        return

    if preview:
        peek = queue[0]
        print(f"{CYAN}[i]{RESET} Next queued wallpaper: {peek['name']} (from {peek.get('repo_name', 'Repo')})")
        return

    current = queue.pop(0)
    wallpaper = config.cache_dir / current["file"]

    if dry_run:
        print(f"{YELLOW}[Dry-Run]{RESET} Would apply wallpaper: {current['name']} ({current.get('repo_name')})")
        return

    success, de_name = set_wallpaper(
        str(wallpaper),
        desktop=config.desktop_environment,
        light_dark=config.light_dark_sync,
        lock_screen=config.lock_screen_sync,
    )

    if not success:
        print(f"{RED}[✗]{RESET} Failed to set wallpaper: {de_name}")
        return

    state["current"] = current
    if "shown" not in state:
        state["shown"] = []

    if current["id"] not in state["shown"]:
        state["shown"].append(current["id"])

    save_state(config.state_file, state)
    db.record_view(current["id"], current["name"])

    fill_queue(provider, queue, state, config, db)
    save_queue(config.queue_file, queue)

    size = wallpaper.stat().st_size if wallpaper.exists() else 0
    size_str = f"{size / (1024 * 1024):.2f} MB" if size >= 1024 * 1024 else f"{size / 1024:.2f} KB"

    print(
        f"{GREEN}[✓]{RESET} Applied: {CYAN}{current['name']}{RESET} ({size_str}) "
        f"[{current.get('repo_name', 'Repo')}] [{de_name}]"
    )
    print(f"{YELLOW}[i]{RESET} Cache Queue: {len(queue)}/{config.queue_size}")

    if config.enable_notifications:
        notify("WallSync Updated", f"Applied {current['name']} ({current.get('repo_name')})")
