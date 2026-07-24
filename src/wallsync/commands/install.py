from pathlib import Path
import shutil
import subprocess

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"

SERVICE = Path.home() / ".config/systemd/user/wallsync.service"
TIMER = Path.home() / ".config/systemd/user/wallsync.timer"

DEFAULT_INTERVAL = 30


def run():
    if shutil.which("systemctl") is None:
        print(f"{RED}[✗]{RESET} systemd is not available.")
        return

    wallsync = shutil.which("wallsync")

    if wallsync is None:
        print(f"{RED}[✗]{RESET} wallsync executable not found.")
        return

    SERVICE.parent.mkdir(parents=True, exist_ok=True)

    SERVICE.write_text(
        f"""[Unit]
Description=WallSync Wallpaper Rotator

[Service]
Type=oneshot
ExecStart={wallsync} next
"""
    )

    TIMER.write_text(
        f"""[Unit]
Description=Run WallSync every {DEFAULT_INTERVAL} minutes

[Timer]
OnBootSec=1min
OnUnitActiveSec={DEFAULT_INTERVAL}min
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
            ["systemctl", "--user", "enable", "--now", "wallsync.timer"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )

        print(f"{GREEN}[✓]{RESET} WallSync service installed.")
        print(f"{YELLOW}[i]{RESET} Interval : {DEFAULT_INTERVAL} minutes")
        print(f"{YELLOW}[i]{RESET} Timer    : Active")

    except subprocess.CalledProcessError:
        print(f"{RED}[✗]{RESET} Failed to enable WallSync timer.")
