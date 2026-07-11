import argparse

from wallsync.commands.next import run as next_wallpaper
from wallsync.commands.scan import run as scan
from wallsync.commands.stats import run as stats


def main():
    parser = argparse.ArgumentParser(
        prog="wallsync",
        description="Cloud-backed wallpaper synchronization tool",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    scan_parser = subparsers.add_parser(
        "scan",
        help="Scan and index a wallpaper collection",
    )
    scan_parser.add_argument(
        "directory",
        help="Path to the wallpaper collection",
    )

    subparsers.add_parser(
        "next",
        help="Apply the next wallpaper",
    )

    subparsers.add_parser(
        "stats",
        help="Show database statistics",
    )

    args = parser.parse_args()

    if args.command == "scan":
        scan(args.directory)

    elif args.command == "next":
        next_wallpaper()

    elif args.command == "stats":
        stats()


if __name__ == "__main__":
    main()
