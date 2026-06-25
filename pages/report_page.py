import tkinter as tk

from widgets.reports_widget import ReportsWidget


class ReportsPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        # ================= TITLE =================
        title = tk.Label(
            self,
            text="Reports",
            font=("Segoe UI", 22, "bold"),
            bg="#EEF2F7",
            fg="#0B1B44"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        ReportsWidget(
            self
        ).pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(10, 20)
        )