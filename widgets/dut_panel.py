import tkinter as tk
from widgets.status_panel import StatusPanel


class DUTPanel(tk.LabelFrame):
    def __init__(self, parent, dut_name,items=None):
        super().__init__(
            parent,
            text=dut_name,
            font=("Segoe UI", 11, "bold"),
            padx=5,
            pady=5
        )

        # Two equal columns
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Charging Panel
        self.charging = StatusPanel(self, "Charging",items)
        self.charging.grid(
            row=0,
            column=0,
            padx=(0, 5),
            pady=5,
            sticky="nsew"
        )

        # Discharging Panel
        self.discharging = StatusPanel(self, "Discharging",items)
        self.discharging.grid(
            row=0,
            column=1,
            padx=(5, 0),
            pady=5,
            sticky="nsew"
        )

    # ---------------- Update Methods ----------------

    # def update_charging(self, max_temp, min_temp):
    #     self.charging.max_lbl.config(text=max_temp)
    #     self.charging.min_lbl.config(text=min_temp)

    # def update_discharging(self, max_temp, min_temp):
    #     self.discharging.max_lbl.config(text=max_temp)
    #     self.discharging.min_lbl.config(text=min_temp)
        
        
    def update_charging(self, **kwargs):
        self.charging.update_values(**kwargs)

    def update_discharging(self, **kwargs):
        self.discharging.update_values(**kwargs)
        
    
    
    