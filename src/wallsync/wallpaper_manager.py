import os
import shutil
import subprocess
from pathlib import Path
from typing import Tuple


def detect_desktop_environment() -> str:
    desktop = os.environ.get("XDG_CURRENT_DESKTOP", "").lower()
    if "gnome" in desktop:
        return "gnome"
    elif "kde" in desktop or "plasma" in desktop:
        return "kde"
    elif "cinnamon" in desktop:
        return "cinnamon"
    elif "mate" in desktop:
        return "mate"
    elif "xfce" in desktop:
        return "xfce"
    elif "sway" in desktop or "hyprland" in desktop:
        return "wayland"

    if shutil.which("gsettings"):
        return "gnome"
    elif shutil.which("plasma-apply-wallpaperimage"):
        return "kde"
    elif shutil.which("swww"):
        return "wayland"
    elif shutil.which("feh"):
        return "feh"

    return "gnome"


def set_wallpaper(path: str, desktop: str = "auto", light_dark: bool = True, lock_screen: bool = True) -> Tuple[bool, str]:
    wallpaper = Path(path).resolve()
    if not wallpaper.exists():
        raise FileNotFoundError(f"Wallpaper file not found: {path}")

    uri = f"file://{wallpaper}"
    target_desktop = detect_desktop_environment() if desktop == "auto" else desktop.lower()

    if target_desktop == "gnome":
        try:
            subprocess.run(
                ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            if light_dark:
                subprocess.run(
                    ["gsettings", "set", "org.gnome.desktop.background", "picture-uri-dark", uri],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            if lock_screen:
                subprocess.run(
                    ["gsettings", "set", "org.gnome.desktop.screensaver", "picture-uri", uri],
                    check=False,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                )
            return True, "GNOME"
        except Exception as e:
            return False, f"GNOME gsettings error: {e}"

    elif target_desktop == "cinnamon":
        try:
            subprocess.run(
                ["gsettings", "set", "org.cinnamon.desktop.background", "picture-uri", uri],
                check=True,
            )
            return True, "Cinnamon"
        except Exception as e:
            return False, f"Cinnamon error: {e}"

    elif target_desktop == "mate":
        try:
            subprocess.run(
                ["gsettings", "set", "org.mate.background", "picture-filename", str(wallpaper)],
                check=True,
            )
            return True, "MATE"
        except Exception as e:
            return False, f"MATE error: {e}"

    elif target_desktop == "kde":
        if shutil.which("plasma-apply-wallpaperimage"):
            try:
                subprocess.run(["plasma-apply-wallpaperimage", str(wallpaper)], check=True)
                return True, "KDE Plasma"
            except Exception as e:
                return False, f"KDE error: {e}"

    elif target_desktop in ("wayland", "swww"):
        if shutil.which("swww"):
            try:
                subprocess.run(["swww", "img", str(wallpaper)], check=True)
                return True, "swww (Wayland)"
            except Exception as e:
                return False, f"swww error: {e}"

    if shutil.which("feh"):
        try:
            subprocess.run(["feh", "--bg-fill", str(wallpaper)], check=True)
            return True, "feh"
        except Exception as e:
            return False, f"feh error: {e}"

    # Default fallback to GNOME
    try:
        subprocess.run(
            ["gsettings", "set", "org.gnome.desktop.background", "picture-uri", uri],
            check=True,
        )
        return True, "GNOME (fallback)"
    except Exception as e:
        return False, str(e)
