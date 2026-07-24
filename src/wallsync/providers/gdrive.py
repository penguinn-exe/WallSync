import random
import sys
import time
from pathlib import Path
from typing import Any, Dict, List, Optional

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload, MediaIoBaseDownload

from wallsync.config import get_config
from wallsync.providers.base import BaseProvider


class GoogleDriveProvider(BaseProvider):
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(
        self,
        token_file: Optional[Path] = None,
        folder_name: Optional[str] = None,
        repo_name: str = "Google Drive Main",
    ):
        config = get_config()
        self.token_file = token_file or config.token_file
        self.folder_name = folder_name or config.drive_folder_name
        self._name = repo_name

        if not self.token_file.exists():
            raise FileNotFoundError(
                f"Token file not found at {self.token_file}. Run 'wallsync login' first."
            )

        self.creds = Credentials.from_authorized_user_file(
            str(self.token_file),
            self.SCOPES,
        )

        self.service = build(
            "drive",
            "v3",
            credentials=self.creds,
        )

        self.folder_id = self.get_repo_folder(self.folder_name)["id"]

    @property
    def provider_type(self) -> str:
        return "gdrive"

    @property
    def name(self) -> str:
        return self._name

    def get_repo_folder(self, folder_name: str) -> Dict[str, Any]:
        for attempt in range(3):
            try:
                results = (
                    self.service.files()
                    .list(
                        q=(
                            f"name='{folder_name}' and "
                            "mimeType='application/vnd.google-apps.folder' and "
                            "trashed=false"
                        ),
                        fields="files(id,name)",
                        pageSize=1,
                    )
                    .execute()
                )
                folders = results.get("files", [])
                if not folders:
                    raise FileNotFoundError(f"Google Drive folder '{folder_name}' not found.")
                return folders[0]
            except Exception:
                if attempt == 2:
                    raise
                time.sleep(1)
        raise FileNotFoundError(f"Google Drive folder '{folder_name}' not found.")

    def list_files(self) -> List[Dict[str, Any]]:
        results = (
            self.service.files()
            .list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                fields="files(id,name,mimeType,size)",
            )
            .execute()
        )
        return results.get("files", [])

    def list_wallpapers(self) -> List[Dict[str, Any]]:
        raw_files = self.list_files()
        wallpapers = []
        for f in raw_files:
            if f.get("mimeType", "").startswith("image/"):
                wallpapers.append(
                    {
                        "id": f["id"],
                        "name": f["name"],
                        "size": int(f.get("size", 0)),
                        "mimeType": f.get("mimeType", "image/jpeg"),
                        "provider_type": self.provider_type,
                        "repo_name": self.name,
                    }
                )
        return wallpapers

    def random_wallpaper(self) -> Dict[str, Any]:
        wallpapers = self.list_wallpapers()
        if not wallpapers:
            raise RuntimeError("No wallpapers found in Google Drive folder.")
        return random.choice(wallpapers)

    def upload_wallpaper(self, file_path: str) -> Dict[str, Any]:
        path = Path(file_path)
        metadata = {
            "name": path.name,
            "parents": [self.folder_id],
        }
        media = MediaFileUpload(str(path), resumable=True)
        res = (
            self.service.files()
            .create(
                body=metadata,
                media_body=media,
                fields="id,name,mimeType,size",
            )
            .execute()
        )
        res["provider_type"] = self.provider_type
        res["repo_name"] = self.name
        return res

    def download_wallpaper(self, file_id: str, destination: Path) -> Path:
        destination = Path(destination)
        destination.parent.mkdir(parents=True, exist_ok=True)

        filename = destination.name
        request = self.service.files().get_media(fileId=file_id)

        spinner = ["|", "/", "-", "\\"]
        frame = 0

        try:
            with destination.open("wb") as f:
                downloader = MediaIoBaseDownload(f, request)
                done = False
                while not done:
                    status, done = downloader.next_chunk()
                    sys.stdout.write(
                        f"\r\033[36m[{spinner[frame]}]\033[0m Downloading {filename}"
                    )
                    sys.stdout.flush()
                    frame = (frame + 1) % len(spinner)
                    time.sleep(0.02)

            if destination.stat().st_size == 0:
                destination.unlink(missing_ok=True)
                raise RuntimeError("Downloaded file is empty.")

            sys.stdout.write(f"\r\033[32m[✓]\033[0m Downloaded {filename}\n")
            sys.stdout.flush()
            return destination

        except Exception:
            destination.unlink(missing_ok=True)
            sys.stdout.write(f"\r\033[31m[✗]\033[0m Failed downloading {filename}\n")
            sys.stdout.flush()
            raise

    def delete_wallpaper(self, file_id: str) -> None:
        self.service.files().delete(fileId=file_id).execute()
