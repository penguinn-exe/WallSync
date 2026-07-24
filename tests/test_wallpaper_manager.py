from pathlib import Path
import pytest
from wallsync.wallpaper_manager import detect_desktop_environment, set_wallpaper


def test_detect_desktop_environment(monkeypatch):
    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "GNOME")
    assert detect_desktop_environment() == "gnome"

    monkeypatch.setenv("XDG_CURRENT_DESKTOP", "KDE")
    assert detect_desktop_environment() == "kde"


def test_set_wallpaper_missing_file(tmp_path: Path):
    non_existent = tmp_path / "missing.jpg"
    with pytest.raises(FileNotFoundError):
        set_wallpaper(str(non_existent))
