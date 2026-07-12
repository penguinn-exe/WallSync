import ctypes
from pathlib import Path

SPI_SETDESKWALLPAPER = 20
SPIF_UPDATEINIFILE = 0x01
SPIF_SENDCHANGE = 0x02


def set_wallpaper(path: str):
    wallpaper = str(Path(path).resolve())

    success = ctypes.windll.user32.SystemParametersInfoW(
        SPI_SETDESKWALLPAPER,
        0,
        wallpaper,
        SPIF_UPDATEINIFILE | SPIF_SENDCHANGE,
    )

    if not success:
        raise OSError("Failed to set wallpaper.")