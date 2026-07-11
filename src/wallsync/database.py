import sqlite3

from wallsync.config import Config

config = Config()


def connect():
    config.database.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(config.database)

    conn.execute("""
    CREATE TABLE IF NOT EXISTS wallpapers (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        path TEXT UNIQUE NOT NULL,
        filename TEXT NOT NULL,
        extension TEXT NOT NULL,
        size INTEGER NOT NULL,
        width INTEGER NOT NULL,
        height INTEGER NOT NULL,
        sha256 TEXT NOT NULL,
        last_shown TIMESTAMP,
        times_shown INTEGER NOT NULL DEFAULT 0,
        favorite INTEGER NOT NULL DEFAULT 0,
        rating INTEGER NOT NULL DEFAULT 0
    );
    """)

    conn.commit()

    return conn
