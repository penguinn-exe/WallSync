import argparse
import sys

from wallsync.commands.clean import run as clean
from wallsync.commands.config import run as config_cmd
from wallsync.commands.delete import run as delete
from wallsync.commands.favorite import run as favorite
from wallsync.commands.history import run as history
from wallsync.commands.info import run as info
from wallsync.commands.install import run as install
from wallsync.commands.interval import run as interval
from wallsync.commands.login import run as login
from wallsync.commands.next import run as next_wallpaper
from wallsync.commands.pause import run as pause
from wallsync.commands.prev import run as prev_wallpaper
from wallsync.commands.repo import run as repo_cmd
from wallsync.commands.reset import run as reset
from wallsync.commands.resume import run as resume
from wallsync.commands.stats import run as stats
from wallsync.commands.status import run as status
from wallsync.commands.sync import run as sync
from wallsync.commands.tag import run as tag
from wallsync.commands.uninstall import run as uninstall
from wallsync.commands.upload import run as upload


def main():
    parser = argparse.ArgumentParser(
        prog="wallsync",
        description="Google Drive, MEGA & Multi-Desktop Wallpaper Rotator",
    )

    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output",
    )
    parser.add_argument(
        "-q", "--quiet",
        action="store_true",
        help="Suppress non-error messages",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simulate operations without modifying wallpaper or state",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser("login", help="Authenticate with Google Drive API")

    next_parser = subparsers.add_parser("next", help="Apply the next wallpaper")
    next_parser.add_argument(
        "--preview", action="store_true", help="Preview the next queued wallpaper without applying"
    )

    subparsers.add_parser("prev", help="Switch back to the previous wallpaper in history")
    subparsers.add_parser("history", help="Show wallpaper history log")
    subparsers.add_parser("sync", help="Synchronize wallpaper library with Google Drive & active repos")
    subparsers.add_parser("info", help="Show wallpaper information and status")
    subparsers.add_parser("stats", help="Show detailed usage analytics")
    subparsers.add_parser("clean", help="Clean up local cached wallpaper files")

    repo_parser = subparsers.add_parser("repo", help="Manage wallpaper repositories (GDrive, GDrive Public, MEGA, Local)")
    repo_parser.add_argument("action", nargs="?", default="list", choices=["list", "add", "remove", "toggle"])
    repo_parser.add_argument("name", nargs="?", default=None)
    repo_parser.add_argument("repo_type", nargs="?", default=None, choices=["gdrive", "gdrive_public", "mega", "local"])
    repo_parser.add_argument("target", nargs="?", default=None)

    reset_parser = subparsers.add_parser("reset", help="Reset local database and cache")
    reset_parser.add_argument(
        "--force", action="store_true", help="Skip confirmation prompt"
    )

    fav_parser = subparsers.add_parser("favorite", help="Manage favorite wallpapers")
    fav_parser.add_argument("action", nargs="?", default="list", choices=["list", "add", "remove"])
    fav_parser.add_argument("wallpaper_id", nargs="?", default=None)

    tag_parser = subparsers.add_parser("tag", help="Manage wallpaper tags")
    tag_parser.add_argument("action", nargs="?", default="list", choices=["list", "add", "remove"])
    tag_parser.add_argument("tag_name", nargs="?", default=None)
    tag_parser.add_argument("wallpaper_id", nargs="?", default=None)

    cfg_parser = subparsers.add_parser("config", help="View or modify WallSync settings")
    cfg_parser.add_argument("action", nargs="?", default="list", choices=["list", "get", "set"])
    cfg_parser.add_argument("key", nargs="?", default=None)
    cfg_parser.add_argument("value", nargs="?", default=None)

    subparsers.add_parser("install", help="Install WallSync systemd service")
    subparsers.add_parser("uninstall", help="Remove WallSync systemd service")
    subparsers.add_parser("status", help="Show WallSync service status")
    subparsers.add_parser("pause", help="Pause the WallSync timer")
    subparsers.add_parser("resume", help="Resume the WallSync timer")

    interval_parser = subparsers.add_parser("interval", help="Set wallpaper rotation interval")
    interval_parser.add_argument("minutes", type=int, help="Rotation interval in minutes")

    upload_parser = subparsers.add_parser("upload", help="Upload a wallpaper or folder")
    upload_parser.add_argument("path", help="Path to image or directory")

    delete_parser = subparsers.add_parser("delete", help="Delete current wallpaper")
    delete_parser.add_argument("--force", action="store_true", help="Skip confirmation prompt")

    args = parser.parse_args()

    if args.command == "login":
        login()
    elif args.command == "next":
        next_wallpaper(preview=args.preview, dry_run=args.dry_run)
    elif args.command == "prev":
        prev_wallpaper()
    elif args.command == "history":
        history()
    elif args.command == "sync":
        sync()
    elif args.command == "info":
        info()
    elif args.command == "stats":
        stats()
    elif args.command == "clean":
        clean()
    elif args.command == "repo":
        repo_cmd(action=args.action, name=args.name, repo_type=args.repo_type, target=args.target)
    elif args.command == "reset":
        reset(force=args.force)
    elif args.command == "favorite":
        favorite(action=args.action, wallpaper_id=args.wallpaper_id)
    elif args.command == "tag":
        tag(action=args.action, tag_name=args.tag_name, wallpaper_id=args.wallpaper_id)
    elif args.command == "config":
        config_cmd(action=args.action, key=args.key, value=args.value)
    elif args.command == "install":
        install()
    elif args.command == "uninstall":
        uninstall()
    elif args.command == "status":
        status()
    elif args.command == "pause":
        pause()
    elif args.command == "resume":
        resume()
    elif args.command == "interval":
        interval(args.minutes)
    elif args.command == "upload":
        upload(args.path)
    elif args.command == "delete":
        delete(args.force)


if __name__ == "__main__":
    main()
