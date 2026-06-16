import tkinter as tk
from widgets.table_config import TableWidget
from widgets.form_popup import FormPopup


class UserConfig(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#eef2f7")

        self.user_data = []

        self.create_ui()
        self.user_tabel()

    def create_ui(self):
        self.card = tk.Frame(self, bg="white")
        self.card.pack(fill="both", expand=True, padx=10, pady=10)

        tk.Button(
            self.card,
            text="+ Add User",
            bg="#16a34a",
            fg="white",
            command=self.add_user
        ).pack(anchor="w", padx=20, pady=10)
        
    def add_user(self):
        print("added user succesfully")
        
        
    def user_tabel(self):

        columns = (
            "S.No",
            "Username",
            "Role",
            "Status",
            "Action",
            
        )

        self.table = TableWidget(self.card, columns)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)
        
    def add_data(self):
        

        # def save(values):

        #     sno = len(self.instrument_data) + 1

        #     row = [
        #         sno,
        #         values[0],
        #         values[1],
        #         values[2],
        #         values[3],
        #         values[4],
        #         "Edit | Delete"
        #     ]

        #     self.instrument_data.append(row)
        #     self.table.insert(row)

        # FormPopup(
        #     self,
        #     "Add User",
        #     [
        #         "Instrument Name",
        #         "Address",
        #         "Serial Number",
        #         "Calibration Date",
        #         "Status"
        #     ],
        #     save
        # )
        print("added data succesfully")