# 🚀 Smart File Organizer

A Python automation tool that organizes files into category-based folders and also fixes misplaced files automatically.

## ✨ Features

- 📂 Organizes files by extension
- 🔄 Detects and fixes wrongly placed files
- 🧠 Smart categorization (Images, Videos, Docs, etc.)
- ⚠️ Handles duplicate file names safely
- 👀 Dry-run mode (preview changes before applying)
- 📊 Summary of operations
- 🛡️ Error handling for safe execution

## 🛠️ Tech Stack

- Python
- pathlib
- shutil

## 📁 Categories

- Images
- PDFs
- Videos
- Documents
- Audio
- Archives
- Code
- Spreadsheets
- Others

## ▶️ How to Run

```bash
python main.py

##📸 Example

 Before:
test_folder/
    photo.jpg
    PDFs/
        image.png
After:
test_folder/
    Images/photo.jpg
    Images/image.png 
 
 👨‍💻 Author

Palak Barsaiyan
