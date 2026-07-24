from pathlib import Path
from typing import Any, Dict, List, Optional

from wallsync.providers.base import BaseProvider

MEGA_AVAILABLE = False
try:
    from mega import Mega
    MEGA_AVAILABLE = True
except Exception:
    MEGA_AVAILABLE = False


class MegaProvider(BaseProvider):
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

    def __init__(
        self,
        folder_url_or_name: str,
        email: Optional[str] = None,
        password: Optional[str] = None,
        repo_name: str = "MEGA Wallpapers",
    ):
        self.folder_target = folder_url_or_name
        self.email = email
        self.password = password
        self._name = repo_name
        self._m = None

    def _login(self):
        if not MEGA_AVAILABLE:
            raise RuntimeError(
                "MEGA library is not compatible or available in Python environment."
            )
        if self._m is None:
            mega = Mega()
            if self.email and self.password:
                self._m = mega.login(self.email, self.password)
            else:
                self._m = mega.login()

    @property
    def provider_type(self) -> str:
        return "mega"

    @property
    def name(self) -> str:
        return self._name

    def list_wallpapers(self) -> List[Dict[str, Any]]:
        if not MEGA_AVAILABLE:
            return []
        try:
            self._login()
            wallpapers = []
            if self.folder_target.startswith("http"):
                files = self._m.get_public_url_info(self.folder_target)
                if isinstance(files, dict):
                    for handle, file_info in files.items():
                        name = file_info.get("a", {}).get("n", "")
                        ext = Path(name).suffix.lower()
                        if ext in self.SUPPORTED_EXTENSIONS:
                            wallpapers.append(
                                {
                                    "id": f"mega_{handle}",
                                    "name": name,
                                    "size": file_info.get("s", 0),
                                    "mimeType": f"image/{ext.lstrip('.')}",
                                    "provider_type": self.provider_type,
                                    "repo_name": self.name,
                                    "handle": handle,
                                }
                            )
            return wallpapers
        except Exception:
            return []

    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        self._login()
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        handle = file_id.replace("mega_", "")
        try:
            temp_path = self._m.download_by_upload_gfile((handle, None), dest_path=str(destination.parent))
            if temp_path and Path(temp_path).exists():
                Path(temp_path).rename(destination)
                return destination
        except Exception:
            pass

        if destination.exists() and destination.stat().st_size > 0:
            return destination
        raise RuntimeError(f"Failed to download wallpaper '{file_id}' from MEGA.")
