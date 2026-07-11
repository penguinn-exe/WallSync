import time
from pathlib import Path

from PIL import Image

from wallsync.models import CollectionStats

SUPPORTED_EXTENSIONS = {
    ".jpg",
    ".jpeg",
    ".png",
    ".webp",
    ".bmp",
    ".gif",
    ".tiff",
    ".avif",
}


def format_size(size_bytes: int) -> str:
    units = ["B", "KB", "MB", "GB", "TB"]

    size = float(size_bytes)

    for unit in units:
        if size < 1024 or unit == units[-1]:
            return f"{size:.2f} {unit}"
        size /= 1024


def run(directory: str):
    path = Path(directory)

    if not path.exists():
        print("Directory does not exist.")
        return

    if not path.is_dir():
        print("Not a directory.")
        return

    stats = CollectionStats()

    start = time.perf_counter()

    for item in path.rglob("*"):

        if item.is_dir():
            stats.folders += 1
            continue

        if not item.is_file():
            continue

        if item.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        stats.images += 1
        stats.total_size += item.stat().st_size
        stats.formats[item.suffix.lower()] += 1

        try:
            with Image.open(item) as img:
                resolution = f"{img.width}x{img.height}"
                stats.resolutions[resolution] += 1

        except Exception:
            stats.corrupted += 1

    elapsed = time.perf_counter() - start

    print("\nCollection Summary")
    print("------------------------------")
    print(f"Directory : {path}")
    print(f"Images    : {stats.images}")
    print(f"Folders   : {stats.folders}")
    print(f"Size      : {format_size(stats.total_size)}")
    print(f"Corrupted : {stats.corrupted}")
    print(f"Time      : {elapsed:.2f}s")

    print("\nFormats")
    print("-------")
    for ext, count in sorted(stats.formats.items()):
        print(f"{ext:<10}{count}")

    print("\nTop 10 Resolutions")
    print("------------------")
    for resolution, count in stats.resolutions.most_common(10):
        print(f"{resolution:<15}{count}")
