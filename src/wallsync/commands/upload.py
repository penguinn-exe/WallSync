from pathlib import Path
import sys
import time

from wallsync.providers.gdrive import GoogleDriveProvider

GREEN = "\033[32m"
RED = "\033[31m"
CYAN = "\033[36m"
YELLOW = "\033[33m"
RESET = "\033[0m"

SUPPORTED = {".jpg", ".jpeg", ".png", ".webp"}


def spinner(text):
    frames = ["|", "/", "-", "\\"]
    for frame in frames:
        sys.stdout.write(f"\r{CYAN}[{frame}]{RESET} {text}")
        sys.stdout.flush()
        time.sleep(0.03)


def collect_images(path: Path):
    if path.is_file():
        if path.suffix.lower() in SUPPORTED:
            return [path]
        return []

    images = []

    for ext in SUPPORTED:
        images.extend(path.rglob(f"*{ext}"))
        images.extend(path.rglob(f"*{ext.upper()}"))

    return sorted(images)


def run(target):
    path = Path(target).expanduser()

    if not path.exists():
        print(f"{RED}[✗]{RESET} Path not found.")
        return

    provider = GoogleDriveProvider()

    existing = {file["name"] for file in provider.list_wallpapers()}

    images = collect_images(path)

    if not images:
        print(f"{RED}[✗]{RESET} No supported images found.")
        return

    uploaded = 0
    skipped = 0
    failed = 0

    for image in images:
        if image.name in existing:
            print(f"{YELLOW}[i]{RESET} Skipped {image.name} (already exists)")
            skipped += 1
            continue

        try:
            spinner(f"Uploading {image.name}")

            provider.upload_wallpaper(image)

            sys.stdout.write(f"\r{GREEN}[✓]{RESET} Uploaded {image.name}\n")
            sys.stdout.flush()

            uploaded += 1

        except Exception:
            sys.stdout.write(f"\r{RED}[✗]{RESET} Failed {image.name}\n")
            sys.stdout.flush()

            failed += 1

    print()
    print(f"{GREEN}[✓]{RESET} Uploaded : {uploaded}")
    print(f"{YELLOW}[i]{RESET} Skipped  : {skipped}")

    if failed:
        print(f"{RED}[✗]{RESET} Failed   : {failed}")
