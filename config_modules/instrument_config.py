import tkinter as tk
from tkinter import messagebox

from widgets.table_widgets import TableWidget
from widgets.form_popup import FormPopup

from models.instrument_data import InstrumentData


class InstrumentConfig(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#eef2f7")
        self.context = context
        self.instrument_repository = self.context.instrument_repository
        self.channel_repository = self.context.channel_repository

        self.selected_channel_id = None

        channels = self.channel_repository.get_all_channels()
        if channels:
            self.selected_channel_id = channels[0]["ChannelID"]

        self.create_ui()
        self.create_table()
        self.load_instruments()

    # ---------------- UI ----------------
    def create_ui(self):
        self.card = tk.Frame(self, bg="white")
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        header = tk.Frame(self.card, bg="white")
        header.pack(fill="x", padx=10, pady=(10, 15))

        tk.Button(
            header,
            text="+ Add Instrument",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.add_data
        ).pack(side="left")

    # ---------------- TABLE ----------------
    def create_table(self):

        columns = (
     
            "SNo",
            "Instrument Name",
            "Address",
            "Serial Number",
            "Calibration Due Date",
            "Status",
            "Action"
        )

        self.table = TableWidget(
            self.card,
            columns,
         
            key_column=0   # instrument_id is KEY
        )

        self.table.pack(fill="both", expand=True, padx=20, pady=10)

        self.table.edit_callback = self.edit_instrument
        self.table.delete_callback = self.delete_instrument

    # ---------------- CHANNEL ----------------
    def set_channel(self, channel_id):
        self.selected_channel_id = channel_id
        self.load_instruments()

    # ---------------- LOAD ----------------
    def load_instruments(self):

        self.table.clear()

        if not self.selected_channel_id:
            return

        instruments = self.instrument_repository.get_by_channel(
            self.selected_channel_id
        )

        # print("Selected Channel:", self.selected_channel_id)
        # print("Found:", len(instruments))

        for index, ins in enumerate(instruments, start=1):

            self.table.insert(
                [
                    index,                      # Display S.No
                    ins.instrument_name,
                    ins.address,
                    ins.instrument_sno,
                    ins.calibration_due_date,
                    ins.status
                ],
                key=ins.instrument_id          # Real DB ID
            )

    # ---------------- ADD ----------------
    def add_data(self):

        def save(values):

            instrument = InstrumentData(
                instrument_name=values[0],
                address=values[1],
                instrument_sno=values[2],
                calibration_due_date=values[3],
                status=values[4],
                channel_id=self.selected_channel_id
            )

            self.instrument_repository.add(instrument)
            self.load_instruments()

        FormPopup(
            self,
            "Add Instrument",
            [
                "Instrument Name",
                "Address",
                "Serial Number",
                "Calibration Date",
                "Status"
            ],
            save
        )
    # ---------------- DELETE ----------------
    def delete_instrument(self, instrument_id):

        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this instrument?"
        )

        if not confirm:
            return

        self.instrument_repository.delete(instrument_id)
        self.load_instruments()

    # ---------------- EDIT ----------------
    def edit_instrument(self, instrument_id):
        print("Edit Instrument ID:", instrument_id)

        instrument = self.instrument_repository.get_by_id(instrument_id)
        if instrument:
            print("Channel:", instrument.channel_id)
        if not instrument:
            return

        def save(values):

            updated = InstrumentData(
                instrument_id=instrument.instrument_id,
                instrument_name=values[0],
                address=values[1],
                instrument_sno=values[2],
                calibration_due_date=values[3],
                status=values[4],
                is_locked=instrument.is_locked,
                channel_id=instrument.channel_id,
                is_shared=instrument.is_shared
            )

            self.instrument_repository.update(updated)
            self.load_instruments()

        FormPopup(
            self,
            "Edit Instrument",
            [
                "Instrument Name",
                "Address",
                "Serial Number",
                "Calibration Date",
                "Status"
            ],
            save,
            prefill=[
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status
            ]
        )