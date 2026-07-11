# WallSync

A minimal command-line wallpaper rotator for **GNOME** that uses **Google Drive** as its wallpaper repository.

WallSync downloads wallpapers from Google Drive, maintains a lightweight local cache, avoids repeats until every wallpaper has been shown, and can automatically rotate wallpapers in the background using a systemd user timer.

---

## Features

- Google Drive-backed wallpaper library
- Lightweight local wallpaper cache
- Random wallpaper rotation
- No repeated wallpapers until every wallpaper has been shown
- Delete wallpapers directly from Google Drive
- Upload a wallpaper or an entire folder
- Wallpaper information command
- Automatic background rotation
- Configurable rotation interval
- Lightweight ANSI terminal interface
- Automatic corrupted download cleanup
- systemd user service integration

---

## Supported Desktop

Currently supported:

- ✅ GNOME

Planned:

- KDE Plasma
- Cinnamon
- XFCE
- MATE

---

## Requirements

- Linux
- GNOME
- Python 3.11+
- uv
- Google account
- Google Drive API enabled

---

## Installation

```bash
git clone https://github.com/penguinn-exe/WallSync.git
cd WallSync

uv sync
uv tool install .
```

Verify the installation:

```bash
wallsync --help
```

---

## Google Cloud Setup

1. Create a Google Cloud project.
2. Enable the Google Drive API.
3. Configure the OAuth Consent Screen.
4. Create an OAuth Desktop Client.
5. Download `credentials.json`.
6. Place it in:

```text
~/.config/wallsync/
```

Result:

```text
~/.config/wallsync/
└── credentials.json
```

---

## Google Drive Setup

Create a folder named:

```text
Wallsync_repo
```

Upload your wallpapers into this folder.

Supported image formats:

- jpg
- jpeg
- png
- webp

---

## Authentication

Authenticate once:

```bash
wallsync login
```

A browser window will open.

After authentication a `token.json` file is automatically created inside:

```text
~/.config/wallsync/
```

---

# Commands

### Apply the next wallpaper

```bash
wallsync next
```

---

### Upload wallpapers

Single image:

```bash
wallsync upload ~/Pictures/wallpaper.png
```

Entire folder:

```bash
wallsync upload ~/Pictures/Wallpapers
```

---

### Delete current wallpaper

```bash
wallsync delete
```

Skip confirmation:

```bash
wallsync delete --force
```

---

### Show wallpaper information

```bash
wallsync info
```

---

### Install automatic wallpaper rotation

```bash
wallsync install
```

---

### Remove automatic wallpaper rotation

```bash
wallsync uninstall
```

---

### Change rotation interval

```bash
wallsync interval 30
```

Example:

```bash
wallsync interval 60
```

---

### Service status

```bash
wallsync status
```

---

## Example

```text
$ wallsync next

[/] Downloading 0054.jpg
[-] Downloading 0054.jpg
[\] Downloading 0054.jpg
[|] Downloading 0054.jpg
[✓] Downloaded 0054.jpg

[✓] Applied: 0054.jpg (4.82 MB)
[i] Cache: 3/3
```

---

## Wallpaper Information

```text
$ wallsync info

WallSync Status
──────────────────────────────
Current : 0054.jpg
Size    : 4.82 MB
Drive   : 52 wallpapers
Cache   : 3 wallpapers • 18.42 MB
```

---

## Service Status

```text
$ wallsync status

WallSync Service
──────────────────────────────
Status   : Running
Interval : 30min
Next Run : Mon 21 Jul 15:30:00 IST
```

---

## How It Works

- Searches Google Drive for a folder named `Wallsync_repo`
- Downloads wallpapers as needed
- Maintains a local cache
- Prevents repeats until every wallpaper has been shown
- Automatically rotates wallpapers using a systemd user timer
- Deletes wallpapers directly from Google Drive when requested

---

## File Locations

Configuration:

```text
~/.config/wallsync/
├── credentials.json
└── token.json
```

Cache:

```text
~/.cache/wallsync/
├── queue.json
├── state.json
└── wallpapers...
```

systemd:

```text
~/.config/systemd/user/
├── wallsync.service
└── wallsync.timer
```

---

## Project Structure

```text
WallSync
├── LICENSE
├── README.md
├── pyproject.toml
├── uv.lock
└── src
    └── wallsync
        ├── cli.py
        ├── config.py
        ├── wallpaper_manager.py
        ├── commands
        ├── providers
        └── __main__.py
```

---

## Roadmap

- Bundle OAuth client for easier setup
- Multi-desktop support
- Custom Google Drive folder names
- Wallpaper history
- Optional wallpaper metadata

---

## Contributing

Contributions, bug reports and feature requests are welcome.

Please open an issue or submit a pull request.

---

## Author

Created and maintained by **penguin**

GitHub: https://github.com/penguinn-exe

If you find WallSync useful, consider giving the repository a ⭐.

---

## License

This project is licensed under the MIT License.
