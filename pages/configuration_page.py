import tkinter as tk
from config_modules.instrument_config import InstrumentConfig
from config_modules.user_config import UserConfig


class ConfigurationPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#f5f5f5")

        self.create_header()
        self.create_tabs()

    def create_header(self):
        tk.Label(
            self,
            text="Configuration",
            font=("Segoe UI", 18, "bold"),
            bg="#f5f5f5"
        ).pack(anchor="w", padx=30, pady=20)

    def create_tabs(self):

    # Header Tab Bar
        tab_frame = tk.Frame(
            self,
            # bg="#ffffff",
            height=60,
            # bd=1,
            relief="solid"
        )
        tab_frame.pack(fill="x", padx=15, pady=(10, 0))

        # Content Area
        self.container = tk.Frame(
            self,
            bg="#eef2f7"
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Pages
        self.instrument_page = InstrumentConfig(self.container)
        self.user_page = UserConfig(self.container)

        self.instrument_page.pack(fill="both", expand=True)

        # Style
        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
            "bg": "#2563eb",
            "fg": "white",
            "activebackground": "#1d4ed8",
            "activeforeground": "white",
            "bd": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 8
        }

        self.instrument_btn = tk.Button(
            tab_frame,
            text="Channel 1 Configuration",
            command=self.show_instrument,
            **btn_style
        )
        self.instrument_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        self.user_btn = tk.Button(
            tab_frame,
            text="User Management",
            command=self.show_user,
            **btn_style
        )
        self.user_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

    def show_instrument(self):

        self.user_page.pack_forget()
        self.instrument_page.pack(fill="both", expand=True)

        self.instrument_btn.config(bg="#16a34a")
        self.user_btn.config(bg="#2563eb")


    def show_user(self):

        self.instrument_page.pack_forget()
        self.user_page.pack(fill="both", expand=True)

        self.user_btn.config(bg="#16a34a")
        self.instrument_btn.config(bg="#2563eb")