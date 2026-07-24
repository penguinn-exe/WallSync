from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Dict, List


class BaseProvider(ABC):
    @property
    @abstractmethod
    def provider_type(self) -> str:
        """Return the provider type string identifier (e.g., 'gdrive', 'mega', 'local')."""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Return the friendly repository name."""
        pass

    @abstractmethod
    def list_wallpapers(self) -> List[Dict[str, Any]]:
        """List wallpapers available in the repository.
        Returns a list of dicts containing:
          - id: unique identifier
          - name: filename
          - size: file size in bytes
          - mimeType: mime type string
          - provider_type: provider name
          - repo_name: friendly repo name
        """
        pass

    @abstractmethod
    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        """Download or copy a wallpaper to local destination path."""
        pass

    def upload_wallpaper(self, file_path: str) -> Dict[str, Any]:
        """Upload a wallpaper to the repository."""
        raise NotImplementedError("Upload is not supported by this provider.")

    def delete_wallpaper(self, file_id: str) -> None:
        """Delete a wallpaper from the repository."""
        raise NotImplementedError("Delete is not supported by this provider.")
