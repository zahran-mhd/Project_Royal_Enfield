import tkinter as tk

from widgets.historical_trend_widget import (
    HistoricalTrendWidget
)


class HistoricalTrendPage(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#E9EDF2")

        title = tk.Label(
            self,
            text="Historical Trend",
            font=("Segoe UI", 20, "bold"),
            bg="#E9EDF2",
            fg="#0B1B44"
        )

        title.pack(
            anchor="w",
            padx=25,
            pady=(20, 10)
        )

        HistoricalTrendWidget(
            self,
            app
        ).pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )