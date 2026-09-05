import tkinter as tk


from widgets.ctk_table import CTkTableWidget

import customtkinter as ctk

from controllers.instrument_controller import InstrumentController


class   InstrumentConfig(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#eef2f7")
        self.context = context
        self.controller = InstrumentController(self, context)
      

        self.create_ui()
        self.create_table()
        # self.load_instruments()   
        self.controller.initialize()

    # ---------------- UI ----------------
    def create_ui(self):

        # Main Card
        self.card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )
        self.card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Header
        header = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        # Add Instrument Button
        add_btn = ctk.CTkButton(
            header,
            text="+ Add Instrument",
            font=ctk.CTkFont(
                family="Bookman Antiqua",
                size=16,
                weight="bold"
            ),
            fg_color="#16A34A",
            hover_color="#15803D",
            text_color="white",
            corner_radius=8,
            width=170,
            height=38,
            command=self.controller.add_data
        )
        add_btn.pack(side="left")

    # ---------------- TABLE ----------------
    def create_table(self):

        columns = (
     
            "SNo",
            "Instrument Name",
            "Address",
            "Serial Number",
            "Calibration Due Date",
            "Status",
          
        )

        table_frame = tk.Frame(self.card, bg="white", height=420)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        table_frame.pack_propagate(False)

        self.table = CTkTableWidget(
            table_frame,
            columns=columns
        )
        self.table.pack(fill="x", padx=20, pady=10)

        self.table.edit_callback = self.controller.edit_instrument
        self.table.delete_callback = self.controller.delete_instrument

    
    def display_instruments(self, instruments):

        self.table.clear()

        for index, ins in enumerate(instruments, start=1):
            status = "Connected" if ins.status == 1 else "Disconnected"
            self.table.insert(
                [
                    index,
                    ins.instrument_name,
                    ins.address,
                    ins.instrument_sno,
                    ins.calibration_due_date,
                    status
                ],
                key=(ins.instrument_id, ins.channel_id)
            )
    
