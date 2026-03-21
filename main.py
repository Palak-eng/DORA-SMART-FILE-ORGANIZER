from pathlib import Path
import shutil

FILE_CATEGORIES = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".webp"],
    "PDFs": [".pdf"],
    "Videos": [".mp4", ".mkv", ".avi", ".mov"],
    "Documents": [".docx", ".doc", ".txt", ".pptx"],
    "Audio": [".mp3", ".wav"],
    "Archives": [".zip", ".rar"],
    "Code": [".py", ".java", ".cpp", ".html", ".css", ".js"],
    "Spreadsheets": [".csv", ".xlsx"]
}

CATEGORY_NAMES = list(FILE_CATEGORIES.keys()) + ["Others"]


def get_file_category(file_name: str) -> str:
    extension = Path(file_name).suffix.lower()
    for category, extensions in FILE_CATEGORIES.items():
        if extension in extensions:
            return category
    return "Others"


def get_unique_destination(destination: Path) -> Path:
    if not destination.exists():
        return destination

    counter = 1
    while True:
        new_destination = destination.parent / f"{destination.stem}_{counter}{destination.suffix}"
        if not new_destination.exists():
            return new_destination
        counter += 1


def collect_files(folder_path: Path):
    files = []

    # Files in main folder
    for item in folder_path.iterdir():
        if item.is_file():
            files.append(item)

    # Files inside already existing category folders only
    for category in CATEGORY_NAMES:
        category_folder = folder_path / category
        if category_folder.exists() and category_folder.is_dir():
            for item in category_folder.iterdir():
                if item.is_file():
                    files.append(item)

    return files


def remove_empty_category_folders(folder_path: Path) -> None:
    for category in CATEGORY_NAMES:
        category_folder = folder_path / category
        if category_folder.exists() and category_folder.is_dir():
            if not any(category_folder.iterdir()):
                category_folder.rmdir()
                print(f"Removed empty folder: {category}")


def organize_files(folder_path: Path, dry_run: bool = False):
    files = collect_files(folder_path)

    moved_count = 0
    correct_count = 0
    total_scanned = 0

    summary = {category: 0 for category in CATEGORY_NAMES}

    # Find only required categories
    required_categories = set()

    for file_path in files:
        if file_path.name == "organizer_log.txt":
            continue
        category = get_file_category(file_path.name)
        required_categories.add(category)

    # Create only required folders
    for category in required_categories:
        (folder_path / category).mkdir(exist_ok=True)

    # Process files
    for file_path in files:
        if file_path.name == "organizer_log.txt":
            continue

        total_scanned += 1

        correct_category = get_file_category(file_path.name)
        correct_folder = folder_path / correct_category

        # Already in correct folder
        if file_path.parent.resolve() == correct_folder.resolve():
            print(f"Already correct: {file_path.name} -> {correct_category}")
            correct_count += 1
            continue

        destination = correct_folder / file_path.name
        destination = get_unique_destination(destination)

        if dry_run:
            print(f"[DRY RUN] {file_path} -> {destination}")
            moved_count += 1
            summary[correct_category] += 1
        else:
            shutil.move(str(file_path), str(destination))
            print(f"Moved: {file_path.name} -> {correct_category}")
            moved_count += 1
            summary[correct_category] += 1

    # Remove empty folders only in actual run
    if not dry_run:
        remove_empty_category_folders(folder_path)

    print("\n--- Summary ---")
    print(f"Total scanned: {total_scanned}")
    print(f"Moved files: {moved_count}")
    print(f"Already correct: {correct_count}")

    return total_scanned, moved_count, correct_count, summary


def main() -> None:
    folder_input = input("Enter folder path to organize: ").strip()
    folder_path = Path(folder_input)

    if not folder_path.exists():
        print("Error: folder does not exist.")
        return

    if not folder_path.is_dir():
        print("Error: entered path is not a folder.")
        return

    dry_run_input = input("Run in dry mode? (yes/no): ").strip().lower()
    dry_run = dry_run_input == "yes"

    total_scanned, moved_count, correct_count, summary = organize_files(folder_path, dry_run)

    print("\n--- Category Summary ---")
    for category, count in summary.items():
        print(f"{category}: {count}")


if __name__ == "__main__":
    main()