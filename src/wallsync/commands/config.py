import json
from typing import Optional

from wallsync.config import get_config

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"


def run(action: str = "list", key: Optional[str] = None, value: Optional[str] = None):
    config = get_config()

    if action == "list":
        print(f"{CYAN}WallSync Configuration Settings{RESET}")
        print("──────────────────────────────────────────────────────")
        for k, v in config.to_dict().items():
            print(f"{k:<24} : {v}")

    elif action == "get":
        if not key:
            print(f"{RED}[✗]{RESET} Missing key argument.")
            return
        if hasattr(config, key):
            print(f"{key} = {getattr(config, key)}")
        else:
            print(f"{RED}[✗]{RESET} Unknown configuration key: {key}")

    elif action == "set":
        if not key or value is None:
            print(f"{RED}[✗]{RESET} Usage: wallsync config set <key> <value>")
            return
        if not hasattr(config, key) or key.endswith("_dir") or key.endswith("_file"):
            print(f"{RED}[✗]{RESET} Unknown or read-only configuration key: {key}")
            return

        curr_val = getattr(config, key)
        parsed_val: any = value

        if isinstance(curr_val, bool):
            parsed_val = value.lower() in ("true", "1", "yes", "on")
        elif isinstance(curr_val, int):
            try:
                parsed_val = int(value)
            except ValueError:
                print(f"{RED}[✗]{RESET} Value for {key} must be an integer.")
                return

        setattr(config, key, parsed_val)
        config.save()
        print(f"{GREEN}[✓]{RESET} Updated {key} = {parsed_val}")
