# DORA — Desktop File Organizer

DORA is a desktop file organization tool built with Python and CustomTkinter. It helps users organize files into category-based folders, correct misplaced files, preview changes through Dry Run mode, and generate exportable operation reports through a modern multi-theme GUI.

## Overview

DORA was designed as a user-friendly desktop application for automating folder cleanup and file organization. It combines file-system automation with a polished graphical interface, allowing users to manage files safely and efficiently without using the command line.

## Features

- Organizes files into category-based folders
- Detects and corrects misplaced files
- Supports Dry Run mode for safe preview before execution
- Removes empty organizer folders after processing
- Handles duplicate file names safely
- Provides a multi-theme GUI:
  - Professional
  - Dark
  - Light
  - Cute
  - Lavender
- Saves user preferences such as selected theme, folder path, and Dry Run state
- Exports operation reports
- Includes custom branding and desktop application icon
- Built as a standalone Windows executable using PyInstaller

## Tech Stack

- Python
- CustomTkinter
- Pillow
- PyInstaller

## Project Structure

```text
DORA/
│── gui.py
│── main.py
│── logo.png
│── logo.ico
│── README.md
│── .gitignore
How It Works

DORA scans the selected folder, identifies files by extension, determines the correct target category, creates only the required folders, moves files into their appropriate locations, and removes empty folders after organization. The interface also provides a Dry Run mode so users can review intended changes before applying them.

Supported Categories
Images
PDFs
Videos
Documents
Audio
Archives
Code
Spreadsheets
Others
Installation

Clone the repository and install the required dependencies:

git clone https://github.com/YOUR_USERNAME/DORA-file-organizer.git
cd DORA-file-organizer
pip install customtkinter pillow
Run the Application
python gui.py
Build the Windows Executable
pyinstaller --noconfirm --clean --onefile --windowed --icon=logo.ico --add-data "logo.png;." --name "DORA" gui.py

After building, the executable will be available inside the dist/ folder.

Use Cases
Organizing downloads folders
Cleaning up screenshots and documents
Reorganizing mixed project folders
Safely previewing file organization before execution
Creating a desktop utility for file management
Future Improvements
Undo last operation
Real-time folder monitoring
Drag-and-drop folder selection
Installer package for easier distribution
Cross-platform packaging
Author

Palak Barsaiyan

License

This project is for educational and portfolio use.