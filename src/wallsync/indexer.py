from pathlib import Path

from PIL import Image

from wallsync.database import connect
from wallsync.hashing import sha256


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


def build_index(root: Path):
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM wallpapers")

    count = 0

    for file in root.rglob("*"):

        if not file.is_file():
            continue

        if file.suffix.lower() not in SUPPORTED_EXTENSIONS:
            continue

        try:
            with Image.open(file) as img:
                width = img.width
                height = img.height
        except Exception:
            continue

        file_hash = sha256(file)

        cursor.execute(
            """
            INSERT INTO wallpapers
            (
                path,
                filename,
                extension,
                size,
                width,
                height,
                sha256
            )
            VALUES
            (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                str(file),
                file.name,
                file.suffix.lower(),
                file.stat().st_size,
                width,
                height,
                file_hash,
            ),
        )

        count += 1

    conn.commit()
    conn.close()

    print(f"Indexed {count} wallpapers.")
