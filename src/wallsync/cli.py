import argparse

from wallsync.commands.delete import run as delete
from wallsync.commands.info import run as info
from wallsync.commands.install import run as install
from wallsync.commands.interval import run as interval
from wallsync.commands.login import run as login
from wallsync.commands.next import run as next_wallpaper
from wallsync.commands.status import run as status
from wallsync.commands.uninstall import run as uninstall
from wallsync.commands.upload import run as upload


def main():
    parser = argparse.ArgumentParser(
        prog="wallsync",
        description="Google Drive wallpaper rotator",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    subparsers.add_parser(
        "login",
        help="Authenticate with Google Drive",
    )

    subparsers.add_parser(
        "next",
        help="Apply the next wallpaper",
    )

    subparsers.add_parser(
        "info",
        help="Show wallpaper information",
    )

    subparsers.add_parser(
        "install",
        help="Install WallSync systemd service",
    )

    subparsers.add_parser(
        "uninstall",
        help="Remove WallSync systemd service",
    )

    subparsers.add_parser(
        "status",
        help="Show WallSync service status",
    )

    interval_parser = subparsers.add_parser(
        "interval",
        help="Set wallpaper rotation interval",
    )

    interval_parser.add_argument(
        "minutes",
        type=int,
        help="Rotation interval in minutes",
    )

    upload_parser = subparsers.add_parser(
        "upload",
        help="Upload a wallpaper or an entire folder",
    )

    upload_parser.add_argument(
        "path",
        help="Path to an image or folder",
    )

    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete the current wallpaper and apply another",
    )

    delete_parser.add_argument(
        "--force",
        action="store_true",
        help="Delete without confirmation",
    )

    args = parser.parse_args()

    if args.command == "login":
        login()

    elif args.command == "next":
        next_wallpaper()

    elif args.command == "info":
        info()

    elif args.command == "install":
        install()

    elif args.command == "uninstall":
        uninstall()

    elif args.command == "status":
        status()

    elif args.command == "interval":
        interval(args.minutes)

    elif args.command == "upload":
        upload(args.path)

    elif args.command == "delete":
        delete(args.force)


if __name__ == "__main__":
    main()
