from pathlib import Path
from wallsync.db import Database


def test_db_operations(tmp_path: Path):
    db_file = tmp_path / "test_wallsync.db"
    db = Database(db_file)

    db.upsert_wallpaper("img1", "wallpaper1.jpg", file_size=1024)
    db.upsert_wallpaper("img2", "wallpaper2.jpg", file_size=2048)

    stats = db.get_stats()
    assert stats["total"] == 2
    assert stats["never_shown"] == 2

    # Record view
    db.record_view("img1", "wallpaper1.jpg")

    stats2 = db.get_stats()
    assert stats2["never_shown"] == 1
    assert len(stats2["most_shown"]) == 1
    assert stats2["most_shown"][0]["id"] == "img1"

    # Test Favorites
    db.set_favorite("img1", True)
    favs = db.list_favorites()
    assert len(favs) == 1
    assert favs[0]["id"] == "img1"

    # Test Tags
    db.add_tag("img1", "nature")
    tags = db.get_tags("img1")
    assert "nature" in tags
