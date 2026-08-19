import tkinter as tk
from tkinter import ttk
from widgets.parameter_widget import *
from widgets.form_popup import FormPopup
from widgets.delete_popup import DeleteDutPopup
from tkinter import filedialog
import os
from tkinter import messagebox


class ParameterSettingsPage(tk.Frame):

    def __init__(self, parent,context):

        super().__init__(parent, bg="#f5f5f5")
        self.context = context
        self.controller = self.context.parameter_settings_controller

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
        create_label(supplier, "Bit Rate", 0, 1)
        create_label(supplier, "DBC File", 0, 3)

        # self.dut_map = {
        #     "Supplier A": 1,
        #     "Supplier B": 2,
        #     "Supplier C": 3
        # }
        rows = self.controller.get_all_duts()
        self.dut_map = {row["dut_name"]: row["dut_id"] for row in rows}

        # self.dut_type["values"] = list(self.dut_map.keys())

        # DUT Type Combobox
        self.dut_type = create_combobox(
            supplier,
            1,
            0,
            list(self.dut_map.keys())
        )

        self.dut_type.bind(
            "<<ComboboxSelected>>",
            self.on_dut_selected
        )

        # Bits Rate
        self.entries["bits_rate"] = create_entry(
            supplier,
            1,
            1
        )

        # Edit button
        create_button(
            supplier,
            "Edit",
            "#007bff",
            "white",
            1,
            2,
            command=self.edit_supplier
        )

        # # Bits Rate
        # self.entries["bits_rate"] = create_entry(
        #     supplier,
        #     1,
        #     2
        # )

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
            0,
            command=self.upload_dbc
        )

        create_button(
            button_frame,
            "Remove",
            "#dc3545",
            "white",
            0,
            1,
            command=self.remove_dbc
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

        self.entries["line_dwell_time"] = create_entry(
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

        self.entries["line_obc_load_current"] = create_entry(
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

        self.obc_panel = load_regulation_panel(
            body,
            "OBC Load Regulation"
        )

        self.obc_panel["panel"].grid(
            row=0,
            column=0,
            padx=40,
            sticky="n"
        )

        self.entries["obc_steps"] = self.obc_panel["steps"]

        # ---------------- Right Panel ----------------

        self.hp_panel = load_regulation_panel(
            body,
            "HP DCDC Load Regulation"
        )

        self.hp_panel["panel"].grid(
            row=0,
            column=1,
            padx=40,
            sticky="n"
        )

        self.entries["hp_steps"] = self.hp_panel["steps"]

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

        # create_bottom_button(
        #     button_frame,
        #     "Add New",
        #     "#18b56b"
        # ).pack(side="left", padx=10)

        add_btn = tk.Button(
                        button_frame,
                        text="Add New",
                        bg="#2d6cdf",
                        fg="white",
                        relief="flat",
                        command=self.add_new_dut,
                        font=("Arial", 11, "bold"),
                        padx=20,
                        pady=8
                    )
        
        add_btn.pack(side="left", padx=10)

        delete_btn = tk.Button(
                        button_frame,
                        text="Delete Existing",
                        bg="#ef4444",
                        fg="white",
                        relief="flat",
                        command=self.delete_dut,
                        font=("Arial", 11, "bold"),
                        padx=20,
                        pady=8
                    )
        
        delete_btn.pack(side="left", padx=10)

        # create_bottom_button(
        #     button_frame,
        #     "Delete Existing",
        #     "#ef4444"
        # ).pack(side="left", padx=10)

        # create_bottom_button(
        #     button_frame,
        #     "Save Settings",
        #     "#2d6cdf"
        # ).pack(side="left", padx=10)

       

        btn = tk.Button(
                button_frame,
                text="Save Settings",
                bg="#2d6cdf",
                fg="white",
                relief="flat",
                command=self.save_all_settings,
                font=("Arial", 11, "bold"),
                padx=20,
                pady=8
            )

        btn.pack(side="left", padx=10)
            
    # def on_dut_selected(self, event):
    #     dut_name = self.dut_type.get()
    #     dut_id = self.dut_map[dut_name]

    #     settings = self.controller.get_all_settings(dut_id)

    #     self.load_settings(settings)

    def on_dut_selected(self, event):

        dut_name = self.dut_type.get()

        dut_id = self.dut_map[dut_name]

        settings = self.controller.get_all_settings(dut_id)

        self.load_dut(settings["dut"])

        self.load_endurance(settings["endurance"])

        self.load_line_common(settings["line_common"])

        self.load_obc_inputs(settings["obc_line_inputs"])

        # self.load_hpdc_line_current(settings["hpdc_line_current"])

        self.load_hpdc_line(settings["hpdc_line_setting"])

        self.load_load_common(settings["load_common"])

        self.load_obc_regulation(settings["obc_load_settings"])

        self.load_hpdc_regulation(settings["hpdc_load_settings"])

        self.load_dbc_file(dut_id)

        # self.load_hpdc_regulation(settings["hpdc_load_regulation"])

    def load_dut(self, dut):
    
        if not dut:
            return

        self.set_entry("bits_rate", dut["dut_bit_rate"])


    def load_endurance(self, endurance):

        if not endurance:
            return

        self.set_entry("cycle_charging", endurance["charge_time"])
        self.set_entry("cycle_discharging", endurance["discharge_time"])

        self.set_entry("cycle_rest1", endurance["rest_time1"])
        self.set_entry("cycle_rest2", endurance["rest_time2"])

        self.set_entry("ac_input_voltage", endurance["ac_input_voltage"])
        self.set_entry("input_frequency", endurance["ac_input_frequency"])

        self.set_entry("obc_output_voltage", endurance["dc_output_voltage"])
        self.set_entry("obc_output_current", endurance["dc_output_current"])

        self.set_entry("charging_hp_load_current", endurance["char_dc_load_current"])
        self.set_entry("discharging_hp_load_current", endurance["dis_dc_load_current"])

    def load_line_common(self, common):

        if not common:
            return

        self.set_entry(
            "line_dwell_time",
            common["dwell_time"]
        )

    # def load_obc_inputs(self, inputs):

    #     if not inputs:
    #         return

    #     self.set_entry(
    #         "line_obc_load_current",
    #         inputs[0]["dc_load_current"]
    #     )

    #     for i, row in enumerate(inputs, start=1):

    #         self.set_entry(
    #             f"voltage_{i}",
    #             row["input_voltage"]
    #         )

    #         self.set_entry(
    #             f"frequency_{i}",
    #             row["input_frequency"]
    #         )

    # def load_obc_outputs(self, outputs):
    
    #         if not outputs:
    #             return
    
    #         # self.set_entry(
    #         #     "line_obc_load_current",
    #         #     outputs[0]["dc_load_current"]
    #         # )
    
    #         for i, row in enumerate(outputs, start=1):
    
    #             self.set_entry(
    #                 f"voltage_{i}",
    #                 row["input_voltage"]
    #             )
    
    #             self.set_entry(
    #                 f"frequency_{i}",
    #                 row["input_frequency"]
    #             )

    def load_obc_inputs(self, inputs):

        if not inputs:
            return

        self.set_entry(
            "line_obc_load_current",
            inputs[0]["dc_load_current"]
        )

        for i, item in enumerate(inputs, start=1):

            self.set_entry(
                f"voltage_{i}",
                item["input_voltage"]
            )

            self.set_entry(
                f"frequency_{i}",
                item["input_frequency"]
            )

            for output in item["outputs"]:

                step = output["step_no"]

                self.set_entry(
                    f"step{step}_hv_voltage",
                    output["hv_voltage"]
                )

                self.set_entry(
                    f"step{step}_hv_current",
                    output["hv_current"]
                )

    # def load_hpdc_line_current(self, common):
    
    #     if not common:
    #         return

    #     self.set_entry(
    #         "hp_dcdc_load_current",
    #         common["dc_load_current"]
    #     )

    # def load_hpdc_line(self, hpdc):

    #     if not hpdc:
    #         return

    #     print(hpdc)

    #     for step in hpdc["step_no"]:

    #         self.set_entry(
    #             f"hp_voltage_{step['step_no']}",
    #             step["hv_voltage"]
    #         )

    def load_hpdc_line(self, hpdc):

        if not hpdc:
            return

        self.set_entry(
            "hp_dcdc_load_current",
            hpdc["dc_load_current"]
        )

        for step in hpdc["hv_steps"]:

            self.set_entry(
                f"hp_voltage_{step['step_no']}",
                step["hv_voltage"]
            )

    def load_load_common(self, common):
        if not common:
            return

        self.set_entry(
            "load_dwell_time",
            common["dwell_time"]
        )

        self.set_entry(
            "load_input_frequency",
            common["input_frequency"]
        )

        self.set_entry(
            "load_input_voltage",
            common["input_voltage"]
        )

    def load_obc_regulation(self, regulation):

        if not regulation:
            return

        for step in regulation:

            widget = self.obc_panel["steps"][
                f"step{step['step_no']}"
            ]

            self.set_widget_entry(
                widget["step_voltage"],
                step["hv_voltage"]
            )

            for load, current in step["loads"].items():

                self.set_widget_entry(
                    widget["load_entries"][load],
                    current
                )

    def load_hpdc_regulation(self, regulation):
    
            if not regulation:
                return
    
            for step in regulation:
    
                widget = self.hp_panel["steps"][
                    f"step{step['step_no']}"
                ]
    
                self.set_widget_entry(
                    widget["step_voltage"],
                    step["hv_voltage"]
                )
    
                for load, current in step["loads"].items():
    
                    self.set_widget_entry(
                        widget["load_entries"][load],
                        current
                    )
    

    # def load_settings(self, settings):

    #     dut =settings["dut"]

    #     if dut:
        
    #         self.entries["bits_rate"].delete(0, "end")
    #         self.entries["bits_rate"].insert(
    #             0,
    #             dut["dut_bit_rate"]
    #         )

    #     endurance = settings["endurance"]

    #     if endurance:

    #         self.entries["cycle_charging"].delete(0, "end")
    #         self.entries["cycle_charging"].insert(
    #             0,
    #             endurance["charge_time"]
    #         )

    #         self.entries["cycle_discharging"].delete(0, "end")
    #         self.entries["cycle_discharging"].insert(
    #             0,
    #             endurance["discharge_time"]
    #         )

    #         self.entries["cycle_rest1"].delete(0, "end")
    #         self.entries["cycle_rest1"].insert(
    #             0,
    #             endurance["rest_time1"]
    #         )

    #         self.entries["cycle_rest2"].delete(0, "end")
    #         self.entries["cycle_rest2"].insert(
    #             0,
    #             endurance["rest_time2"]
    #         )

    #         self.entries["ac_input_voltage"].delete(0, "end")
    #         self.entries["ac_input_voltage"].insert(
    #             0,
    #             endurance["ac_input_voltage"]
    #         )

    #         self.entries["input_frequency"].delete(0, "end")
    #         self.entries["input_frequency"].insert(
    #             0,
    #             endurance["ac_input_frequency"]
    #         )

    #         self.entries["obc_output_voltage"].delete(0, "end")
    #         self.entries["obc_output_voltage"].insert(
    #             0,
    #             endurance["dc_output_voltage"]
    #         )

    #         self.entries["obc_output_current"].delete(0, "end")
    #         self.entries["obc_output_current"].insert(
    #             0,
    #             endurance["dc_output_current"]
    #         )

    #         self.entries["charging_hp_load_current"].delete(0, "end")
    #         self.entries["charging_hp_load_current"].insert(
    #             0,
    #             endurance["char_dc_load_current"]
    #         )

    #         self.entries["discharging_hp_load_current"].delete(0, "end")
    #         self.entries["discharging_hp_load_current"].insert(
    #             0,
    #             endurance["dis_dc_load_current"]
    #         )
            
    #     line_common = settings["line_common"]

    #     if line_common:
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )

    #     line_obc_input = settings["line_obc_input"]
        
    #     if line_obc_input:
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         self.entries["line_dwell_time"].delete(0, "end")
    #         self.entries["line_dwell_time"].insert(
    #             0,
    #             line_common["dwell_time"]
    #         )
    #         pass

    #     line_obc_output = settings["line_obc_output"]
        
    #     if line_obc_output:
    #         pass

    #     line_hpdc_input = settings["line_hpdc_input"]
        
    #     if line_hpdc_input:
    #         pass

    #     line_hpdc_output = settings["line_hpdc_output"]
        
    #     if line_hpdc_output:
    #         pass




    def edit_supplier(self):

        dut_name = self.dut_type.get()

        if not dut_name:
            return

        dut_id = self.dut_map[dut_name]

        print("Selected Supplier:", dut_name)
        print("DUT ID:", dut_id)

        def save(values):

            # values = [dut_name, bit_rate]

            values.insert(0, dut_id)      # [dut_id, dut_name, bit_rate]

            self.controller.edit_dut(values)

            rows = self.controller.get_all_duts()

            self.dut_map = {
                row["dut_name"]: row["dut_id"]
                for row in rows
            }

            self.dut_type["values"] = list(self.dut_map.keys())

        FormPopup(
            self,
            "Edit DUT",
            [
                "DUT Name",
                "Bit Rate [kbits/s]"
            ],
            save
        )

    def save_all_settings(self):
        data = self.collect_all_settings()
        self.controller.save_settings(data)

    def add_new_dut(self):
        print("clicked add new")
        def save(values):
            self.controller.add_dut(values)
            rows = self.controller.get_all_duts()
            self.dut_map = {row["dut_name"]: row["dut_id"] for row in rows}
    
            self.dut_type["values"] = list(self.dut_map.keys())
            
        FormPopup(
            self,
            "Add New Dut",
            [
                "DUT Name",
                "Bit Rate [kbits/s]"
            ],
            save
        )
        # self.controller.add_dut()

    # def delete_dut(self):
    #         print("clicked delete")
    #         def save(values):
    #             self.controller.delete_dut(values)
    #             rows = self.controller.get_all_duts()
    #             self.dut_map = {row["dut_name"]: row["dut_id"] for row in rows}
        
    #             self.dut_type["values"] = list(self.dut_map.keys())
                
    #         FormPopup(
    #             self,
    #             "Delete Dut",
    #             [
    #                 "DUT Name",
    #                 "Bit Rate [kbits/s]"
    #             ],
    #             save
    #         )
    
    def delete_dut(self):

        rows = self.controller.get_all_duts()

        DeleteDutPopup(
            self,
            rows,
            self.delete_selected_duts
        )

    def delete_selected_duts(self, dut_ids):

        self.controller.delete_duts(dut_ids)

        rows = self.controller.get_all_duts()

        self.dut_map = {
            row["dut_name"]: row["dut_id"]
            for row in rows
        }

        self.dut_type["values"] = list(self.dut_map.keys())

        if self.dut_map:
            self.dut_type.current(0)
        else:
            self.dut_type.set("")



    def collect_all_settings(self):
        dut_name = self.dut_type.get()
        return {
            
            "dut_id": self.dut_map[dut_name],

            "endurance": {

                "charge_time": self.get_float("cycle_charging"),
                "discharge_time": self.get_float("cycle_discharging"),
                "rest_time1": self.get_float("cycle_rest1"),
                "rest_time2": self.get_float("cycle_rest2"),

                "ac_input_voltage": self.get_float("ac_input_voltage"),
                "ac_input_frequency": self.get_float("input_frequency"),

                "dc_output_voltage": self.get_float("obc_output_voltage"),
                "dc_output_current": self.get_float("obc_output_current"),

                "char_dc_load_current": self.get_float("charging_hp_load_current"),
                "dis_dc_load_current": self.get_float("discharging_hp_load_current"),
            },

            "line_common": {

                "line_dwell_time": self.get_float("line_dwell_time")

            },

            "obc_line_inputs":[

                {
                    "dc_load_current": self.get_float("line_obc_load_current"),
                    "input_voltage":self.get_float("voltage_1"),
                    "input_frequency":self.get_float("frequency_1"),

                    "outputs":[
                        {"step_no":1,"hv_voltage":self.get_float("step1_hv_voltage"),"hv_current":self.get_float("step1_hv_current")},
                        {"step_no":2,"hv_voltage":self.get_float("step2_hv_voltage"),"hv_current":self.get_float("step2_hv_current")},
                        {"step_no":3,"hv_voltage":self.get_float("step3_hv_voltage"),"hv_current":self.get_float("step3_hv_current")}
                    ]
                },

                {
                    "dc_load_current": self.get_float("line_obc_load_current"),
                    "input_voltage":self.get_float("voltage_2"),
                    "input_frequency":self.get_float("frequency_2"),

                    "outputs":[
                        {"step_no":1,"hv_voltage":self.get_float("step1_hv_voltage"),"hv_current":self.get_float("step1_hv_current")},
                        {"step_no":2,"hv_voltage":self.get_float("step2_hv_voltage"),"hv_current":self.get_float("step2_hv_current")},
                        {"step_no":3,"hv_voltage":self.get_float("step3_hv_voltage"),"hv_current":self.get_float("step3_hv_current")}
                    ]
                },

                {
                    "dc_load_current": self.get_float("line_obc_load_current"),
                    "input_voltage":self.get_float("voltage_3"),
                    "input_frequency":self.get_float("frequency_3"),

                    "outputs":[
                        {"step_no":1,"hv_voltage":self.get_float("step1_hv_voltage"),"hv_current":self.get_float("step1_hv_current")},
                        {"step_no":2,"hv_voltage":self.get_float("step2_hv_voltage"),"hv_current":self.get_float("step2_hv_current")},
                        {"step_no":3,"hv_voltage":self.get_float("step3_hv_voltage"),"hv_current":self.get_float("step3_hv_current")}
                    ]
                }
            ],

            "hpdc_line":{

                "dc_load_current":self.get_float("hp_dcdc_load_current"),

                "hv_steps":[
                    {"step_no":1,"hv_voltage":self.get_float("hp_voltage_1")},
                    {"step_no":2,"hv_voltage":self.get_float("hp_voltage_2")},
                    {"step_no":3,"hv_voltage":self.get_float("hp_voltage_3")}
                ]

            },

            "load_common": {
            
                            "load_dwell_time": self.get_float("load_dwell_time"),
                            "load_input_voltage": self.get_float("load_input_voltage"),
                            "load_input_frequency": self.get_float("load_input_frequency")
                        },

            "obc_load_regulation": self.collect_obc_regulation(),

            "hpdc_load_regulation": self.collect_hpdc_regulation()

        }

    def collect_obc_regulation(self):

        regulation_data = []

        for step_name, step in self.obc_panel["steps"].items():

            regulation_data.append({

                "step_no": int(step_name.replace("step", "")),

                "hv_voltage": self.get_float_entry(step["step_voltage"]),

                "loads": {
                    load: self.get_float_entry(entry)
                    for load, entry in step["load_entries"].items()
                }

            })

        return regulation_data

    def collect_hpdc_regulation(self):
    
            hp_regulation_data = []
    
            for step_name, step in self.hp_panel["steps"].items():
    
                hp_regulation_data.append({
    
                    "step_no": int(step_name.replace("step", "")),
    
                    "hv_voltage": self.get_float_entry(step["step_voltage"]),
    
                    "loads": {
                        load: self.get_float_entry(entry)
                        for load, entry in step["load_entries"].items()
                    }
    
                })
    
            return hp_regulation_data

    def get_float_entry(self, entry):

        value = entry.get().strip()

        if value == "":
            return None

        return float(value)

    def get_float(self, key):
        entry = self.entries[key]
        text = entry.get().strip()

        try:
            return float(text) if text else 0.0
        except ValueError:
            return 0.0

        
    # def set_entry(self, key, value):

    #     entry = self.entries[key]

    #     entry.delete(0, "end")

    #     if value is not None:
    #         entry.insert(0, value)

    def set_entry(self, key, value):

        self.entries[key].delete(0, "end")

        if value is not None:
            self.entries[key].insert(0, value)

    def set_widget_entry(self, entry, value):

        entry.delete(0, "end")

        if value is not None:
            entry.insert(0, str(value))

   

    def upload_dbc(self):

        if not self.dut_type.get():
            messagebox.showwarning("Warning", "Please select a DUT first.")
            return

        file_path = filedialog.askopenfilename(
            title="Select DBC File",
            filetypes=[("DBC Files", "*.dbc")]
        )

        if not file_path:
            return

        dut_id = self.dut_map[self.dut_type.get()]

        self.controller.save_dbc_file(
            dut_id,
            file_path
        )

        self.entries["dbc_file"].delete(0, "end")
        self.entries["dbc_file"].insert(
            0,
            os.path.basename(file_path)
        )

    def remove_dbc(self):

        if not self.dut_type.get():
            return

        dut_id = self.dut_map[self.dut_type.get()]

        self.controller.remove_dbc_file(dut_id)

        self.entries["dbc_file"].delete(0, "end")

    def load_dbc_file(self, dut_id):

        self.entries["dbc_file"].delete(0, "end")

        dbc = self.controller.get_dbc_file(dut_id)

        if dbc:
            self.entries["dbc_file"].insert(0, dbc["file_name"])



