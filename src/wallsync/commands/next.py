from wallsync.database import connect
from wallsync.wallpaper import set_wallpaper


def run():
    conn = connect()
    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT id, path
        FROM wallpapers
        ORDER BY
            CASE
                WHEN last_shown IS NULL THEN 0
                ELSE 1
            END,
            last_shown ASC,
            RANDOM()
        LIMIT 1
        """
    )

    wallpaper = cursor.fetchone()

    if wallpaper is None:
        print("Database is empty.")
        conn.close()
        return

    wallpaper_id = wallpaper[0]
    wallpaper_path = wallpaper[1]

    # Apply wallpaper
    set_wallpaper(wallpaper_path)

    # Update wallpaper history
    cursor.execute(
        """
        UPDATE wallpapers
        SET
            last_shown = CURRENT_TIMESTAMP,
            times_shown = times_shown + 1
        WHERE id = ?
        """,
        (wallpaper_id,),
    )

    conn.commit()
    conn.close()

    print("\nWallpaper Applied")
    print("-----------------")
    print(f"Path : {wallpaper_path}")
    print(f"ID   : {wallpaper_id}")
