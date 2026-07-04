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
        create_entry(
            supplier,
            1,
            2
        )

        # DBC File
        create_entry(
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
        
        parameter_row(charging,1,"AC Input Voltage","V")
        parameter_row(charging,3,"Input Frequency","Hz")
        parameter_row(charging,5,"OBC-DC Output Voltage","V")
        parameter_row(charging,7,"OBC-DC Output Current","A")
        parameter_row(charging,9,"HP DC-DC Load Current","A")
        

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

        parameter_row(discharge,1,"HP DC-DC Load Current","A")

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

        parameter_row(cycle,1,"Charging","min")
        parameter_row(cycle,3,"Rest","min")
        parameter_row(cycle,5,"Discharging","min")
        parameter_row(cycle,7,"Rest","min")

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
