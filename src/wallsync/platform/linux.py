import subprocess
from pathlib import Path


def set_wallpaper(path: str):
    wallpaper = Path(path).resolve()

    uri = f"file://{wallpaper}"

    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri",
            uri,
        ],
        check=True,
    )

    subprocess.run(
        [
            "gsettings",
            "set",
            "org.gnome.desktop.background",
            "picture-uri-dark",
            uri,
        ],
        check=True,
    )
