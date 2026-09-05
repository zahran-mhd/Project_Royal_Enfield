
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
            font=("Bookman Antiqua", 18, "bold"),
            bg="#f5f5f5",
          
        )

        title.pack(

            padx=15,
           
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