import shutil
from pathlib import Path
from typing import Any, Dict, List

from wallsync.providers.base import BaseProvider


class LocalProvider(BaseProvider):
    SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}

    def __init__(self, path: str, repo_name: str = "Local Wallpapers"):
        self.directory = Path(path).expanduser().resolve()
        self._name = repo_name
        self.directory.mkdir(parents=True, exist_ok=True)

    @property
    def provider_type(self) -> str:
        return "local"

    @property
    def name(self) -> str:
        return self._name

    def list_wallpapers(self) -> List[Dict[str, Any]]:
        wallpapers = []
        if not self.directory.exists():
            return wallpapers

        for ext in self.SUPPORTED_EXTENSIONS:
            for file_path in self.directory.rglob(f"*{ext}"):
                if file_path.is_file():
                    rel_id = f"local_{file_path.name}_{file_path.stat().st_size}"
                    wallpapers.append(
                        {
                            "id": rel_id,
                            "name": file_path.name,
                            "size": file_path.stat().st_size,
                            "mimeType": f"image/{file_path.suffix.lstrip('.')}",
                            "provider_type": self.provider_type,
                            "repo_name": self.name,
                            "local_path": str(file_path),
                        }
                    )
        return sorted(wallpapers, key=lambda x: x["name"])

    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        for w in self.list_wallpapers():
            if w["id"] == file_id:
                source = Path(w["local_path"])
                shutil.copy2(source, destination)
                return destination

        raise FileNotFoundError(f"Local wallpaper with ID '{file_id}' not found.")

    def upload_wallpaper(self, file_path: str) -> Dict[str, Any]:
        source = Path(file_path).expanduser().resolve()
        if not source.exists():
            raise FileNotFoundError(f"Source file not found: {file_path}")

        dest = self.directory / source.name
        shutil.copy2(source, dest)
        return {
            "id": f"local_{dest.name}_{dest.stat().st_size}",
            "name": dest.name,
            "size": dest.stat().st_size,
            "mimeType": f"image/{dest.suffix.lstrip('.')}",
            "provider_type": self.provider_type,
            "repo_name": self.name,
            "local_path": str(dest),
        }

    def delete_wallpaper(self, file_id: str) -> None:
        for w in self.list_wallpapers():
            if w["id"] == file_id:
                Path(w["local_path"]).unlink(missing_ok=True)
                return
