from pathlib import Path
import random
import sys
import time

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import (
    MediaFileUpload,
    MediaIoBaseDownload,
)

from wallsync import config
from wallsync import config
from wallsync.config import Config


class GoogleDriveProvider:
    SCOPES = ["https://www.googleapis.com/auth/drive"]

    def __init__(self):
        from wallsync.config import Config

        config = Config()
        token_file = config.token

        self.creds = Credentials.from_authorized_user_file(
            token_file,
            self.SCOPES,
        )

        self.service = build(
            "drive",
            "v3",
            credentials=self.creds,
        )

        self.folder_id = self.get_repo_folder()["id"]

    def get_repo_folder(self, folder_name="Wallsync_repo"):
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

    def list_files(self):
        results = (
            self.service.files()
            .list(
                q=f"'{self.folder_id}' in parents and trashed=false",
                fields="files(id,name,mimeType,size)",
            )
            .execute()
        )

        return results.get("files", [])

    def list_wallpapers(self):
        return [f for f in self.list_files() if f["mimeType"].startswith("image/")]

    def random_wallpaper(self):
        wallpapers = self.list_wallpapers()

        if not wallpapers:
            raise RuntimeError("No wallpapers found.")

        return random.choice(wallpapers)

    def upload_wallpaper(self, file_path):
        metadata = {
            "name": Path(file_path).name,
            "parents": [self.folder_id],
        }

        media = MediaFileUpload(file_path, resumable=True)

        return (
            self.service.files()
            .create(
                body=metadata,
                media_body=media,
                fields="id,name,mimeType",
            )
            .execute()
        )

    def download_wallpaper(self, file_id, destination):
        destination = Path(destination)
        destination.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        filename = destination.name

        request = self.service.files().get_media(fileId=file_id)

        spinner = ["|", "/", "-", "\\"]
        frame = 0

        try:
            with destination.open("wb") as f:
                downloader = MediaIoBaseDownload(
                    f,
                    request,
                )

                done = False

                while not done:
                    status, done = downloader.next_chunk()

                    sys.stdout.write(
                        f"\r\033[36m[{spinner[frame]}]\033[0m Downloading {filename}"
                    )
                    sys.stdout.flush()

                    frame = (frame + 1) % len(spinner)

                    time.sleep(0.03)

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

    def delete_wallpaper(self, file_id):
        self.service.files().delete(fileId=file_id).execute()

    def get_file(self, file_id):
        return (
            self.service.files()
            .get(
                fileId=file_id,
                fields="id,name,mimeType,size,modifiedTime",
            )
            .execute()
        )
