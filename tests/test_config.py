from pathlib import Path
from wallsync.config import Config


def test_config_defaults(tmp_path: Path):
    cfg = Config(
        config_dir=tmp_path / "config",
        cache_dir=tmp_path / "cache",
        data_dir=tmp_path / "data",
        log_dir=tmp_path / "log",
    )
    assert cfg.provider == "composite"
    assert cfg.drive_folder_name == "Wallsync_repo"
    assert cfg.queue_size == 3
    assert cfg.enable_notifications is True


def test_config_save_and_load(tmp_path: Path):
    cfg = Config(
        config_dir=tmp_path / "config",
        cache_dir=tmp_path / "cache",
        data_dir=tmp_path / "data",
        log_dir=tmp_path / "log",
        queue_size=5,
        drive_folder_name="CustomFolder",
    )
    cfg.save()

    assert cfg.config_file.exists()

    loaded = Config(
        config_dir=tmp_path / "config",
        cache_dir=tmp_path / "cache",
        data_dir=tmp_path / "data",
        log_dir=tmp_path / "log",
    ).load()

    assert loaded.queue_size == 5
    assert loaded.drive_folder_name == "CustomFolder"
