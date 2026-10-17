import os
import shutil
import logging
from pathlib import Path

# Extension -> category folder
EXTENSION_MAP = {
    # Documents
    ".pdf": "Documents", ".doc": "Documents", ".docx": "Documents",
    ".txt": "Documents", ".xls": "Documents", ".xlsx": "Documents",
    ".ppt": "Documents", ".pptx": "Documents", ".csv": "Documents",
    # Images
    ".jpg": "Images", ".jpeg": "Images", ".png": "Images",
    ".gif": "Images", ".bmp": "Images", ".svg": "Images", ".webp": "Images",
    # Videos
    ".mp4": "Videos", ".mkv": "Videos", ".avi": "Videos",
    ".mov": "Videos", ".wmv": "Videos",
    # Archives
    ".zip": "Archives", ".rar": "Archives", ".7z": "Archives",
    ".tar": "Archives", ".gz": "Archives",
    # Code
    ".py": "Code", ".js": "Code", ".html": "Code", ".css": "Code",
    ".java": "Code", ".c": "Code", ".cpp": "Code", ".json": "Code",
}

DEFAULT_CATEGORY = "Others"
LOG_FILE = "organizer.log"
SKIP_FILES = {"organizer.py", LOG_FILE}

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


def get_category(filename):
    """Return the category folder name for a file based on its extension."""
    return EXTENSION_MAP.get(Path(filename).suffix.lower(), DEFAULT_CATEGORY)


def unique_destination(dest):
    """If dest already exists, return 'name (1).ext', 'name (2).ext', ..."""
    if not dest.exists():
        return dest
    counter = 1
    while True:
        candidate = dest.with_name(f"{dest.stem} ({counter}){dest.suffix}")
        if not candidate.exists():
            return candidate
        counter += 1


def create_demo_folder():
    """Create a small messy folder so the script can be tested safely."""
    demo = Path("demo_messy_folder")
    demo.mkdir(exist_ok=True)
    sample_files = [
        "report.pdf", "notes.txt", "photo1.jpg", "logo.png", "movie.mp4",
        "backup.zip", "script.py", "index.html", "data.csv", "unknown.xyz",
    ]
    for name in sample_files:
        (demo / name).write_text("demo file")

    # Pre-existing file to demonstrate naming collision handling
    (demo / "Documents").mkdir(exist_ok=True)
    (demo / "Documents" / "report.pdf").write_text("old report")

    print(f"Created demo folder: {demo.resolve()}")
    return demo


def organize_folder(folder, dry_run=False):
    """Move every file in `folder` into a category subfolder."""
    summary = {"moved": 0, "skipped": 0, "errors": 0}
    per_category = {}

    # Read all entries first, then move (do not modify while scanning)
    with os.scandir(folder) as entries:
        files = [e for e in entries if e.is_file()]

    for entry in files:
        name = entry.name

        if name in SKIP_FILES or name.startswith("."):
            summary["skipped"] += 1
            continue

        category = get_category(name)
        dest_dir = folder / category

        if dry_run:
            print(f"[DRY RUN] {name}  ->  {category}/")
            summary["moved"] += 1
            per_category[category] = per_category.get(category, 0) + 1
            continue

        try:
            dest_dir.mkdir(exist_ok=True)
            dest = unique_destination(dest_dir / name)
            shutil.move(entry.path, str(dest))
            if dest.name != name:
                print(f"Renamed (name collision): {name}  ->  {category}/{dest.name}")
                logging.warning("Name collision: %s saved as %s", name, dest.name)
            else:
                print(f"Moved: {name}  ->  {category}/")
            logging.info("Moved %s -> %s", entry.path, dest)
            summary["moved"] += 1
            per_category[category] = per_category.get(category, 0) + 1
        except PermissionError:
            print(f"Permission denied: {name}")
            logging.error("Permission denied: %s", entry.path)
            summary["errors"] += 1
        except FileExistsError:
            print(f"File already exists: {name}")
            logging.error("File exists: %s", entry.path)
            summary["errors"] += 1
        except (OSError, shutil.Error) as e:
            print(f"Could not move {name}: {e}")
            logging.error("Could not move %s: %s", entry.path, e)
            summary["errors"] += 1

    return summary, per_category


def print_summary(folder, summary, per_category, dry_run):
    line = "=" * 50
    print("\n" + line)
    print("FILE ORGANIZER - EXECUTION SUMMARY".center(50))
    print(line)
    print(f"Folder          : {folder}")
    print(f"Mode            : {'DRY RUN (nothing moved)' if dry_run else 'LIVE'}")
    print(f"Files relocated : {summary['moved']}")
    print(f"Files skipped   : {summary['skipped']}")
    print(f"Errors          : {summary['errors']}")
    if per_category:
        print("-" * 50)
        for category, count in sorted(per_category.items()):
            print(f"  {category:<12}: {count}")
    print(line)
    print(f"Log saved to {LOG_FILE}")


def main():
    print("=== AUTOMATED FILE ORGANIZER ===")
    print("Enter the path of the folder to organize.")
    print("Press Enter without typing anything to create and use a demo folder.\n")

    user_input = input("Folder path: ").strip().strip('"')

    if user_input == "":
        folder = create_demo_folder()
    else:
        folder = Path(user_input)
        if not folder.is_dir():
            print("That folder does not exist. Please check the path.")
            return

    answer = input("Run a dry run first (no files moved)? (y/n): ").strip().lower()
    dry_run = answer == "y"

    if not dry_run:
        confirm = input(f"Organize all files in '{folder}'? (y/n): ").strip().lower()
        if confirm != "y":
            print("Cancelled. No files were moved.")
            return

    logging.info("Started organizing %s (dry_run=%s)", folder, dry_run)
    summary, per_category = organize_folder(folder, dry_run)
    print_summary(folder, summary, per_category, dry_run)
    logging.info("Finished: %s", summary)


if __name__ == "__main__":
    main()