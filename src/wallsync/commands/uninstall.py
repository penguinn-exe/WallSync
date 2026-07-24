from pathlib import Path
import shutil
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

SERVICE = Path.home() / ".config/systemd/user/wallsync.service"
TIMER = Path.home() / ".config/systemd/user/wallsync.timer"


def run():
    if shutil.which("systemctl") is None:
        print(f"{RED}[✗]{RESET} systemd is not available.")
        return

    try:
        subprocess.run(
            ["systemctl", "--user", "disable", "--now", "wallsync.timer"],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        SERVICE.unlink(missing_ok=True)
        TIMER.unlink(missing_ok=True)

        subprocess.run(
            ["systemctl", "--user", "daemon-reload"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(f"{GREEN}[✓]{RESET} WallSync service removed.")
        print(f"{YELLOW}[i]{RESET} Timer    : Disabled")

    except subprocess.CalledProcessError:
        print(f"{RED}[✗]{RESET} Failed to remove WallSync service.")
