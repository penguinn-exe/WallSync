from wallsync.config import get_config
from wallsync.stats import get_full_stats

CYAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RESET = "\033[0m"


def run():
    config = get_config()
    stats = get_full_stats(config)

    print(f"{CYAN}WallSync Detailed Usage Statistics{RESET}")
    print("──────────────────────────────────────────────────────")
    print(f"Total Wallpapers Repository : {stats['total_wallpapers']}")
    print(f"Never Shown in Cycle       : {stats['never_shown']}")
    print(f"Last Rotation Sync Time     : {stats['last_sync']}")
    print(f"Local Cache Size            : {stats['cache_size_str']} ({stats['cache_count']} files)")
    print(f"Metadata / Database Size    : {stats['database_size_str']}")
    print(f"Active Timer Interval       : {stats['interval']}")
    print()

    print(f"{YELLOW}Top 3 Most Viewed Wallpapers:{RESET}")
    if stats["most_shown"]:
        for item in stats["most_shown"]:
            print(f"  - {item['filename']}: {item['view_count']} views")
    else:
        print("  (No views logged yet)")

    print()
    print(f"{YELLOW}Bottom 3 Least Viewed Wallpapers:{RESET}")
    if stats["least_shown"]:
        for item in stats["least_shown"]:
            print(f"  - {item['filename']}: {item['view_count']} views")
    else:
        print("  (No wallpapers in database)")
