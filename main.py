from pathlib import Path
import shutil

folder_input = input("Enter folder path to organize: ")
folder_path = Path(folder_input)

file_categories = {
    "Images": [".jpg", ".jpeg", ".png", ".gif"],
    "PDFs": [".pdf"],
    "Videos": [".mp4", ".mkv", ".avi"],
    "Documents": [".docx", ".doc", ".txt"],
    "Audio": [".mp3", ".wav"]
}

moved_count = 0

for category in file_categories.keys():
    (folder_path / category).mkdir(exist_ok=True)

(folder_path / "Others").mkdir(exist_ok=True)


def get_unique_destination(destination):
    if not destination.exists():
        return destination

    counter = 1
    while True:
        new_name = f"{destination.stem}_{counter}{destination.suffix}"
        new_destination = destination.parent / new_name
        if not new_destination.exists():
            return new_destination
        counter += 1


for item in folder_path.iterdir():
    if item.is_file():
        file_extension = item.suffix.lower()
        moved = False

        for category, extensions in file_categories.items():
            if file_extension in extensions:
                destination = folder_path / category / item.name
                destination = get_unique_destination(destination)
                shutil.move(str(item), str(destination))
                print(f"Moved {item.name} -> {category}")
                moved = True
                moved_count += 1
                break

        if not moved:
            destination = folder_path / "Others" / item.name
            destination = get_unique_destination(destination)
            shutil.move(str(item), str(destination))
            print(f"Moved {item.name} -> Others")
            moved_count += 1

print(f"\nTotal files moved: {moved_count}")