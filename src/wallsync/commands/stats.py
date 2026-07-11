from wallsync.config import Config
from wallsync.database import connect

config = Config()


def format_size(size):
    units = ["B", "KB", "MB", "GB"]

    size = float(size)

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} TB"


def run():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM wallpapers")
    indexed = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM wallpapers WHERE last_shown IS NULL"
    )
    never_shown = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COALESCE(SUM(times_shown),0) FROM wallpapers"
    )
    total_displays = cursor.fetchone()[0]

    cursor.execute(
        "SELECT COUNT(*) FROM wallpapers WHERE favorite = 1"
    )
    favorites = cursor.fetchone()[0]

    conn.close()

    db_size = (
        format_size(config.database.stat().st_size)
        if config.database.exists()
        else "0 B"
    )

    print("\nWallSync Statistics")
    print("-------------------")
    print(f"Indexed Wallpapers : {indexed}")
    print(f"Never Shown        : {never_shown}")
    print(f"Total Displays     : {total_displays}")
    print(f"Favorites          : {favorites}")
    print(f"Database Size      : {db_size}")
