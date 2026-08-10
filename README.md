# 🚀 DORA — Desktop File Organizer

DORA (Digital Organizer & Routing Assistant) is a desktop file organization tool built using Python and CustomTkinter. It helps automate file sorting, correct misplaced files, and keep folders clean through a modern and intuitive GUI.

---

## 📂 Project Structure

```
DORA/
│── gui.py
│── main.py
│── logo.png
│── logo.ico
│── README.md
│── .gitignore
```

---

## ⚙️ How It Works

DORA performs the following steps:

- 🔍 Scans the selected folder
- 🧠 Detects file types using extensions
- 📁 Determines the correct category
- 📦 Creates only required folders
- 🔄 Moves files into appropriate locations
- 🧹 Removes empty folders after organization

✨ Includes **Dry Run mode** to preview changes before applying them.

---

## 📊 Supported Categories

- 🖼️ Images
- 📄 PDFs
- 🎥 Videos
- 📝 Documents
- 🎵 Audio
- 📦 Archives
- 💻 Code
- 📊 Spreadsheets
- 📁 Others

---

## 🛠️ Installation

Clone the repository and install dependencies:

```bash
git clone https://github.com/Palak-eng/DORA-SMART-FILE-ORGANIZER.git
cd DORA-file-organizer
pip install customtkinter pillow
```

---

## ▶️ Run the Application

```bash
python gui.py
```

---

## 🏗️ Build Windows Executable (.exe)

```bash
pyinstaller --noconfirm --clean --onefile --windowed --icon=logo.ico --add-data "logo.png;." --name "DORA" gui.py
```

📦 The executable will be generated inside the `dist/` folder.

---

## 💡 Use Cases

- 📥 Organizing Downloads folder
- 🧾 Cleaning screenshots & documents
- 📂 Structuring messy project directories
- 🔍 Previewing file changes safely (Dry Run)
- 🖥️ Creating a personal desktop utility

---

## 🚀 Future Improvements

- 🔁 Undo last operation
- 👀 Real-time folder monitoring
- 🖱️ Drag-and-drop folder selection
- 📦 Installer setup (Setup.exe / MSI)
- 🌐 Cross-platform support

---

## 👨‍💻 Author

**Palak Barsaiyan**

---

## 📜 License

This project is intended for educational and portfolio use.
