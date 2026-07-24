from wallsync.config import get_config

GREEN = "\033[32m"
CYAN = "\033[36m"
RESET = "\033[0m"


def run():
    config = get_config()
    print(f"{CYAN}[i]{RESET} Cleaning up WallSync cache directory...")
    removed = 0
    bytes_freed = 0

    if config.cache_dir.exists():
        for item in config.cache_dir.iterdir():
            if item.is_file() and item.name not in ("state.json", "queue.json"):
                size = item.stat().st_size
                item.unlink(missing_ok=True)
                removed += 1
                bytes_freed += size

    size_mb = bytes_freed / (1024 * 1024)
    print(f"{GREEN}[✓]{RESET} Removed {removed} cached wallpaper files ({size_mb:.2f} MB freed).")
