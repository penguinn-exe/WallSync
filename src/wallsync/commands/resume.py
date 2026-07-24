from pathlib import Path
import shutil
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

TIMER = Path.home() / ".config/systemd/user/wallsync.timer"


def run():
    if shutil.which("systemctl") is None:
        print(f"{RED}[✗]{RESET} systemd is not available.")
        return

    if not TIMER.exists():
        print(f"{RED}[✗]{RESET} WallSync is not installed.")
        print(f"{YELLOW}[i]{RESET} Run 'wallsync install' first.")
        return

    active = subprocess.run(
        ["systemctl", "--user", "is-active", "wallsync.timer"],
        capture_output=True,
        text=True,
    ).stdout.strip()

    if active == "active":
        print(f"{YELLOW}[i]{RESET} WallSync is already running.")
        return

    try:
        subprocess.run(
            ["systemctl", "--user", "start", "wallsync.timer"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        print(f"{GREEN}[✓]{RESET} WallSync resumed.")
        print(f"{YELLOW}[i]{RESET} Run 'wallsync status' to check the timer.")

    except subprocess.CalledProcessError:
        print(f"{RED}[✗]{RESET} Failed to resume WallSync timer.")
