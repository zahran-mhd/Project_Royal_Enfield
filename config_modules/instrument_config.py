import tkinter as tk

from widgets.table_config import TableWidget
from widgets.form_popup import FormPopup
from database.repositories.instrument_repository import InstrumentRepository
from database.database_manager import DatabaseManager
from models.instrument_data import InstrumentData
from tkinter import messagebox


class InstrumentConfig(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#eef2f7")

        self.instrument_data = []
      
        self.db = DatabaseManager()
        self.instrument_repository = InstrumentRepository(self.db)
        self.create_ui()
        
        self.create_InstrumentTable()
        
        self.load_instruments()
    

    def create_ui(self):
        self.card = tk.Frame(self, bg="white")
        self.card.pack(fill="both", expand=True, padx=20, pady=20)

        # Header Frame
        header_frame = tk.Frame(self.card, bg="white")
        header_frame.pack(fill="x", padx=10, pady=(10, 15))

     

        # Add Button
        add_btn = tk.Button(
            header_frame,
            text="+ Add Instrument",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.add_data
        )
        add_btn.pack(side="left")
        
       
    def create_InstrumentTable(self):

        columns = (
            "S.No",
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
    key_column=0   # S.No column
)
 
        self.table.pack(fill="both", expand=True, padx=20, pady=10)
        self.table.delete_callback = self.delete_instrument
        self.table.edit_callback = self.edit_instrument
        
    def load_instruments(self):

        for item in self.table.tree.get_children():
            self.table.tree.delete(item)

        instruments = self.instrument_repository.get_all()

        print("Records from DB:", len(instruments))

        for instrument in instruments:

            row = [
                instrument.sno,
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status,
                "Edit | Delete"
            ]

            self.table.insert(row)
            
    def add_data(self):

        def save(values):

            sno = self.instrument_repository.get_next_sno()

            instrument = InstrumentData(
                sno=sno,
                instrument_name=values[0],
                address=values[1],
                instrument_sno=values[2],
                calibration_due_date=values[3],
                status=values[4],
                is_locked=0
            )

            self.instrument_repository.add(instrument)
           
            print("Inserted successfully")
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
        
    def delete_instrument(self, sno):

        confirm = messagebox.askyesno(
            "Delete Instrument",
            f"Are you sure you want to delete Instrument S.No {sno}?"
        )

        if not confirm:
            return

        instrument = self.instrument_repository.get_by_sno(sno)

        if not instrument:
            messagebox.showerror(
                "Error",
                "Instrument not found!"
            )
            return

        self.instrument_repository.delete(
            instrument.instrument_id
        )

        # messagebox.showinfo(
        #     "Success",
        #     "Instrument deleted successfully."
        # )

        self.load_instruments()
                        
    def edit_instrument(self, sno):

        instrument = self.instrument_repository.get_by_sno(sno)

        if not instrument:
            return

        def save(values):
            updated = InstrumentData(
                instrument_id=instrument.instrument_id,
                sno=instrument.sno,
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