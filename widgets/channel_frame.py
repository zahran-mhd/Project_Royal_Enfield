import tkinter as tk
import customtkinter as ctk
from widgets.dut_panel import DUTPanel

class ChannelFrame(tk.LabelFrame):

    def __init__(
        self,
        parent,
        channel_name,
        dut_names,
        items=None,
        stop_callback=None,
        value_width=13
    ):
        super().__init__(
            parent,
            text=channel_name,
            font=("Bookman Antiqua", 11, "bold"),  # smaller font
            padx=5,
            pady=5                           # was 10
        )

        # Header
        header = tk.Frame(self)
        header.pack(fill="x", pady=(0, 3))   # was (0,10)

        left = tk.Frame(header)
        left.pack(side="left")

        self.stop_callback = stop_callback

        self.cycle_lbl = tk.Label(
            left,
            text="Cycle : 0",
            font=("Bookman Antiqua", 9)
        )
        self.cycle_lbl.pack(anchor="w")

        self.time_lbl = tk.Label(
            left,
            text="Time Remaining : 00:00:00",
            font=("Bookman Antiqua", 9)
        )
        self.time_lbl.pack(anchor="w")

        # self.stop_btn = ctk.CTkButton(
        #     header,
        #     text="STOP",
        #     font=ctk.CTkFont(
        #         family="Bookman Antiqua",
        #         size=16,
        #         weight="bold"
        #     ),
        #     fg_color="#d9534f",
        #     hover_color="#15803D",
        #     text_color="white",
        #     width=30,
        #     height=2,
        #     # bg="#d9534f",
        #     # fg="white",
        #     command=self.on_stop_clicked
        # )
        self.stop_btn = ctk.CTkButton(
            header,
            text="⏹  STOP TEST",
            font=ctk.CTkFont(
                family="Bookman Antiqua",
                size=18,
                weight="bold"
            ),
            fg_color="#C62828",
            hover_color="#8E1B1B",
            text_color="#FFFFFF",
            corner_radius=12,
            border_width=1,
            border_color="#EF5350",
            width=135,
            height=44,
            cursor="hand2",
            command=self.on_stop_clicked
        )
        self.stop_btn.pack(side="right")

        # =========================
        # 3D STOP BUTTON
        # =========================

        # Shadow / depth layer
        # self.stop_shadow = ctk.CTkButton(
        #     header,
        #     text="",
        #     fg_color="#7F1D1D",
        #     hover_color="#7F1D1D",
        #     corner_radius=10,
        #     width=120,
        #     height=44,
        #     state="disabled"
        # )

        # self.stop_shadow.place(
        #     relx=0.95,
        #     rely=0.5,
        #     anchor="center",
        #     x=0,
        #     y=4
        # )

        # # Main button
        # self.stop_btn = ctk.CTkButton(
        #     header,
        #     text="⏹  STOP",
        #     font=ctk.CTkFont(
        #         family="Bookman Antiqua",
        #         size=15,
        #         weight="bold"
        #     ),
        #     fg_color="#DC3545",
        #     hover_color="#E84A59",
        #     text_color="white",
        #     corner_radius=10,
        #     border_width=1,
        #     border_color="#FF6B6B",
        #     width=120,
        #     height=44,
        #     cursor="hand2",
        #     command=self.on_stop_clicked
        # )

        # self.stop_btn.place(
        #     relx=0.95,
        #     rely=0.5,
        #     anchor="center",
        #     x=0,
        #     y=0
        # )
        

        # add_btn = ctk.CTkButton(
        #             header,
        #             text="+ Add Instrument",
        #             font=ctk.CTkFont(
        #                 family="Bookman Antiqua",
        #                 size=16,
        #                 weight="bold"
        #             ),
        #             fg_color="#16A34A",
        #             hover_color="#15803D",
        #             text_color="white",
        #             corner_radius=8,
        #             width=170,
        #             height=38,
        #             command=self.controller.add_data
        #         )
        # add_btn.pack(side="left")

        body = tk.Frame(self)
        body.pack(fill="both", expand=True)

        body.grid_columnconfigure(0, weight=1)
        body.grid_columnconfigure(1, weight=1)

        self.dut1 = DUTPanel(body, [dut_names[0]], items,value_width=value_width)
        self.dut1.grid(row=0, column=0, padx=3, pady=2, sticky="nsew")

        self.dut2 = DUTPanel(body, [dut_names[1]], items,value_width=value_width)
        self.dut2.grid(row=0, column=1, padx=3, pady=2, sticky="nsew")

    # ================= Update Methods =================
    def on_stop_clicked(self):
        if self.stop_callback:
            self.stop_callback()
 
 
    def set_cycle(self, current_cycle, total_cycles):
        self.cycle_lbl.config(
            text=f"Cycle : {current_cycle}/{total_cycles}"
        )

    def set_time_remaining(self, time_text):
        self.time_lbl.config(text=f"Time Remaining : {time_text}")
        
    def set_dut1_charging(self):
        self.dut1.show_charging()

    def set_dut1_discharging(self):
        self.dut1.show_discharging()

    def set_dut2_charging(self):
        self.dut2.show_charging()

    def set_dut2_discharging(self):
        self.dut2.show_discharging()

    def set_value(self, dut_index, panel, item_key, value):

        if dut_index == 0:

            self.dut1.set_value(
                panel,
                item_key,
                value
            )

        else:

            self.dut2.set_value(
                panel,
                item_key,
                value
            )