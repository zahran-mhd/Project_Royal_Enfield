import tkinter as tk
from tkinter import ttk
from widgets.parameter_widget import *


class ParameterSettingsPage(tk.Frame):

    def __init__(self, parent):

        super().__init__(parent, bg="#f5f5f5")

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical"
        )

        scrollbar.pack(
            side="right",
            fill="y"
        )

        canvas = tk.Canvas(
            self,
            bg="#f5f5f5",
            highlightthickness=0,
            yscrollcommand=scrollbar.set
        )

        canvas.pack(
            side="left",
            fill="both",
            expand=True
        )

        scrollbar.config(command=canvas.yview)

        self.container = tk.Frame(
            canvas,
            bg="#f5f5f5"
        )

        canvas_window = canvas.create_window(
            (0, 0),
            window=self.container,
            anchor="nw"
        )

        self.container.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.bind(
            "<Configure>",
            lambda e: canvas.itemconfigure(
                canvas_window,
                width=e.width
            )
        )

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(
                int(-e.delta / 120),
                "units"
            )
        )
        self.entries = {}

        self.create_ui()
        
    def create_ui(self):

        # =================================================
        # DUT Supplier Settings
        # =================================================

        # DUT Supplier Settings Heading
        supplier_title = tk.Label(
            self.container,
            text="DUT Supplier Settings",
            font=("Arial", 22, "bold"),
            bg="#f5f5f5"
        )

        supplier_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        # White container
        supplier = tk.Frame(
            self.container,
            bg="white",
            padx=15,
            pady=15,
            bd=1,
            relief="solid"
        )

        supplier.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )
        # Make columns expand
        for i in range(5):
            supplier.columnconfigure(i, weight=1)

        # ---------------- Labels ----------------
        create_label(supplier, "DUT Type", 0, 0)
        create_label(supplier, "Bits Rate", 0, 2)
        create_label(supplier, "DBC File", 0, 3)

        # DUT Type Combobox
        self.dut_type = create_combobox(
            supplier,
            1,
            0,
            ["Supplier A", "Supplier B", "Supplier C"]
        )

        # Edit button
        create_button(
            supplier,
            "Edit",
            "#007bff",
            "white",
            1,
            1,
            command=self.edit_supplier
        )

        # Bits Rate
        self.entries["bits_rate"] = create_entry(
            supplier,
            1,
            2
        )

        self.entries["dbc_file"] = create_entry(
            supplier,
            1,
            3,
            width=40
        )

        # Upload / Remove buttons
        button_frame = tk.Frame(supplier, bg="white")
        button_frame.grid(
            row=1,
            column=4,
            sticky="w",
            padx=(10, 0)
        )

        create_button(
            button_frame,
            "Upload",
            "#28a745",
            "white",
            0,
            0
        )

        create_button(
            button_frame,
            "Remove",
            "#dc3545",
            "white",
            0,
            1
        )

        # =================================================
        # Endurance
        # =================================================

        title = tk.Label(
            self.container,
            text="Endurance",
            font=("Arial", 22, "bold"),
            bg="#f5f5f5"
        )
        title.pack(anchor="w", padx=20, pady=(10, 10))

        body = tk.Frame(
            self.container,
            bg="#f5f5f5"
        )
        body.pack(fill="x", padx=20, pady=(0,20))

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)
        body.columnconfigure(2, weight=1)

        # =================================================
        # Charging
        # =================================================

        charging = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )
        charging.grid(row=0, column=0, padx=10, sticky="nsew")

        charging.columnconfigure(0, weight=1)

        tk.Label(
            charging,
            text="Charging",
            bg="white",
            font=("Arial",16,"bold")
        ).grid(row=0,column=0,columnspan=2,sticky="w",padx=15,pady=(15,15))
        
        self.entries["ac_input_voltage"] = parameter_row(
            charging,
            1,
            "AC Input Voltage",
            "V"
        )
        self.entries["input_frequency"] = parameter_row(
            charging,
            3,
            "Input Frequency",
            "Hz"
        )
        self.entries["obc_output_voltage"] = parameter_row(
            charging,
            5,
            "OBC-DC Output Voltage",
            "V"
        )
        self.entries["obc_output_current"] = parameter_row(
            charging,
            7,
            "OBC-DC Output Current",
            "A"
        )
        self.entries["charging_hp_load_current"] = parameter_row(
            charging,
            9,
            "HP DC-DC Load Current",
            "A"
        )
                

        # =================================================
        # Discharging
        # =================================================

        discharge = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )
        discharge.grid(row=0,column=1,padx=10,sticky="nsew")

        discharge.columnconfigure(0,weight=1)

        tk.Label(
            discharge,
            text="Discharging",
            bg="white",
            font=("Arial",16,"bold")
        ).grid(row=0,column=0,columnspan=2,sticky="w",padx=15,pady=(15,15))

        self.entries["discharging_hp_load_current"] = parameter_row(
            discharge,
            1,
            "HP DC-DC Load Current",
            "A"
        )
        # =================================================
        # Cycle Time Settings
        # =================================================

        cycle = tk.Frame(
            body,
            bg="white",
            bd=1,
            relief="solid"
        )
        cycle.grid(row=0,column=2,padx=10,sticky="nsew")

        cycle.columnconfigure(0,weight=1)

        tk.Label(
            cycle,
            text="Cycle Time Settings",
            bg="white",
            font=("Arial",16,"bold")
        ).grid(row=0,column=0,columnspan=2,sticky="w",padx=15,pady=(15,15))

        self.entries["cycle_charging"] = parameter_row(
            cycle,
            1,
            "Charging",
            "min"
        )
        self.entries["cycle_rest1"] = parameter_row(
            cycle,
            3,
            "Rest",
            "min"
        )
        self.entries["cycle_discharging"] = parameter_row(
            cycle,
            5,
            "Discharging",
            "min"
        )
        self.entries["cycle_rest2"] = parameter_row(
            cycle,
            7,
            "Rest",
            "min"
        )


        # =================================================
        # LINE REGULATION
        # =================================================

        title = tk.Label(
            self.container,
            text="LINE REGULATION",
            font=("Arial",22,"bold"),
            bg="#f5f5f5"
        )
        title.pack(anchor="w", padx=20, pady=(20,10))

        line = tk.Frame(
            self.container,
            bg="white",
            bd=1,
            relief="solid",
            padx=20,
            pady=20
        )
        line.pack(fill="x", padx=20, pady=(0,20))

        # ---------------------------------------
        # Dwell Time
        # ---------------------------------------

        top = tk.Frame(line, bg="white")
        top.grid(row=0, column=0, columnspan=3, sticky="w", padx=20, pady=(5,25))

        create_label(top, "Dwell Time", 0, 0)

        self.entries["dwell_time"] = create_entry(
            top,
            0,
            1,
            width=8
        )

        create_label(top, "Sec", 0, 2)

        # Three equal columns
        line.grid_columnconfigure(0, weight=3)   
        line.grid_columnconfigure(1, weight=1)   

        # =======================================
        # LEFT PANEL
        # =======================================

        first_box = tk.Frame(
            line,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=15
        )
        first_box.grid_columnconfigure(0, weight=1)
        first_box.grid_columnconfigure(1, weight=1)

        first_box.grid(
            row=1,
            column=0,
            padx=(15,20),
            sticky="n"
        )

        left = tk.Frame(first_box, bg="white")

        left.grid(
            row=0,
            column=0,
            padx=(10,40),
            sticky="nw"
        )
        section_title(left, "OBC Line Regulation", 0, 0, 4)

        create_label(left, "DC-DC Load Current", 1, 0)

        self.entries["obc_load_current"] = create_entry(
            left,
            1,
            1,
            width=10
        )

        create_label(left, "A", 1, 2)

        # ----- One table with 4 columns -----

        table = tk.Frame(left, bg="white")
        table.grid(row=2, column=0, columnspan=4, pady=(15,0))

        table.grid_columnconfigure(0, minsize=80)
        table.grid_columnconfigure(1, minsize=130)
        table.grid_columnconfigure(2, minsize=80)
        table.grid_columnconfigure(3, minsize=130)

        tk.Label(
            table,
            text="Input Voltage (V)",
            bg="#f2f2f2",
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12    
        ).grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="nsew"
        )

        tk.Label(
            table,
            text="Input Frequency (Hz)",
            bg="#f2f2f2",
            relief="solid",
            bd=1,
            font=("Arial", 10, "bold"),
            padx=12,
            pady=12      # Increase this
        ).grid(
            row=0,
            column=2,
            columnspan=2,
            sticky="nsew"
        )
        for i in range(3):

            table_label(table, f"V{i+1}", i+1, 0)
            self.entries[f"voltage_{i+1}"] = table_entry(
                table,
                i+1,
                1
            )
            table_label(table, f"F{i+1}", i+1, 2)
            self.entries[f"frequency_{i+1}"] = table_entry(
                table,
                i+1,
                3
            )

        # =======================================
        # CENTER PANEL
        # =======================================

        step = tk.Frame(first_box, bg="white")

        for i in range(4):
            step.grid_rowconfigure(i, minsize=38)

        step.grid(
            row=0,
            column=1,
            padx=(40, 10),
            pady=(74, 0),
            sticky="nw"
        )
        tk.Frame(step, bg="white", height=74).grid(
            row=0,
            column=0,
            columnspan=3
        )
        table_header(step, "Steps", 0, 0)
        table_header(step, "HV Voltage(V)", 0, 1)
        table_header(step, "HV Load Current(A)", 0, 2)

        for i in range(3):
            table_label(step, f"Step{i+1}", i+1, 0)
            self.entries[f"step{i+1}_hv_voltage"] = table_entry(
                step,
                i+1,
                1
            )
            self.entries[f"step{i+1}_hv_current"] = table_entry(
                step,
                i+1,
                2
            )
        # =======================================
        # RIGHT PANEL
        # =======================================

        second_box = tk.Frame(
            line,
            bg="white",
            bd=1,
            relief="solid",
            padx=15,
            pady=15
        )

        second_box.grid(
            row=1,
            column=1,
            padx=(20,15),
            sticky="n"
        )

        right = tk.Frame(second_box, bg="white")
        right.grid(
            row=0,
            column=0,
            padx=10,
            sticky="n"
        )
        section_title(right, "HP DCDC Line Regulation", 0, 0, 2)

        create_label(right, "DC-DC Load Current", 1, 0)
        self.entries["hp_dcdc_load_current"] = create_entry(
            right,
            1,
            1,
            width=10
        )
        create_label(right, "A", 1, 2)

        table2 = tk.Frame(right, bg="white")
        table2.grid(row=2, column=0, columnspan=2, pady=(15,0))

        table_header(table2, "HV Voltage (V)", 0, 0)
        table2.grid_columnconfigure(0, weight=1)
        table2.grid_columnconfigure(1, weight=1)

        table2.grid_slaves(row=0, column=0)[0].grid(columnspan=2, sticky="ew")

        for i in range(3):

            table_label(table2, f"HV{i+1}", i+1, 0)
            self.entries[f"hp_voltage_{i+1}"] = table_entry(
                table2,
                i+1,
                1
            )

        # ==========================================
        # LOAD REGULATION
        # ==========================================

        title = tk.Label(
            self.container,
            text="LOAD REGULATION",
            font=("Arial", 22, "bold"),
            bg="#f5f5f5"
        )

        title.pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        load = tk.Frame(
            self.container,
            bg="white",
            bd=1,
            relief="solid"
        )

        load.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        # ---------------- Header ----------------

        header = load_header(load)

        self.entries["load_dwell_time"] = header["dwell_time"]
        self.entries["load_input_voltage"] = header["input_voltage"]
        self.entries["load_input_frequency"] = header["input_frequency"]

        # ---------------- Body ----------------

        body = tk.Frame(
            load,
            bg="white"
        )

        body.pack(
            fill="x",
            padx=50,
            pady=(5, 15)
        )

        body.columnconfigure(0, weight=1)
        body.columnconfigure(1, weight=1)

        # ---------------- Left Panel ----------------

        obc = load_regulation_panel(
            body,
            "OBC Load Regulation"
        )

        obc["panel"].grid(
            row=0,
            column=0,
            padx=40,
            sticky="n"
        )

        self.entries["obc_steps"] = obc["steps"]

        # ---------------- Right Panel ----------------

        hp = load_regulation_panel(
            body,
            "HP DCDC Load Regulation"
        )

        hp["panel"].grid(
            row=0,
            column=1,
            padx=40,
            sticky="n"
        )

        self.entries["hp_steps"] = hp["steps"]

        # =================================================
        # Buttons
        # ================================================

        
        button_frame = tk.Frame(
            self.container,
            bg="#f5f5f5"
        )

        button_frame.pack(
            pady=20
        )

        create_bottom_button(
            button_frame,
            "Add New",
            "#18b56b"
        ).pack(side="left", padx=10)

        create_bottom_button(
            button_frame,
            "Delete Existing",
            "#ef4444"
        ).pack(side="left", padx=10)

        create_bottom_button(
            button_frame,
            "Save Settings",
            "#2d6cdf"
        ).pack(side="left", padx=10)
            
    
    def edit_supplier(self):
        print("Selected Supplier:", self.dut_type.get())

        




