import tkinter as tk
from widgets.status_panel import StatusPanel


class DUTPanel(tk.LabelFrame):
    def __init__(self, parent, dut_name, items=None):
        super().__init__(
            parent,
            text=dut_name,
            font=("Segoe UI", 11, "bold"),
            padx=5,
            pady=5
        )

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Charging Panel
        self.charging_panel = StatusPanel(self, "Charging", items)
        self.charging_panel.grid(
            row=0,
            column=0,
            padx=(0, 5),
            pady=5,
            sticky="nsew"
        )
 
        # Discharging Panel
        self.discharging_panel = StatusPanel(self, "Discharging", items)
        self.discharging_panel.grid(
            row=0,
            column=1,
            padx=(5, 0),
            pady=5,
            sticky="nsew"
        )

        # Default state
        self.set_mode("charging")

    def set_mode(self, mode):

        if mode.lower() == "charging":
            # Charging panel = Green
            self.charging_panel.set_active("#d4edda")

            # Discharging panel = White
            self.discharging_panel.set_active("white")

        elif mode.lower() == "discharging":
            # Charging panel = White
            self.charging_panel.set_active("white")

            # Discharging panel = Red
            self.discharging_panel.set_active("#f8d7da")

        

    # ---------------- Update Methods ----------------

    # def update_charging(self, max_temp, min_temp):
    #     self.charging.max_lbl.config(text=max_temp)
    #     self.charging.min_lbl.config(text=min_temp)

    # def update_discharging(self, max_temp, min_temp):
    #     self.discharging.max_lbl.config(text=max_temp)
    #     self.discharging.min_lbl.config(text=min_temp)
        
 
    
    