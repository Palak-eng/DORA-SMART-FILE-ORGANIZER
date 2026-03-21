# Smart File Organizer

A beginner-friendly Python automation project that organizes files into folders based on file type.

## Features
- Detects file types using extensions
- Creates folders automatically
- Moves files into the correct category
- Sends unknown files to `Others`
- Handles duplicate file names safely

## Tech Used
- Python
- pathlib
- shutil

## Categories
- Images
- PDFs
- Videos
- Documents
- Audio
- Others

## How to Run
1. Open terminal in the project folder
2. Run:
   python main.py
3. Enter the folder path you want to organize

## Example
Before:
- photo.jpg
- notes.pdf
- song.mp3

After:
- Images/photo.jpg
- PDFs/notes.pdf
- Audio/song.mp3