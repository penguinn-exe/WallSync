import argparse

from wallsync.commands.scan import run as scan


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
        help="Scan a wallpaper collection",
    )
    scan_parser.add_argument(
        "directory",
        help="Path to the wallpaper collection",
    )

    subparsers.add_parser(
        "next",
        help="Download and apply the next wallpaper",
    )

    subparsers.add_parser(
        "status",
        help="Show current status",
    )

    args = parser.parse_args()

    if args.command == "scan":
        scan(args.directory)
    elif args.command == "next":
        print("Selecting next wallpaper...")
    elif args.command == "status":
        print("WallSync v0.1")


if __name__ == "__main__":
    main()
