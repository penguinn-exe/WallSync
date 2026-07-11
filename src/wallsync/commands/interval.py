from pathlib import Path
import shutil
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

SERVICE = Path.home() / ".config/systemd/user/wallsync.service"
TIMER = Path.home() / ".config/systemd/user/wallsync.timer"


def run(minutes):
    if shutil.which("systemctl") is None:
        print(f"{RED}[✗]{RESET} systemd is not available.")
        return

    if not TIMER.exists():
        print(f"{RED}[✗]{RESET} WallSync is not installed.")
        print(f"{YELLOW}[i]{RESET} Run 'wallsync install' first.")
        return

    try:
        minutes = int(minutes)

        if minutes < 1:
            raise ValueError

    except ValueError:
        print(f"{RED}[✗]{RESET} Interval must be a positive integer.")
        return

    TIMER.write_text(
        f"""[Unit]
Description=Run WallSync every {minutes} minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec={minutes}min
Unit=wallsync.service

[Install]
WantedBy=timers.target
"""
    )

    try:
        subprocess.run(
            ["systemctl", "--user", "daemon-reload"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        subprocess.run(
            ["systemctl", "--user", "restart", "wallsync.timer"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(f"{GREEN}[✓]{RESET} Wallpaper rotation interval updated.")
        print(f"{YELLOW}[i]{RESET} Interval : {minutes} minutes")

    except subprocess.CalledProcessError:
        print(f"{RED}[✗]{RESET} Failed to restart WallSync timer.")
