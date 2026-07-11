import subprocess
from pathlib import Path

GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
CYAN = "\033[36m"
RESET = "\033[0m"

TIMER = Path.home() / ".config/systemd/user/wallsync.timer"


def _run(command):
    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def run():
    if not TIMER.exists():
        print(f"{RED}[✗]{RESET} WallSync is not installed.")
        print(f"{YELLOW}[i]{RESET} Run 'wallsync install' first.")
        return

    active = _run(
        [
            "systemctl",
            "--user",
            "is-active",
            "wallsync.timer",
        ]
    )

    interval = _run(
        [
            "systemctl",
            "--user",
            "show",
            "wallsync.timer",
            "--property=OnUnitActiveUSec",
            "--value",
        ]
    )

    next_run = _run(
        [
            "systemctl",
            "--user",
            "show",
            "wallsync.timer",
            "--property=NextElapseUSecRealtime",
            "--value",
        ]
    )

    print(f"{CYAN}WallSync Service{RESET}")
    print("──────────────────────────────")

    if active == "active":
        print(f"Status   : {GREEN}Running{RESET}")
    else:
        print(f"Status   : {RED}Stopped{RESET}")

    if interval:
        print(f"Interval : {interval}")

    if next_run:
        print(f"Next Run : {next_run}")
