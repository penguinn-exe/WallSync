from pathlib import Path
from typing import Any, Dict, List, Optional

from wallsync.config import Config, get_config
from wallsync.providers.base import BaseProvider
from wallsync.providers.gdrive import GoogleDriveProvider
from wallsync.providers.gdrive_public import GoogleDrivePublicProvider
from wallsync.providers.local import LocalProvider
from wallsync.providers.mega import MegaProvider


class CompositeProvider(BaseProvider):
    def __init__(self, config: Optional[Config] = None):
        self.config = config or get_config()
        self.providers: List[BaseProvider] = []
        self._init_providers()

    def _init_providers(self):
        self.providers = []
        repositories = getattr(self.config, "repositories", [])

        if not repositories:
            repositories = [
                {"name": "Local Wallpapers", "type": "local", "enabled": True, "path": "~/Pictures/Wallpapers"},
            ]

        for repo in repositories:
            if not repo.get("enabled", True):
                continue
            r_type = repo.get("type")
            r_name = repo.get("name", "Repository")

            if r_type == "gdrive":
                try:
                    p = GoogleDriveProvider(
                        token_file=self.config.token_file,
                        folder_name=repo.get("folder", self.config.drive_folder_name),
                        repo_name=r_name,
                    )
                    self.providers.append(p)
                except Exception:
                    pass

            elif r_type == "gdrive_public":
                try:
                    p = GoogleDrivePublicProvider(
                        folder_url_or_id=repo.get("url") or repo.get("folder", ""),
                        repo_name=r_name,
                    )
                    self.providers.append(p)
                except Exception:
                    pass

            elif r_type == "local":
                try:
                    p = LocalProvider(
                        path=repo.get("path", "~/Pictures/Wallpapers"),
                        repo_name=r_name,
                    )
                    self.providers.append(p)
                except Exception:
                    pass

            elif r_type == "mega":
                try:
                    p = MegaProvider(
                        folder_url_or_name=repo.get("folder", ""),
                        email=repo.get("email"),
                        password=repo.get("password"),
                        repo_name=r_name,
                    )
                    self.providers.append(p)
                except Exception:
                    pass

    @property
    def provider_type(self) -> str:
        return "composite"

    @property
    def name(self) -> str:
        return f"Composite Engine ({len(self.providers)} repos active)"

    def list_wallpapers(self) -> List[Dict[str, Any]]:
        all_wallpapers = []
        for provider in self.providers:
            try:
                all_wallpapers.extend(provider.list_wallpapers())
            except Exception:
                pass
        return all_wallpapers

    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        for provider in self.providers:
            try:
                for w in provider.list_wallpapers():
                    if w["id"] == file_id:
                        return provider.download_wallpaper(file_id, destination)
            except Exception:
                pass
        raise RuntimeError(f"Wallpaper ID '{file_id}' could not be downloaded from any active provider.")

    def upload_wallpaper(self, file_path: str) -> Dict[str, Any]:
        if not self.providers:
            raise RuntimeError("No active providers configured to upload wallpaper.")
        return self.providers[0].upload_wallpaper(file_path)

    def delete_wallpaper(self, file_id: str) -> None:
        for provider in self.providers:
            try:
                provider.delete_wallpaper(file_id)
                return
            except Exception:
                pass
