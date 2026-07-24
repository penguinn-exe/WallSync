from typing import Optional
from wallsync.config import get_config

CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run(
    action: str = "list",
    name: Optional[str] = None,
    repo_type: Optional[str] = None,
    target: Optional[str] = None,
):
    config = get_config()
    repos = config.repositories

    if action == "list":
        print(f"{CYAN}WallSync Active Repositories ({len(repos)}){RESET}")
        print("──────────────────────────────────────────────────────")
        for idx, r in enumerate(repos, 1):
            status = f"{GREEN}Enabled{RESET}" if r.get("enabled", True) else f"{YELLOW}Disabled{RESET}"
            r_type = r.get("type", "unknown").upper()
            target_info = r.get("url") or r.get("folder") or r.get("path") or "Default"
            print(f"{idx}. {r.get('name')} [{r_type}] - {target_info} ({status})")

    elif action == "add":
        if not name or not repo_type or not target:
            print(f"{RED}[✗]{RESET} Usage: wallsync repo add <name> <gdrive|gdrive_public|mega|local> <url_or_path>")
            return

        r_type = repo_type.lower()
        if r_type not in ("gdrive", "gdrive_public", "mega", "local"):
            print(f"{RED}[✗]{RESET} Invalid repo type '{repo_type}'. Supported: gdrive, gdrive_public, mega, local.")
            return

        new_repo = {
            "name": name,
            "type": r_type,
            "enabled": True,
        }
        if r_type == "local":
            new_repo["path"] = target
        elif r_type == "gdrive_public":
            new_repo["url"] = target
        else:
            new_repo["folder"] = target

        repos.append(new_repo)
        config.repositories = repos
        config.save()
        print(f"{GREEN}[✓]{RESET} Added repository '{name}' [{r_type.upper()}]. No API keys required!")

    elif action == "remove":
        if not name:
            print(f"{RED}[✗]{RESET} Usage: wallsync repo remove <name>")
            return

        filtered = [r for r in repos if r.get("name").lower() != name.lower()]
        if len(filtered) == len(repos):
            print(f"{RED}[✗]{RESET} Repository '{name}' not found.")
            return

        config.repositories = filtered
        config.save()
        print(f"{GREEN}[✓]{RESET} Removed repository '{name}'.")

    elif action == "toggle":
        if not name:
            print(f"{RED}[✗]{RESET} Usage: wallsync repo toggle <name>")
            return

        found = False
        for r in repos:
            if r.get("name").lower() == name.lower():
                r["enabled"] = not r.get("enabled", True)
                status_str = "enabled" if r["enabled"] else "disabled"
                print(f"{GREEN}[✓]{RESET} Repository '{r['name']}' is now {status_str}.")
                found = True
                break

        if not found:
            print(f"{RED}[✗]{RESET} Repository '{name}' not found.")
            return

        config.repositories = repos
        config.save()
