import tkinter as tk
from tkinter import ttk


class ChannelCard(tk.LabelFrame):

    def __init__(
        self,
        context,
        parent,
        title,
        channel_name,
        dut_list,
        channel_id=None
    ):
        super().__init__(
            parent,
            text=title,
            font=("Segoe UI", 11, "bold"),
            bg="white",
            padx=15,
            pady=15
        )
        self.context = context
        self.test_controller=context.test_controller
        self.channel_name = channel_name
        self.channel_id = channel_id
        self.dut_list = dut_list

        self.create_widgets()

    def create_widgets(self):

        duts = self.dut_list

        row = 0

        # DUT Type
        tk.Label(
            self,
            text="Type of DUT",
            bg="white"
        ).grid(row=row, column=0, sticky="w", pady=5)

        self.supplier_combo = ttk.Combobox(
            self,
            values=[
                "Supplier A",
                "Supplier B",
                "Supplier C"
            ],
            state="readonly"
        )
        self.supplier_combo.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        row += 1

        # DUT Selection
        tk.Label(
            self,
            text="Select DUT",
            bg="white"
        ).grid(row=row, column=0, sticky="nw", pady=5)

        dut_frame = tk.Frame(self, bg="white")
        dut_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="w"
        )

        self.dut_vars = {}

        for dut in duts:
            var = tk.BooleanVar()
            self.dut_vars[dut] = var

            tk.Checkbutton(
                dut_frame,
                text=dut,
                variable=var,
                bg="white"
            ).pack(side="left", padx=10)

        row += 1

        ttk.Separator(self).grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=10
        )

        row += 1

        # Test Selection
        tk.Label(
            self,
            text="Test Type",
            bg="white"
        ).grid(row=row, column=0, sticky="nw")

        test_frame = tk.Frame(self, bg="white")
        test_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="w"
        )

        self.test_vars = {}

        tests = [
            "Endurance",
            "Line Regulation",
            "Load Regulation"
        ]
        self.selected_test = tk.StringVar(value="")

        for test in tests:
            tk.Radiobutton(
                test_frame,
                text=test,
                variable=self.selected_test,
                value=test,
                bg="white"
            ).pack(anchor="w")

        row += 1

        ttk.Separator(self).grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=10
        )

        row += 1

        # Test Name
        tk.Label(
            self,
            text="Test Name",
            bg="white"
        ).grid(row=row, column=0, sticky="w", pady=5)

        self.test_name = ttk.Entry(self)
        self.test_name.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        row += 1

        # Serial Numbers
        
        
        
        tk.Label(
            self,
            text="Serial Numbers",
            bg="white"
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            pady=5
        )

        serial_frame = tk.Frame(
            self,
            bg="white"
        )
        serial_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        self.serial_entries = {}

        for col, dut in enumerate(duts):

            tk.Label(
                serial_frame,
                text=f"{dut} SN",
                bg="white",
                font=("Segoe UI", 9)
            ).grid(
                row=0,
                column=col,
                sticky="w",
                padx=5
            )

            entry = ttk.Entry(serial_frame)

            entry.grid(
                row=1,
                column=col,
                sticky="ew",
                padx=5
            )

            self.serial_entries[dut] = entry

            serial_frame.columnconfigure(
                col,
                weight=1
            )

        row += 1
        
        
       
        # Cycles
        tk.Label(
            self,
            text="Cycles",
            bg="white"
        ).grid(row=row, column=0, sticky="w", pady=5)

        self.cycles_entry = ttk.Entry(self)
        self.cycles_entry.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        row += 1

        # Time Interval
        tk.Label(
            self,
            text="Interval (sec)",
            bg="white"
        ).grid(row=row, column=0, sticky="w", pady=5)

        self.time_entry = ttk.Entry(self)
        self.time_entry.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            pady=5
        )

        row += 1
        

        # Start Button
        self.start_btn = tk.Button(
            self,
            text="▶ Start Test",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            relief="flat",
            cursor="hand2",
            command=self.on_start_clicked
        )
        self.start_btn.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=(15, 0)
        )

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    def on_start_clicked(self):
        values = self.get_settings()

        self.test_controller.start_test(
            self.channel_id,
            values
    )
        
    def get_settings(self):
        return {
            "channel_id": self.channel_id,
            "supplier": self.supplier_combo.get(),
            "selected_duts": [
                dut
                for dut, var in self.dut_vars.items()
                if var.get()
            ],
            "test_type": self.selected_test.get(),
            "test_name": self.test_name.get(),
            "serial_numbers": {
                dut: entry.get()
                for dut, entry in self.serial_entries.items()
            },
            "cycles": self.cycles_entry.get(),
            "interval": self.time_entry.get()
        }