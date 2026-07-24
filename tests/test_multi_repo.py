from pathlib import Path

from wallsync.config import Config
from wallsync.providers.composite import CompositeProvider
from wallsync.providers.gdrive_public import extract_folder_id
from wallsync.providers.local import LocalProvider


def test_extract_folder_id():
    url1 = "https://drive.google.com/drive/folders/1abc123XYZ_456"
    assert extract_folder_id(url1) == "1abc123XYZ_456"

    url2 = "https://drive.google.com/open?id=987zyx321"
    assert extract_folder_id(url2) == "987zyx321"

    plain_id = "1abc123XYZ_456"
    assert extract_folder_id(plain_id) == "1abc123XYZ_456"


def test_local_provider_scanning(tmp_path: Path):
    wallpaper_dir = tmp_path / "wallpapers"
    wallpaper_dir.mkdir(parents=True)

    file1 = wallpaper_dir / "sample1.jpg"
    file1.write_bytes(b"dummy image content 1")
    file2 = wallpaper_dir / "sample2.png"
    file2.write_bytes(b"dummy image content 2")

    provider = LocalProvider(str(wallpaper_dir), repo_name="Test Local")
    wallpapers = provider.list_wallpapers()

    assert len(wallpapers) == 2
    names = {w["name"] for w in wallpapers}
    assert "sample1.jpg" in names
    assert "sample2.png" in names


def test_composite_provider_pooling(tmp_path: Path):
    dir1 = tmp_path / "repo1"
    dir1.mkdir()
    (dir1 / "wall1.jpg").write_bytes(b"img1")

    dir2 = tmp_path / "repo2"
    dir2.mkdir()
    (dir2 / "wall2.png").write_bytes(b"img2")

    cfg = Config(
        config_dir=tmp_path / "config",
        cache_dir=tmp_path / "cache",
        data_dir=tmp_path / "data",
        log_dir=tmp_path / "log",
        repositories=[
            {"name": "Local Repo 1", "type": "local", "enabled": True, "path": str(dir1)},
            {"name": "Local Repo 2", "type": "local", "enabled": True, "path": str(dir2)},
        ],
    )

    composite = CompositeProvider(cfg)
    wallpapers = composite.list_wallpapers()

    assert len(wallpapers) == 2
    names = {w["name"] for w in wallpapers}
    assert "wall1.jpg" in names
    assert "wall2.png" in names
