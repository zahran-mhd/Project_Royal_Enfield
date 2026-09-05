import tkinter as tk
from widgets.status_panel import StatusPanel


class DUTPanel(tk.LabelFrame):

    def __init__(self, parent, dut_name, items=None,value_width=13):
        super().__init__(
            parent,
            text=dut_name,
            font=("Bookman Antiqua", 11, "bold"),
            padx=5,
            pady=5
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Charging Panel
        self.charging_panel = StatusPanel(
            self,
            "Charging",
            items,
            value_width=value_width
        )

        self.charging_panel.grid(
            row=0,
            column=0,
            padx=(0, 5),
            pady=5,
            sticky="nsew"
        )
 
        # Discharging Panel
        self.discharging_panel = StatusPanel(
            self,
            "Discharging",
            items,
            value_width=value_width
        )

        self.discharging_panel.grid(
            row=0,
            column=1,
            padx=(5, 0),
            pady=5,
            sticky="nsew"
        )

        # Default state
        self.set_mode("charging")

    # -------------------------------------------------
    # Mode
    # -------------------------------------------------

    def set_mode(self, mode):

        if mode.lower() == "charging":

            self.charging_panel.set_active("#d4edda")
            self.discharging_panel.set_active("white")

        elif mode.lower() == "discharging":

            self.charging_panel.set_active("white")
            self.discharging_panel.set_active("#f8d7da")

    # -------------------------------------------------
    # Update values
    # -------------------------------------------------

    def set_value(self, panel, item_key, value):

        """
        panel : 'charging' or 'discharging'
        item_key : max / min / avg
        """

        if panel.lower() == "charging":

            self.charging_panel.set_value(
                item_key,
                value
            )

        elif panel.lower() == "discharging":

            self.discharging_panel.set_value(
                item_key,
                value
            )