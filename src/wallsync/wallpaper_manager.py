import platform

if platform.system() == "Linux":
    from .platform.linux import set_wallpaper

elif platform.system() == "Windows":
    from .platform.windows import set_wallpaper

else:
    raise NotImplementedError(
        f"Unsupported operating system: {platform.system()}"
    )