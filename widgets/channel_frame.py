import tkinter as tk
from widgets.dut_panel import DUTPanel

class ChannelFrame(tk.LabelFrame):
    def __init__(self, parent, channel_name, dut_names,items=None):
        super().__init__(
            parent,
            text=channel_name,
            font=("Segoe UI", 11, "bold"),  # smaller font
            padx=5,
            pady=5                           # was 10
        )

        # Header
        header = tk.Frame(self)
        header.pack(fill="x", pady=(0, 3))   # was (0,10)

        left = tk.Frame(header)
        left.pack(side="left")

        self.cycle_lbl = tk.Label(
            left,
            text="Cycle : 0",
            font=("Segoe UI", 9)
        )
        self.cycle_lbl.pack(anchor="w")

        self.time_lbl = tk.Label(
            left,
            text="Time Remaining : 00:00:00",
            font=("Segoe UI", 9)
        )
        self.time_lbl.pack(anchor="w")

        self.stop_btn = tk.Button(
            header,
            text="Stop",
            width=8,
            height=1,
            bg="#d9534f",
            fg="white"
        )
        self.stop_btn.pack(side="right")

        body = tk.Frame(self)
        body.pack(fill="both", expand=True)

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        self.dut1 = DUTPanel(body, [dut_names[0]], items)
        self.dut1.grid(row=0, column=0, padx=3, pady=2, sticky="nsew")

        self.dut2 = DUTPanel(body, [dut_names[1]], items)
        self.dut2.grid(row=0, column=1, padx=3, pady=2, sticky="nsew")

    # ================= Update Methods =================

    def set_cycle(self, cycle):
        self.cycle_lbl.config(text=f"Cycle : {cycle}")
        print(cycle)

    def set_time_remaining(self, time_text):
        self.time_lbl.config(text=f"Time Remaining : {time_text}")