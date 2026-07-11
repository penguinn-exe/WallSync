from importlib.resources import files
from pathlib import Path
import shutil

from google_auth_oauthlib.flow import InstalledAppFlow

GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

SCOPES = ["https://www.googleapis.com/auth/drive"]

CONFIG_DIR = Path.home() / ".config" / "wallsync"
CONFIG_DIR.mkdir(parents=True, exist_ok=True)

CREDENTIALS = CONFIG_DIR / "credentials.json"
TOKEN = CONFIG_DIR / "token.json"


def ensure_credentials():
    """Copy the bundled OAuth client to the user's config directory."""
    if CREDENTIALS.exists():
        return

    source = files("wallsync").joinpath("credentials.json")

    shutil.copy2(source, CREDENTIALS)


def run():
    try:
        ensure_credentials()

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CREDENTIALS),
            SCOPES,
        )

        creds = flow.run_local_server(port=0)

        TOKEN.write_text(creds.to_json())

        print(f"{GREEN}[✓]{RESET} Login successful.")

    except FileNotFoundError:
        print(
            f"{RED}[✗]{RESET} Bundled credentials.json was not found.\n"
            "Reinstall WallSync."
        )

    except Exception as e:
        print(f"{RED}[✗]{RESET} {e}")
