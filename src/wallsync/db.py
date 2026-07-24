import sqlite3
import time
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple


class Database:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.init_db()

    def get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        return conn

    def init_db(self) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS wallpapers (
                    id TEXT PRIMARY KEY,
                    provider TEXT NOT NULL DEFAULT 'gdrive',
                    drive_file_id TEXT,
                    filename TEXT NOT NULL,
                    file_size INTEGER DEFAULT 0,
                    mime_type TEXT,
                    created_at REAL,
                    view_count INTEGER DEFAULT 0,
                    last_viewed_at REAL,
                    is_favorite INTEGER DEFAULT 0,
                    is_excluded INTEGER DEFAULT 0
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wallpaper_id TEXT NOT NULL,
                    filename TEXT NOT NULL,
                    viewed_at REAL NOT NULL,
                    FOREIGN KEY (wallpaper_id) REFERENCES wallpapers(id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS tags (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    wallpaper_id TEXT NOT NULL,
                    tag_name TEXT NOT NULL,
                    UNIQUE(wallpaper_id, tag_name),
                    FOREIGN KEY (wallpaper_id) REFERENCES wallpapers(id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS collections (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT UNIQUE NOT NULL,
                    description TEXT
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS collection_wallpapers (
                    collection_id INTEGER NOT NULL,
                    wallpaper_id TEXT NOT NULL,
                    PRIMARY KEY (collection_id, wallpaper_id),
                    FOREIGN KEY (collection_id) REFERENCES collections(id),
                    FOREIGN KEY (wallpaper_id) REFERENCES wallpapers(id)
                )
                """
            )
            cursor.execute(
                """
                CREATE TABLE IF NOT EXISTS sync_meta (
                    key TEXT PRIMARY KEY,
                    value TEXT,
                    updated_at REAL
                )
                """
            )
            conn.commit()

    def upsert_wallpaper(
        self,
        wallpaper_id: str,
        filename: str,
        provider: str = "gdrive",
        drive_file_id: Optional[str] = None,
        file_size: int = 0,
        mime_type: Optional[str] = None,
    ) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                INSERT INTO wallpapers (id, provider, drive_file_id, filename, file_size, mime_type, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    filename=excluded.filename,
                    file_size=excluded.file_size,
                    mime_type=excluded.mime_type
                """,
                (
                    wallpaper_id,
                    provider,
                    drive_file_id or wallpaper_id,
                    filename,
                    file_size,
                    mime_type,
                    time.time(),
                ),
            )
            conn.commit()

    def record_view(self, wallpaper_id: str, filename: str) -> None:
        now = time.time()
        with self.get_connection() as conn:
            cursor = conn.cursor()
            self.upsert_wallpaper(wallpaper_id, filename)
            cursor.execute(
                """
                UPDATE wallpapers
                SET view_count = view_count + 1, last_viewed_at = ?
                WHERE id = ?
                """,
                (now, wallpaper_id),
            )
            cursor.execute(
                """
                INSERT INTO history (wallpaper_id, filename, viewed_at)
                VALUES (?, ?, ?)
                """,
                (wallpaper_id, filename, now),
            )
            cursor.execute(
                """
                INSERT INTO sync_meta (key, value, updated_at)
                VALUES ('last_sync', ?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value, updated_at=excluded.updated_at
                """,
                (str(now), now),
            )
            conn.commit()

    def get_history(self, limit: int = 20) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                """
                SELECT id, wallpaper_id, filename, viewed_at
                FROM history
                ORDER BY id DESC
                LIMIT ?
                """,
                (limit,),
            )
            return [dict(row) for row in cursor.fetchall()]

    def set_favorite(self, wallpaper_id: str, is_favorite: bool = True) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE wallpapers SET is_favorite = ? WHERE id = ?",
                (1 if is_favorite else 0, wallpaper_id),
            )
            conn.commit()

    def list_favorites(self) -> List[Dict[str, Any]]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM wallpapers WHERE is_favorite = 1 ORDER BY filename ASC"
            )
            return [dict(row) for row in cursor.fetchall()]

    def add_tag(self, wallpaper_id: str, tag_name: str) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT OR IGNORE INTO tags (wallpaper_id, tag_name) VALUES (?, ?)",
                (wallpaper_id, tag_name.lower().strip()),
            )
            conn.commit()

    def remove_tag(self, wallpaper_id: str, tag_name: str) -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tags WHERE wallpaper_id = ? AND tag_name = ?",
                (wallpaper_id, tag_name.lower().strip()),
            )
            conn.commit()

    def get_tags(self, wallpaper_id: str) -> List[str]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT tag_name FROM tags WHERE wallpaper_id = ?", (wallpaper_id,)
            )
            return [row["tag_name"] for row in cursor.fetchall()]

    def get_stats(self) -> Dict[str, Any]:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) as cnt FROM wallpapers")
            total = cursor.fetchone()["cnt"]

            cursor.execute("SELECT COUNT(*) as cnt FROM wallpapers WHERE view_count = 0")
            never_shown = cursor.fetchone()["cnt"]

            cursor.execute(
                "SELECT id, filename, view_count FROM wallpapers WHERE view_count > 0 ORDER BY view_count DESC LIMIT 3"
            )
            most_shown = [dict(row) for row in cursor.fetchall()]

            cursor.execute(
                "SELECT id, filename, view_count FROM wallpapers ORDER BY view_count ASC LIMIT 3"
            )
            least_shown = [dict(row) for row in cursor.fetchall()]

            cursor.execute(
                "SELECT value, updated_at FROM sync_meta WHERE key = 'last_sync'"
            )
            last_sync_row = cursor.fetchone()
            last_sync = last_sync_row["updated_at"] if last_sync_row else None

            return {
                "total": total,
                "never_shown": never_shown,
                "most_shown": most_shown,
                "least_shown": least_shown,
                "last_sync": last_sync,
            }

    def reset() -> None:
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM history")
            cursor.execute("DELETE FROM tags")
            cursor.execute("DELETE FROM collection_wallpapers")
            cursor.execute("DELETE FROM collections")
            cursor.execute("DELETE FROM wallpapers")
            cursor.execute("DELETE FROM sync_meta")
            conn.commit()
