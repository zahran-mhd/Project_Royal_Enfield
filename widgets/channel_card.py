import tkinter as tk
from tkinter import ttk
from widgets.radioButton import CustomRadioButton


class ChannelCard(tk.LabelFrame):

    def __init__(
        self,
        context,
        parent,
        title,
        channel_name,
        dut_list,
        channel_id=None,
        dut_callback=None,
        start_callback=None
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
        self.dut_callback = dut_callback
        self.start_callback = start_callback
        self.dut_list = dut_list

        self.create_widgets()

    def create_widgets(self):

        duts = self.dut_list

        row = 0

        # DUT Type
        tk.Label(
            self,
            text="Type of DUT",
            bg="white",
            cursor="hand2"
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
            pady=5,
            
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
                bg="white",
                cursor="hand2",
                  command=self.on_checkbox_changed,
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
        
        self.selected_test = tk.StringVar(value="")
        tests = [
            "Endurance",
            "Line Regulation",
            "Load Regulation"
        ]
        

        
        for test in tests:
            CustomRadioButton(
                test_frame,
                text=test,
                variable=self.selected_test,
                value=test
            ).pack(anchor="w", pady=2)

        # Ensure nothing is selected
        self.selected_test.set("")

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
            text="Start Test",
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
        
    def on_checkbox_changed(self):

        selected = [
            dut
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        print("ChannelCard:", selected)  

        if self.dut_callback:
            self.dut_callback(self.channel_id, self.channel_name, selected)
            
    def on_start_clicked(self):
        
        

        values = self.get_settings()

        # Notify parent page if callback exists
        if self.start_callback:
            self.start_callback(self)
            
      
        # Start the test
        self.test_controller.start_test(
            self.channel_id,
            values
        )


    def disable_start_button(self):
        self.start_btn.config(state="disabled")


    def enable_start_button(self):
        self.start_btn.config(state="normal")

   
    def get_settings(self):
        
        selected_duts = [
        dut
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        dut_a = self.dut_list[0]
        dut_b = self.dut_list[1]

        # Use the first selected DUT as dut_id
        dut_id = int(selected_duts[0].replace("DUT", "")) if selected_duts else None
        print(dut_id)
        return {
    "channel_id": self.channel_id,
    "dut_id": dut_id,

    "selected_duts": selected_duts,   # <-- Add this back
     "dut_a_name": dut_a,
    "dut_b_name": dut_b,

    "use_dut_a": 1 if dut_a in selected_duts else 0,
    "use_dut_b": 1 if dut_b in selected_duts else 0,

    "supplier": self.supplier_combo.get(),
    "test_type": self.selected_test.get(),
    "test_name": self.test_name.get(),

    "dut_a_serial_no": self.serial_entries[dut_a].get(),
    "dut_b_serial_no": self.serial_entries[dut_b].get(),

    "no_of_cycles": self.cycles_entry.get(),
    "interval_seconds": self.time_entry.get()
}