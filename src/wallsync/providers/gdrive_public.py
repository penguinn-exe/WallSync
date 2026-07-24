import re
from pathlib import Path
from typing import Any, Dict, List

import gdown

from wallsync.providers.base import BaseProvider


def extract_folder_id(url_or_id: str) -> str:
    url_or_id = url_or_id.strip()
    match = re.search(r"folders/([a-zA-Z0-9_-]+)", url_or_id)
    if match:
        return match.group(1)
    match_id = re.search(r"id=([a-zA-Z0-9_-]+)", url_or_id)
    if match_id:
        return match_id.group(1)
    return url_or_id


class GoogleDrivePublicProvider(BaseProvider):
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

    def __init__(self, folder_url_or_id: str, repo_name: str = "Google Drive Public"):
        self.raw_target = folder_url_or_id
        self.folder_id = extract_folder_id(folder_url_or_id)
        self._name = repo_name

    @property
    def provider_type(self) -> str:
        return "gdrive_public"

    @property
    def name(self) -> str:
        return self._name

    def list_wallpapers(self) -> List[Dict[str, Any]]:
        wallpapers = []
        try:
            folder_url = f"https://drive.google.com/drive/folders/{self.folder_id}"
            # Use gdown to list public folder contents
            files = gdown.list_folder(url=folder_url, quiet=True, use_cookies=False)
            if files:
                for f in files:
                    ext = Path(f.name).suffix.lower()
                    if ext in self.SUPPORTED_EXTENSIONS:
                        wallpapers.append(
                            {
                                "id": f"gdrive_public_{f.id}",
                                "name": f.name,
                                "size": f.size if hasattr(f, "size") and f.size else 0,
                                "mimeType": f"image/{ext.lstrip('.')}",
                                "provider_type": self.provider_type,
                                "repo_name": self.name,
                                "file_id": f.id,
                                "download_url": f"https://drive.google.com/uc?id={f.id}",
                            }
                        )
        except Exception:
            pass
        return wallpapers

    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        drive_id = file_id.replace("gdrive_public_", "")
        url = f"https://drive.google.com/uc?id={drive_id}"

        try:
            res = gdown.download(url, str(destination), quiet=True, fuzzy=True)
            if res and Path(res).exists() and Path(res).stat().st_size > 0:
                return Path(res)
        except Exception as e:
            raise RuntimeError(f"Failed to download public file '{file_id}': {e}")

        if destination.exists() and destination.stat().st_size > 0:
            return destination
        raise RuntimeError(f"Failed to download public file '{file_id}' from Google Drive.")
