import customtkinter as ctk
from tkinter import filedialog, messagebox
from pathlib import Path
from main import organize_files
import json
import os
import threading
import queue
import io
import contextlib
from datetime import datetime

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

SETTINGS_FILE = "settings.json"

THEMES = {
    "Cute": {
        "app_bg": "#fff7fb",
        "sidebar_bg": "#ffeef5",
        "sidebar_text": "#7a4760",
        "card_bg": "#ffffff",
        "header_bg": "#ffd9e8",
        "header_text": "#8f3f66",
        "sub_text": "#8c5a72",
        "button_primary": "#f58db2",
        "button_primary_hover": "#ea6e9d",
        "button_secondary": "#ffd6e7",
        "button_secondary_hover": "#ffc1db",
        "status_fg": "#ffe4ef",
        "status_text": "#a03b68",
        "output_bg": "#fffdfd",
        "output_text": "#5f4b59",
        "entry_bg": "#ffffff",
        "border": "#f6bfd4",
        "stat_bg": "#fff0f6",
        "stat_value": "#d94c8a",
    },
    "Lavender": {
        "app_bg": "#f7f4ff",
        "sidebar_bg": "#f1ebff",
        "sidebar_text": "#5d4c89",
        "card_bg": "#ffffff",
        "header_bg": "#e6dcff",
        "header_text": "#5b2ca3",
        "sub_text": "#7a67b5",
        "button_primary": "#9d7cf4",
        "button_primary_hover": "#845ff0",
        "button_secondary": "#e2d7ff",
        "button_secondary_hover": "#d4c4ff",
        "status_fg": "#efe8ff",
        "status_text": "#6f42c1",
        "output_bg": "#fcfbff",
        "output_text": "#46386d",
        "entry_bg": "#ffffff",
        "border": "#d9c7ff",
        "stat_bg": "#f5f1ff",
        "stat_value": "#7c4dff",
    },
    "Professional": {
        "app_bg": "#f4f7fb",
        "sidebar_bg": "#ffffff",
        "sidebar_text": "#334155",
        "card_bg": "#ffffff",
        "header_bg": "#111827",
        "header_text": "#ffffff",
        "sub_text": "#cbd5e1",
        "button_primary": "#2563eb",
        "button_primary_hover": "#1d4ed8",
        "button_secondary": "#e2e8f0",
        "button_secondary_hover": "#cbd5e1",
        "status_fg": "#eff6ff",
        "status_text": "#1d4ed8",
        "output_bg": "#f8fafc",
        "output_text": "#1f2937",
        "entry_bg": "#ffffff",
        "border": "#e2e8f0",
        "stat_bg": "#f8fafc",
        "stat_value": "#2563eb",
    },
    "Dark": {
        "app_bg": "#0b1220",
        "sidebar_bg": "#111827",
        "sidebar_text": "#e5e7eb",
        "card_bg": "#182233",
        "header_bg": "#020617",
        "header_text": "#f8fafc",
        "sub_text": "#94a3b8",
        "button_primary": "#3b82f6",
        "button_primary_hover": "#2563eb",
        "button_secondary": "#243245",
        "button_secondary_hover": "#334155",
        "status_fg": "#122033",
        "status_text": "#7dd3fc",
        "output_bg": "#0f172a",
        "output_text": "#e2e8f0",
        "entry_bg": "#0f172a",
        "border": "#334155",
        "stat_bg": "#111827",
        "stat_value": "#60a5fa",
    },
    "Light": {
        "app_bg": "#f8fbff",
        "sidebar_bg": "#f1f7fd",
        "sidebar_text": "#355070",
        "card_bg": "#ffffff",
        "header_bg": "#e7f2ff",
        "header_text": "#23405f",
        "sub_text": "#4f7093",
        "button_primary": "#4dabf7",
        "button_primary_hover": "#339af0",
        "button_secondary": "#dbeafe",
        "button_secondary_hover": "#bfdbfe",
        "status_fg": "#ebf8ff",
        "status_text": "#0c8599",
        "output_bg": "#ffffff",
        "output_text": "#243b53",
        "entry_bg": "#ffffff",
        "border": "#d0e2f2",
        "stat_bg": "#f7fbff",
        "stat_value": "#339af0",
    }
}

THEME_STYLES = {
    "Cute": {
        "brand": "🎀 Smart File Organizer",
        "page_title": "Cute Dashboard",
        "subtitle": "Bows, blossoms, and beautifully sorted folders ✨",
        "hero": "🎀  🌸  🧁  ✨  🌷",
        "nav": ["🌸 Folder", "🎀 Organize", "🫧 Dry Run", "🧸 Output"],
        "tip_title": "Pretty Tip",
        "tip_text": "Use Dry Run first, then run the real organization once everything looks perfect.",
        "status_idle": "Waiting 💖",
        "welcome": "🎀 Welcome!\n\nChoose a folder and organize your files beautifully 🌸✨\n"
    },
    "Lavender": {
        "brand": "💜 Smart File Organizer",
        "page_title": "Lavender Workspace",
        "subtitle": "Lavender calm with a dreamy, elegant workflow 🌿",
        "hero": "💜  🌿  🪻  ✨  🌙",
        "nav": ["🪻 Folder", "🌿 Organize", "💜 Dry Run", "🌙 Output"],
        "tip_title": "Lavender Note",
        "tip_text": "Preview first for a calm workflow, then run the organizer when everything feels right.",
        "status_idle": "Relaxed 💜",
        "welcome": "🪻 Welcome.\n\nA calm workspace for elegant file organization 🌿💜\n"
    },
    "Professional": {
        "brand": "Smart File Organizer",
        "page_title": "Dashboard",
        "subtitle": "Professional organization workflow with clear operational control.",
        "hero": "▣   ◼   ▣   ◼   ▣",
        "nav": ["📁 Folder", "⚙️ Organize", "🧪 Dry Run", "📋 Output"],
        "tip_title": "Best Practice",
        "tip_text": "Use Dry Run for validation before applying changes to important folders.",
        "status_idle": "Idle",
        "welcome": "System ready.\n\nSelect a target folder and execute the organization workflow.\n"
    },
    "Dark": {
        "brand": "◈ Smart File Organizer",
        "page_title": "Control Center",
        "subtitle": "A sleek dark control panel for precise file operations.",
        "hero": "◢  ◆  ◣  ✦  ◆",
        "nav": ["◈ Folder", "◆ Organize", "✦ Dry Run", "⬢ Output"],
        "tip_title": "Execution Tip",
        "tip_text": "Run Dry Run for a safe preview before committing directory changes.",
        "status_idle": "Standby",
        "welcome": "Dark interface online.\n\nPrecision mode enabled.\n"
    },
    "Light": {
        "brand": "☁ Smart File Organizer",
        "page_title": "Workspace",
        "subtitle": "A fresh, airy workspace for clean file management.",
        "hero": "☁  ✨  ◦  ✦  ☼",
        "nav": ["☁ Folder", "✨ Organize", "◦ Dry Run", "✦ Output"],
        "tip_title": "Clean Tip",
        "tip_text": "Use Dry Run first for a clean preview before making actual folder changes.",
        "status_idle": "Ready",
        "welcome": "☁ Welcome.\n\nA clean workspace for smooth file organization.\n"
    }
}


class SmartFileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Smart File Organizer")
        self.geometry("1320x840")
        self.minsize(1200, 760)

        self.folder_path_var = ctk.StringVar()
        self.dry_run_var = ctk.BooleanVar(value=True)
        self.theme_var = ctk.StringVar(value="Professional")

        self.run_queue = queue.Queue()
        self.current_report = ""
        self.is_running = False

        self.load_settings()
        self.build_ui()
        self.apply_theme()
        self.after(150, self.process_queue)

    # ---------------- SETTINGS ----------------
    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as file:
                    settings = json.load(file)
                self.theme_var.set(settings.get("theme", "Professional"))
                self.folder_path_var.set(settings.get("last_folder", ""))
                self.dry_run_var.set(settings.get("dry_run", True))
            except Exception:
                self.theme_var.set("Professional")
                self.folder_path_var.set("")
                self.dry_run_var.set(True)

    def save_settings(self):
        settings = {
            "theme": self.theme_var.get(),
            "last_folder": self.folder_path_var.get(),
            "dry_run": self.dry_run_var.get()
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as file:
                json.dump(settings, file, indent=4)
        except Exception as e:
            print("Could not save settings:", e)

    # ---------------- UI ----------------
    def build_ui(self):
        self.build_sidebar()
        self.build_main_area()

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=280, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Smart File Organizer",
            font=("Arial", 28, "bold"),
            justify="left"
        )
        self.logo_label.pack(anchor="w", padx=22, pady=(26, 8))

        self.logo_subtitle = ctk.CTkLabel(
            self.sidebar,
            text="Organize and correct file placement",
            font=("Arial", 12),
            justify="left",
            wraplength=220
        )
        self.logo_subtitle.pack(anchor="w", padx=22, pady=(0, 18))

        self.mode_label = ctk.CTkLabel(
            self.sidebar,
            text="Theme Mode",
            font=("Arial", 14, "bold")
        )
        self.mode_label.pack(anchor="w", padx=22, pady=(8, 8))

        self.mode_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=list(THEMES.keys()),
            variable=self.theme_var,
            command=self.change_theme,
            width=220,
            height=40,
            corner_radius=12
        )
        self.mode_menu.pack(anchor="w", padx=22, pady=(0, 16))

        self.decoration_card = ctk.CTkFrame(self.sidebar, corner_radius=18, height=76)
        self.decoration_card.pack(fill="x", padx=16, pady=(0, 14))
        self.decoration_card.pack_propagate(False)

        self.decoration_label = ctk.CTkLabel(
            self.decoration_card,
            text="✦ ✦ ✦",
            font=("Arial", 24, "bold")
        )
        self.decoration_label.pack(expand=True)

        self.nav_card = ctk.CTkFrame(self.sidebar, corner_radius=18)
        self.nav_card.pack(fill="x", padx=16, pady=(0, 14))

        self.nav_title = ctk.CTkLabel(
            self.nav_card,
            text="Navigation",
            font=("Arial", 14, "bold")
        )
        self.nav_title.pack(anchor="w", padx=16, pady=(14, 10))

        self.nav_labels = []
        for _ in range(4):
            label = ctk.CTkLabel(self.nav_card, text="", font=("Arial", 13))
            label.pack(anchor="w", padx=16, pady=6)
            self.nav_labels.append(label)

        self.tip_card = ctk.CTkFrame(self.sidebar, corner_radius=18)
        self.tip_card.pack(fill="x", padx=16, pady=(0, 14))

        self.tip_title = ctk.CTkLabel(
            self.tip_card,
            text="Tip",
            font=("Arial", 14, "bold")
        )
        self.tip_title.pack(anchor="w", padx=16, pady=(14, 8))

        self.tip_text = ctk.CTkLabel(
            self.tip_card,
            text="Use Dry Run first.",
            font=("Arial", 12),
            justify="left",
            wraplength=210
        )
        self.tip_text.pack(anchor="w", padx=16, pady=(0, 14))

        self.sidebar_actions = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        self.sidebar_actions.pack(fill="x", padx=16, pady=(0, 12))

        self.open_folder_button = ctk.CTkButton(
            self.sidebar_actions,
            text="Open Folder",
            height=40,
            corner_radius=12,
            command=self.open_folder
        )
        self.open_folder_button.pack(fill="x", pady=(0, 8))

        self.export_button = ctk.CTkButton(
            self.sidebar_actions,
            text="Export Report",
            height=40,
            corner_radius=12,
            command=self.export_report
        )
        self.export_button.pack(fill="x")

        self.footer_label = ctk.CTkLabel(
            self.sidebar,
            text="Python + CustomTkinter",
            font=("Arial", 11)
        )
        self.footer_label.pack(side="bottom", pady=18)

    def build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color="transparent")
        self.main_area.pack(side="left", fill="both", expand=True, padx=22, pady=22)

        self.header_card = ctk.CTkFrame(self.main_area, corner_radius=28, height=150)
        self.header_card.pack(fill="x", pady=(0, 14))
        self.header_card.pack_propagate(False)

        self.header_title = ctk.CTkLabel(
            self.header_card,
            text="Dashboard",
            font=("Arial", 30, "bold")
        )
        self.header_title.pack(anchor="w", padx=24, pady=(20, 4))

        self.header_subtitle = ctk.CTkLabel(
            self.header_card,
            text="Choose a folder and organize files efficiently.",
            font=("Arial", 13)
        )
        self.header_subtitle.pack(anchor="w", padx=24)

        self.hero_strip = ctk.CTkLabel(
            self.header_card,
            text="✦ ✦ ✦",
            font=("Arial", 24, "bold")
        )
        self.hero_strip.pack(anchor="w", padx=24, pady=(12, 0))

        self.folder_card = ctk.CTkFrame(self.main_area, corner_radius=22)
        self.folder_card.pack(fill="x", pady=(0, 12))

        self.folder_title = ctk.CTkLabel(
            self.folder_card,
            text="Folder Selection",
            font=("Arial", 17, "bold")
        )
        self.folder_title.pack(anchor="w", padx=20, pady=(16, 10))

        self.folder_row = ctk.CTkFrame(self.folder_card, fg_color="transparent")
        self.folder_row.pack(fill="x", padx=20, pady=(0, 16))

        self.folder_entry = ctk.CTkEntry(
            self.folder_row,
            textvariable=self.folder_path_var,
            height=46,
            corner_radius=14,
            font=("Arial", 13),
            placeholder_text="Select a folder to organize..."
        )
        self.folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 12))

        self.browse_button = ctk.CTkButton(
            self.folder_row,
            text="Browse",
            width=128,
            height=46,
            corner_radius=14,
            font=("Arial", 13, "bold"),
            command=self.browse_folder
        )
        self.browse_button.pack(side="left")

        self.controls_row = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.controls_row.pack(fill="x", pady=(0, 12))

        self.options_card = ctk.CTkFrame(self.controls_row, corner_radius=22)
        self.options_card.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.options_title = ctk.CTkLabel(
            self.options_card,
            text="Options",
            font=("Arial", 17, "bold")
        )
        self.options_title.pack(anchor="w", padx=20, pady=(16, 10))

        self.dry_run_switch = ctk.CTkSwitch(
            self.options_card,
            text="Enable Dry Run",
            variable=self.dry_run_var,
            font=("Arial", 14),
            command=self.save_settings
        )
        self.dry_run_switch.pack(anchor="w", padx=20, pady=(0, 6))

        self.option_hint = ctk.CTkLabel(
            self.options_card,
            text="Preview file movement without changing the folder.",
            font=("Arial", 12)
        )
        self.option_hint.pack(anchor="w", padx=20, pady=(0, 16))

        self.actions_card = ctk.CTkFrame(self.controls_row, corner_radius=22)
        self.actions_card.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.actions_title = ctk.CTkLabel(
            self.actions_card,
            text="Actions",
            font=("Arial", 17, "bold")
        )
        self.actions_title.pack(anchor="w", padx=20, pady=(16, 10))

        self.actions_buttons = ctk.CTkFrame(self.actions_card, fg_color="transparent")
        self.actions_buttons.pack(fill="x", padx=20, pady=(0, 16))

        self.organize_button = ctk.CTkButton(
            self.actions_buttons,
            text="Run Organizer",
            height=46,
            corner_radius=14,
            font=("Arial", 13, "bold"),
            command=self.organize_action
        )
        self.organize_button.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.clear_button = ctk.CTkButton(
            self.actions_buttons,
            text="Clear",
            height=46,
            corner_radius=14,
            font=("Arial", 13, "bold"),
            command=self.clear_output
        )
        self.clear_button.pack(side="left", fill="x", expand=True, padx=(8, 0))

        self.stats_row = ctk.CTkFrame(self.main_area, fg_color="transparent")
        self.stats_row.pack(fill="x", pady=(0, 12))

        self.scanned_card = self.create_stat_card(self.stats_row, "Total Scanned", "0")
        self.scanned_card.pack(side="left", fill="both", expand=True, padx=(0, 6))

        self.moved_card = self.create_stat_card(self.stats_row, "Moved Files", "0")
        self.moved_card.pack(side="left", fill="both", expand=True, padx=6)

        self.correct_card = self.create_stat_card(self.stats_row, "Already Correct", "0")
        self.correct_card.pack(side="left", fill="both", expand=True, padx=(6, 0))

        self.output_card = ctk.CTkFrame(self.main_area, corner_radius=22)
        self.output_card.pack(fill="both", expand=True)

        self.output_header = ctk.CTkFrame(self.output_card, fg_color="transparent")
        self.output_header.pack(fill="x", padx=20, pady=(16, 10))

        self.output_title = ctk.CTkLabel(
            self.output_header,
            text="Live Output",
            font=("Arial", 17, "bold")
        )
        self.output_title.pack(side="left")

        self.status_badge = ctk.CTkLabel(
            self.output_header,
            text="Waiting",
            font=("Arial", 12, "bold"),
            corner_radius=16,
            padx=14,
            pady=7
        )
        self.status_badge.pack(side="right")

        self.output_box = ctk.CTkTextbox(
            self.output_card,
            corner_radius=16,
            font=("Consolas", 12),
            border_width=1
        )
        self.output_box.pack(fill="both", expand=True, padx=20, pady=(0, 20))
        self.output_box.configure(state="disabled")

    def create_stat_card(self, parent, title, value):
        card = ctk.CTkFrame(parent, corner_radius=20, height=106)
        card.pack_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=("Arial", 13, "bold")
        )
        title_label.pack(anchor="w", padx=18, pady=(16, 6))

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=("Arial", 30, "bold")
        )
        value_label.pack(anchor="w", padx=18)

        card.title_label = title_label
        card.value_label = value_label
        return card

    # ---------------- THEME ----------------
    def change_theme(self, _=None):
        self.apply_theme()
        self.save_settings()

    def apply_theme(self):
        theme_name = self.theme_var.get()
        theme = THEMES[theme_name]
        style = THEME_STYLES[theme_name]

        self.configure(fg_color=theme["app_bg"])

        self.sidebar.configure(fg_color=theme["sidebar_bg"])
        self.logo_label.configure(text=style["brand"], text_color=theme["sidebar_text"])
        self.logo_subtitle.configure(text=style["subtitle"], text_color=theme["sidebar_text"])
        self.mode_label.configure(text_color=theme["sidebar_text"])

        self.mode_menu.configure(
            fg_color=theme["card_bg"],
            button_color=theme["button_primary"],
            button_hover_color=theme["button_primary_hover"],
            text_color=theme["sidebar_text"]
        )

        self.decoration_card.configure(
            fg_color=theme["card_bg"],
            border_width=1,
            border_color=theme["border"]
        )
        self.decoration_label.configure(text=style["hero"], text_color=theme["sidebar_text"])

        self.nav_card.configure(
            fg_color=theme["card_bg"],
            border_width=1,
            border_color=theme["border"]
        )
        self.nav_title.configure(text_color=theme["sidebar_text"])
        for label, text in zip(self.nav_labels, style["nav"]):
            label.configure(text=text, text_color=theme["sidebar_text"])

        self.tip_card.configure(
            fg_color=theme["card_bg"],
            border_width=1,
            border_color=theme["border"]
        )
        self.tip_title.configure(text=style["tip_title"], text_color=theme["sidebar_text"])
        self.tip_text.configure(text=style["tip_text"], text_color=theme["sidebar_text"])

        self.open_folder_button.configure(
            fg_color=theme["button_secondary"],
            hover_color=theme["button_secondary_hover"],
            text_color=theme["sidebar_text"]
        )
        self.export_button.configure(
            fg_color=theme["button_primary"],
            hover_color=theme["button_primary_hover"],
            text_color="#ffffff"
        )
        self.footer_label.configure(text_color=theme["sidebar_text"])

        self.header_card.configure(
            fg_color=theme["header_bg"],
            border_width=1,
            border_color=theme["border"]
        )
        self.header_title.configure(text=style["page_title"], text_color=theme["header_text"])
        self.header_subtitle.configure(text=style["subtitle"], text_color=theme["sub_text"])
        self.hero_strip.configure(text=style["hero"], text_color=theme["header_text"])

        for card in [self.folder_card, self.options_card, self.actions_card, self.output_card]:
            card.configure(
                fg_color=theme["card_bg"],
                border_width=1,
                border_color=theme["border"]
            )

        self.folder_title.configure(text_color=theme["sidebar_text"])
        self.folder_entry.configure(
            fg_color=theme["entry_bg"],
            border_color=theme["border"],
            text_color=theme["output_text"]
        )
        self.browse_button.configure(
            fg_color=theme["button_primary"],
            hover_color=theme["button_primary_hover"],
            text_color="#ffffff"
        )

        self.options_title.configure(text_color=theme["sidebar_text"])
        self.dry_run_switch.configure(
            progress_color=theme["button_primary"],
            button_color="#ffffff",
            button_hover_color=theme["button_secondary"],
            text_color=theme["sidebar_text"]
        )
        self.option_hint.configure(text_color=theme["sidebar_text"])

        self.actions_title.configure(text_color=theme["sidebar_text"])
        self.organize_button.configure(
            fg_color=theme["button_primary"],
            hover_color=theme["button_primary_hover"],
            text_color="#ffffff"
        )
        self.clear_button.configure(
            fg_color=theme["button_secondary"],
            hover_color=theme["button_secondary_hover"],
            text_color=theme["sidebar_text"]
        )

        for card in [self.scanned_card, self.moved_card, self.correct_card]:
            card.configure(
                fg_color=theme["stat_bg"],
                border_width=1,
                border_color=theme["border"]
            )
            card.title_label.configure(text_color=theme["sidebar_text"])
            card.value_label.configure(text_color=theme["stat_value"])

        self.output_title.configure(text_color=theme["sidebar_text"])
        self.status_badge.configure(
            text=style["status_idle"],
            fg_color=theme["status_fg"],
            text_color=theme["status_text"]
        )
        self.output_box.configure(
            fg_color=theme["output_bg"],
            text_color=theme["output_text"],
            border_color=theme["border"]
        )

        if not self.current_report:
            self.set_output(style["welcome"])

    # ---------------- HELPERS ----------------
    def set_output(self, text: str):
        self.output_box.configure(state="normal")
        self.output_box.delete("0.0", "end")
        self.output_box.insert("0.0", text)
        self.output_box.configure(state="disabled")

    def append_output(self, text: str):
        self.output_box.configure(state="normal")
        self.output_box.insert("end", text)
        self.output_box.see("end")
        self.output_box.configure(state="disabled")

    def set_running_state(self, running: bool):
        self.is_running = running
        state = "disabled" if running else "normal"

        self.organize_button.configure(state=state)
        self.browse_button.configure(state=state)
        self.clear_button.configure(state=state)
        self.open_folder_button.configure(state=state)
        self.export_button.configure(state=state)
        self.mode_menu.configure(state=state)

    def process_queue(self):
        try:
            while True:
                item = self.run_queue.get_nowait()
                kind = item["type"]

                if kind == "log":
                    self.append_output(item["text"])
                elif kind == "done":
                    total_scanned = item["total_scanned"]
                    moved_count = item["moved_count"]
                    correct_count = item["correct_count"]
                    summary = item["summary"]
                    report_text = item["report"]

                    self.scanned_card.value_label.configure(text=str(total_scanned))
                    self.moved_card.value_label.configure(text=str(moved_count))
                    self.correct_card.value_label.configure(text=str(correct_count))
                    self.current_report = report_text
                    self.status_badge.configure(text="Completed")
                    self.set_running_state(False)

                elif kind == "error":
                    self.status_badge.configure(text="Error")
                    self.set_running_state(False)
                    messagebox.showerror("Error", item["message"])
        except queue.Empty:
            pass

        self.after(150, self.process_queue)

    # ---------------- ACTIONS ----------------
    def browse_folder(self):
        folder_selected = filedialog.askdirectory()
        if folder_selected:
            self.folder_path_var.set(folder_selected)
            self.status_badge.configure(text="Folder Selected")
            self.save_settings()

    def open_folder(self):
        folder = self.folder_path_var.get().strip()
        if not folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        path = Path(folder)
        if not path.exists() or not path.is_dir():
            messagebox.showerror("Error", "Selected folder is invalid.")
            return

        try:
            os.startfile(path)
        except Exception as e:
            messagebox.showerror("Error", f"Could not open folder:\n{e}")

    def export_report(self):
        if not self.current_report.strip():
            messagebox.showerror("Error", "No report available to export yet.")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Text File", "*.txt")],
            initialfile=f"organizer_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        )
        if not file_path:
            return

        try:
            with open(file_path, "w", encoding="utf-8") as file:
                file.write(self.current_report)
            messagebox.showinfo("Success", "Report exported successfully.")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export report:\n{e}")

    def organize_action(self):
        if self.is_running:
            return

        selected_folder = self.folder_path_var.get().strip()

        if not selected_folder:
            messagebox.showerror("Error", "Please select a folder first.")
            return

        folder_path = Path(selected_folder)
        if not folder_path.exists():
            messagebox.showerror("Error", "Selected folder does not exist.")
            return

        if not folder_path.is_dir():
            messagebox.showerror("Error", "Selected path is not a folder.")
            return

        dry_run = self.dry_run_var.get()
        self.save_settings()

        self.current_report = ""
        self.scanned_card.value_label.configure(text="0")
        self.moved_card.value_label.configure(text="0")
        self.correct_card.value_label.configure(text="0")

        self.set_output("")
        self.append_output("Starting organizer...\n\n")
        self.status_badge.configure(text="Running")
        self.set_running_state(True)

        worker = threading.Thread(
            target=self.run_organizer_worker,
            args=(folder_path, dry_run),
            daemon=True
        )
        worker.start()

    def run_organizer_worker(self, folder_path: Path, dry_run: bool):
        try:
            buffer = io.StringIO()
            with contextlib.redirect_stdout(buffer):
                total_scanned, moved_count, correct_count, summary = organize_files(folder_path, dry_run=dry_run)

            captured_logs = buffer.getvalue()

            report_lines = [
                "SMART FILE ORGANIZER REPORT",
                "=" * 64,
                "",
                f"Folder Path    : {folder_path}",
                f"Theme Mode     : {self.theme_var.get()}",
                f"Dry Run Mode   : {'Enabled' if dry_run else 'Disabled'}",
                f"Generated At   : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                "",
                "LIVE OPERATION LOG",
                "-" * 64,
                captured_logs.strip(),
                "",
                "SUMMARY",
                "-" * 64,
                f"Total Files Scanned : {total_scanned}",
                f"Moved Files         : {moved_count}",
                f"Already Correct     : {correct_count}",
                "",
                "CATEGORY BREAKDOWN",
                "-" * 64,
            ]

            for category, count in summary.items():
                report_lines.append(f"{category:<18} : {count}")

            report_lines.append("")
            report_lines.append("PROCESS COMPLETED SUCCESSFULLY.")
            report_text = "\n".join(report_lines)

            self.run_queue.put({"type": "log", "text": report_text})
            self.run_queue.put({
                "type": "done",
                "total_scanned": total_scanned,
                "moved_count": moved_count,
                "correct_count": correct_count,
                "summary": summary,
                "report": report_text
            })

        except Exception as e:
            self.run_queue.put({"type": "error", "message": str(e)})

    def clear_output(self):
        style = THEME_STYLES[self.theme_var.get()]
        self.current_report = ""
        self.set_output(style["welcome"])
        self.scanned_card.value_label.configure(text="0")
        self.moved_card.value_label.configure(text="0")
        self.correct_card.value_label.configure(text="0")
        self.status_badge.configure(text=style["status_idle"])

    def on_closing(self):
        self.save_settings()
        self.destroy()


if __name__ == "__main__":
    app = SmartFileOrganizerApp()
    app.protocol("WM_DELETE_WINDOW", app.on_closing)
    app.mainloop()