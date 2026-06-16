import tkinter as tk
from tkinter import ttk

class AlarmSettingsPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#f5f5f5")

        title = tk.Label(
            self,
            text="Alarm Settings pages",
            font=("Segoe UI", 18, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=10)

        container = tk.Frame(self, bg="#f5f5f5")
        container.pack(fill="both", expand=True, padx=20, pady=10)