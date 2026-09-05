# import tkinter as tk

# from widgets.regulation_table import RegulationTable


# class LoadRegulationPage(tk.Frame):

#     def __init__(
#         self,
#         parent,
#         context
#     ):

#         super().__init__(
#             parent,
#             bg="#F5F7FA"
#         )

#         self.context = context

#         self.create_title()

#         self.create_can_section()

#         self.create_power_analyzer_section()

#     # --------------------------------------------------
#     # TITLE
#     # --------------------------------------------------

#     def create_title(self):

#         title = tk.Label(
#             self,
#             text="Load Regulation",
#             font=("Bookman Antiqua", 18, "bold"),
#             bg="#f5f5f5",
            
#         )

#         title.pack(
           
#             padx=15
     
#         )

#     # --------------------------------------------------
#     # CAN SECTION
#     # --------------------------------------------------

#     def create_can_section(self):

#         section = tk.Frame(
#             self,
#             bg="white"
#         )

#         section.pack(
#             fill="x",
#             padx=16,
#             pady=10
#         )

#         title = tk.Label(
#             section,
#             text="OBC Load  Regulation - CAN Data",
#             bg="#2864E8",
#             fg="white",
#             font=("Bookman Antiqua", 14, "bold")
#         )

#         title.pack(
#             fill="x",
#             padx=10,
#             pady=10
#         )
#         sub_title = tk.Label(
#         section,
#         text="HV: 84 Vdc",
#         bg="#EAF2FF",
#         fg="#1F3F68",
#         font=("Bookman Antiqua", 12, "bold"),
#         anchor="w"
#     )

#         sub_title.pack(
#             fill="x",
#             padx=10,
#             pady=(0, 5),
#             ipady=6
#         )
            

#         columns = [
#             "HV Load(%)",
#             "Set HV Current(A)",
#             "Input AC Voltage CAN(V)",
#             "Input AC Current CAN(A)",
#             "Input Power CAN (W)",
#             "Output OBC Voltage CAN (V)",
#             "Output OBC Current CAN (A)",
#             "Output Power CAN (W)",
#             "Efficiency CAN (%)",
#             "Load Regulation (%)"
#         ]

#         table = RegulationTable(
#             section,
#             columns=columns,
#              row_values=[
#                 ( "No load","0.00"),
#         ("25","6.40"),
#         ("50","12.80"),
#         ("75","19.20"),
#         ("100","25.60"),
#     ]
#         )

#         table.pack(
#             fill="x",
#             padx=10,
#             pady=10
#         )

#     # --------------------------------------------------
#     # POWER ANALYZER SECTION
#     # --------------------------------------------------

#     def create_power_analyzer_section(self):

#         section = tk.Frame(
#             self,
#             bg="white"
#         )

#         section.pack(
#             fill="x",
#             padx=16,
#             pady=10
#         )

#         title = tk.Label(
#             section,
#             text="OBC Load Regulation - Power Analyzer Data",
#             bg="#2864E8",
#             fg="white",
#             font=("Bookman Antiqua", 14, "bold")
#         )
#         title.pack(
#                     fill="x",
#                     padx=10,
#                     pady=10
#                 )
#         sub_title = tk.Label(
#                 section,
#                 text="HV: 84 Vdc",
#                 bg="#EAF2FF",
#                 fg="#1F3F68",
#                 font=("Bookman Antiqua", 12, "bold"),
#                 anchor="w"
#             )
        
#         sub_title.pack(
#             fill="x",
#             padx=10,
#             pady=(0, 5),
#             ipady=6
#         )

#         columns = [
#             "HV Load (%)",
#             "Set HV Curren(A)",
#             "Input AC Voltage Power Analyzer (V)",
#             "Input AC Current Power Analyzer (A)",
#             "Input Power Factor (A)",
#             "Input Power Power Analyzer (W)",
#             "OBC Output Voltage Power Analyzer (V)",
#             "OBC Output Current Power Analyzer (A)",
#             "OBC Output Power Power Analyzer (W)",
#             "Efficiency Power Analyzer (%)",
#             "Load Regulation (%)"
#         ]

#         table = RegulationTable(
#             section,
#             columns=columns,
#             row_values=[
#                 ( "No load","0.00"),
#         ("25","6.40"),
#         ("50","12.80"),
#         ("75","19.20"),
#         ("100","25.60"),
#     ]
        
#         )

#         table.pack(
#             fill="x",
#             padx=10,
#             pady=10
#         )



import tkinter as tk

from widgets.regulation_table import RegulationTable


class LoadRegulationPage(tk.Frame):

    # ==========================================================
    # LOAD POINTS
    # ==========================================================

    LOAD_POINTS = [
        ("No Load", 0),
        ("25", 25),
        ("50", 50),
        ("75", 75),
        ("100", 100),
    ]

    def __init__(
        self,
        parent,
        context
    ):

        super().__init__(
            parent,
            bg="#F5F7FA"
        )

        self.context = context

        # ------------------------------------------------------
        # Current HV information
        # ------------------------------------------------------

        self.current_hv_voltage = None
        self.current_hv_step = 0
        self.total_hv_steps = 0

        # ------------------------------------------------------
        # Current load information
        # ------------------------------------------------------

        self.current_load_step = 0
        self.current_load_percent = 0
        self.current_hv_current = 0.0

        # ------------------------------------------------------
        # Table references
        # ------------------------------------------------------

        self.can_table = None
        self.analyzer_table = None

        # ------------------------------------------------------
        # Create UI
        # ------------------------------------------------------

        self.create_title()

        self.create_can_section()

        self.create_power_analyzer_section()
        
        
        self.create_hpdcdc_can_section()

    # --------------------------------------------------
    # TITLE
    # ==========================================================

    def create_title(self):

        title = tk.Label(
            self,
            text="Load Regulation",
            font=("Bookman Antiqua", 18, "bold"),
            bg="#F5F5F5"
        )

        title.pack(
            padx=15
        )

    # ==========================================================
    # CAN SECTION
    # ==========================================================

    def create_can_section(self):

        section = tk.Frame(
            self,
            bg="white"
        )

        section.pack(
            fill="x",
            padx=16,
            pady=10
        )

        # ------------------------------------------------------
        # Section title
        # ------------------------------------------------------

        title = tk.Label(
            section,
            text="OBC Load Regulation - CAN Data",
            bg="#2864E8",
            fg="white",
            font=("Bookman Antiqua", 14, "bold")
        )

        title.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ------------------------------------------------------
        # Dynamic subtitle
        # ------------------------------------------------------

        self.can_sub_title = tk.Label(
            section,
            text="HV: -- Vdc",
            bg="#EAF2FF",
            fg="#1F3F68",
            font=("Bookman Antiqua", 12, "bold"),
            anchor="w"
        )

        self.can_sub_title.pack(
            fill="x",
            padx=10,
            pady=(0, 5),
            ipady=6
        )

        # ------------------------------------------------------
        # Columns
        # ------------------------------------------------------

        columns = [

            "HV Load (%)",

            "Set HV Current(A)",

            "Input AC Voltage CAN(V)",

            "Input AC Current CAN(A)",

            "Input Power CAN (W)",

            "Output OBC Voltage CAN (V)",

            "Output OBC Current CAN (A)",

            "Output Power CAN (W)",

            "Efficiency CAN (%)",

            "Load Regulation (%)"

        ]

        # ------------------------------------------------------
        # Five load rows
        # ------------------------------------------------------

        row_values = [
            ("No load", "0.00"),
            ("25", "0.00"),
            ("50", "0.00"),
            ("75", "0.00"),
            ("100", "0.00"),
        ]

        self.can_table = RegulationTable(
            section,
            columns=columns,
            row_values=row_values
        )

        self.can_table.pack(
            fill="x",
            padx=10,
            pady=10
        )

    # ==========================================================
    # POWER ANALYZER SECTION
    # ==========================================================

    def create_power_analyzer_section(self):

        section = tk.Frame(
            self,
            bg="white"
        )

        section.pack(
            fill="x",
            padx=16,
            pady=10
        )

        # ------------------------------------------------------
        # Section title
        # ------------------------------------------------------

        title = tk.Label(
            section,
            text="OBC Load Regulation - Power Analyzer Data",
            bg="#2864E8",
            fg="white",
            font=("Bookman Antiqua", 14, "bold")
        )

        title.pack(
            fill="x",
            padx=10,
            pady=10
        )

        # ------------------------------------------------------
        # Dynamic subtitle
        # ------------------------------------------------------

        self.analyzer_sub_title = tk.Label(
            section,
            text="HV: -- Vdc",
            bg="#EAF2FF",
            fg="#1F3F68",
            font=("Bookman Antiqua", 12, "bold"),
            anchor="w"
        )

        self.analyzer_sub_title.pack(
            fill="x",
            padx=10,
            pady=(0, 5),
            ipady=6
        )

        # ------------------------------------------------------
        # Columns
        # ------------------------------------------------------

        columns = [

            "HV Load (%)",

            "Set HV Current(A)",

            "Input AC Voltage Power Analyzer (V)",

            "Input AC Current Power Analyzer (A)",

            "Input Power Factor",

            "Input Power Power Analyzer (W)",

            "OBC Output Voltage Power Analyzer (V)",

            "OBC Output Current Power Analyzer (A)",

            "OBC Output Power Power Analyzer (W)",

            "Efficiency Power Analyzer (%)",

            "Load Regulation (%)"

        ]

        # ------------------------------------------------------
        # Five load rows
        # ------------------------------------------------------

        row_values = [
            ("No load", "0.00"),
            ("25", "0.00"),
            ("50", "0.00"),
            ("75", "0.00"),
            ("100", "0.00"),
        ]

        self.analyzer_table = RegulationTable(
            section,
            columns=columns,
            row_values=row_values
        )

        self.analyzer_table.pack(
            fill="x",
            padx=10,
            pady=10
        )

    # ==========================================================
    # UPDATE ACTIVE ROW
    # ==========================================================

    def update_active_row(
        self,
        load_step,
        load_percent,
        hv_voltage,
        hv_current
    ):

        """
        Updates the currently running load row.

        load_step:
            1 = No Load
            2 = 25%
            3 = 50%
            4 = 75%
            5 = 100%
        """

        self.current_load_step = load_step
        self.current_load_percent = load_percent
        self.current_hv_voltage = hv_voltage
        self.current_hv_current = hv_current

        # ------------------------------------------------------
        # Update subtitles
        # ------------------------------------------------------

        hv_text = (
            f"HV: {hv_voltage:.1f} Vdc"
            f"   |   "
            f"Load: {load_percent}%"
            f"   |   "
            f"Set HV Current: {hv_current:.2f} A"
        )

        self.can_sub_title.config(
            text=hv_text
        )

        self.analyzer_sub_title.config(
            text=hv_text
        )

        # ------------------------------------------------------
        # Update current/load cells
        # ------------------------------------------------------

        self._set_table_cell(
            self.can_table,
            load_step - 1,
            "HV Load (%)",
            f"{load_percent}"
        )

        self._set_table_cell(
            self.can_table,
            load_step - 1,
            "Set HV Current(A)",
            f"{hv_current:.2f}"
        )

        self._set_table_cell(
            self.analyzer_table,
            load_step - 1,
            "HV Load (%)",
            f"{load_percent}"
        )

        self._set_table_cell(
            self.analyzer_table,
            load_step - 1,
            "Set HV Current(A)",
            f"{hv_current:.2f}"
        )

    # ==========================================================
    # CAN DATA UPDATE
    # ==========================================================

    def update_can_row(
        self,
        load_step,
        can_data
    ):

        row = load_step - 1

        if row < 0:
            return

        # ------------------------------------------------------
        # CAN values
        # ------------------------------------------------------

        input_voltage = self._get_value(
            can_data,
            [
                "Input AC Voltage",
                "Input AC Voltage CAN",
                "OBC Input Voltage"
            ]
        )

        input_current = self._get_value(
            can_data,
            [
                "Input AC Current",
                "Input AC Current CAN",
                "OBC Input Current"
            ]
        )

        input_power = self._get_value(
            can_data,
            [
                "Input Power",
                "Input Power CAN",
                "OBC Input Power"
            ]
        )

        output_voltage = self._get_value(
            can_data,
            [
                "Output OBC Voltage",
                "Output OBC Voltage CAN",
                "OBC Output Voltage"
            ]
        )

        output_current = self._get_value(
            can_data,
            [
                "Output OBC Current",
                "Output OBC Current CAN",
                "OBC Output Current"
            ]
        )

        output_power = self._get_value(
            can_data,
            [
                "Output Power",
                "Output Power CAN",
                "OBC Output Power"
            ]
        )

        efficiency = self._get_value(
            can_data,
            [
                "Efficiency",
                "Efficiency CAN",
                "OBC Efficiency"
            ]
        )

        load_regulation = self._get_value(
            can_data,
            [
                "Load Regulation",
                "Load Regulation (%)"
            ]
        )

        # ------------------------------------------------------
        # Update table
        # ------------------------------------------------------

        self._set_table_cell(
            self.can_table,
            row,
            "Input AC Voltage CAN(V)",
            self._format_value(input_voltage)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Input AC Current CAN(A)",
            self._format_value(input_current)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Input Power CAN (W)",
            self._format_value(input_power)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Output OBC Voltage CAN (V)",
            self._format_value(output_voltage)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Output OBC Current CAN (A)",
            self._format_value(output_current)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Output Power CAN (W)",
            self._format_value(output_power)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Efficiency CAN (%)",
            self._format_value(efficiency)
        )

        self._set_table_cell(
            self.can_table,
            row,
            "Load Regulation (%)",
            self._format_value(load_regulation)
        )

    # ==========================================================
    # POWER ANALYZER UPDATE
    # ==========================================================

    def update_power_analyzer_row(
        self,
        load_step,
        analyzer_data
    ):

        row = load_step - 1

        if row < 0:
            return

        # ------------------------------------------------------
        # Power Analyzer values
        # ------------------------------------------------------

        input_voltage = self._get_value(
            analyzer_data,
            [
                "Input AC Voltage",
                "Input AC Voltage Power Analyzer"
            ]
        )

        input_current = self._get_value(
            analyzer_data,
            [
                "Input AC Current",
                "Input AC Current Power Analyzer"
            ]
        )

        power_factor = self._get_value(
            analyzer_data,
            [
                "Power Factor",
                "Input Power Factor"
            ]
        )

        input_power = self._get_value(
            analyzer_data,
            [
                "Input Power",
                "Input Power Power Analyzer"
            ]
        )

        output_voltage = self._get_value(
            analyzer_data,
            [
                "OBC Output Voltage",
                "OBC Output Voltage Power Analyzer"
            ]
        )

        output_current = self._get_value(
            analyzer_data,
            [
                "OBC Output Current",
                "OBC Output Current Power Analyzer"
            ]
        )

        output_power = self._get_value(
            analyzer_data,
            [
                "OBC Output Power",
                "OBC Output Power Power Analyzer"
            ]
        )

        efficiency = self._get_value(
            analyzer_data,
            [
                "Efficiency",
                "Efficiency Power Analyzer"
            ]
        )

        load_regulation = self._get_value(
            analyzer_data,
            [
                "Load Regulation",
                "Load Regulation (%)"
            ]
        )

        # ------------------------------------------------------
        # Update table
        # ------------------------------------------------------

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Input AC Voltage Power Analyzer (V)",
            self._format_value(input_voltage)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Input AC Current Power Analyzer (A)",
            self._format_value(input_current)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Input Power Factor",
            self._format_value(power_factor)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Input Power Power Analyzer (W)",
            self._format_value(input_power)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "OBC Output Voltage Power Analyzer (V)",
            self._format_value(output_voltage)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "OBC Output Current Power Analyzer (A)",
            self._format_value(output_current)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "OBC Output Power Power Analyzer (W)",
            self._format_value(output_power)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Efficiency Power Analyzer (%)",
            self._format_value(efficiency)
        )

        self._set_table_cell(
            self.analyzer_table,
            row,
            "Load Regulation (%)",
            self._format_value(load_regulation)
        )

    # ==========================================================
    # TABLE CELL HELPER
    # ==========================================================

    def _set_table_cell(
        self,
        table,
        row,
        column,
        value
    ):

        if table is None:
            return

        try:

            table.update_cell(
                row,
                column,
                value
            )

        except Exception as e:

            print(
                f"Table update error "
                f"({column}, row={row}):",
                e
            )

    # ==========================================================
    # GET VALUE
    # ==========================================================

    def _get_value(
        self,
        data,
        keys
    ):

        if not data:
            return None

        for key in keys:

            if key in data:

                return data[key]

        return None

    # ==========================================================
    # FORMAT VALUE
    # ==========================================================

    def _format_value(
        self,
        value
    ):

        if value is None:
            return "--"

        try:

            return f"{float(value):.2f}"

        except (
            ValueError,
            TypeError
        ):

            return str(value)

    # ==========================================================
    # CLEAR MEASUREMENT TABLES
    # ==========================================================

    def clear_measurement_tables(self):

        # ------------------------------------------------------
        # Reset CAN table
        # ------------------------------------------------------

        if self.can_table is not None:

            for row in range(5):

                self._clear_row(
                    self.can_table,
                    row
                )

        # ------------------------------------------------------
        # Reset Power Analyzer table
        # ------------------------------------------------------

        if self.analyzer_table is not None:

            for row in range(5):

                self._clear_row(
                    self.analyzer_table,
                    row
                )

    # ==========================================================
    # CLEAR SINGLE ROW
    # ==========================================================

    def _clear_row(
        self,
        table,
        row
    ):

        if table is None:
            return

        # ------------------------------------------------------
        # Leave load column and set current to 0
        # ------------------------------------------------------

        load_name = [
            "No load",
            "25",
            "50",
            "75",
            "100"
        ]

        self._set_table_cell(
            table,
            row,
            "HV Load (%)",
            load_name[row]
        )

        self._set_table_cell(
            table,
            row,
            "Set HV Current(A)",
            "0.00"
        )

        # ------------------------------------------------------
        # Clear all remaining columns
        # ------------------------------------------------------

        if table == self.can_table:

            columns = [

                "Input AC Voltage CAN(V)",

                "Input AC Current CAN(A)",

                "Input Power CAN (W)",

                "Output OBC Voltage CAN (V)",

                "Output OBC Current CAN (A)",

                "Output Power CAN (W)",

                "Efficiency CAN (%)",

                "Load Regulation (%)"

            ]

        else:

            columns = [

                "Input AC Voltage Power Analyzer (V)",

                "Input AC Current Power Analyzer (A)",

                "Input Power Factor",

                "Input Power Power Analyzer (W)",

                "OBC Output Voltage Power Analyzer (V)",

                "OBC Output Current Power Analyzer (A)",

                "OBC Output Power Power Analyzer (W)",

                "Efficiency Power Analyzer (%)",

                "Load Regulation (%)"

            ]

        for column in columns:

            self._set_table_cell(
                table,
                row,
                column,
                "--"
            )

    # ==========================================================
    # TEST COMPLETED
    # ==========================================================

    def test_completed(self):

        self.can_sub_title.config(
            text=(
                "Load Regulation Test Completed"
            )
        )

        self.analyzer_sub_title.config(
            text=(
                "Load Regulation Test Completed"
            )
        )

        print(
            "Load Regulation page: "
            "test completed"
        )

    # ==========================================================
    # TEST FAILED
    # ==========================================================

    def test_failed(
        self,
        error
    ):

        self.can_sub_title.config(
            text=(
                f"Load Regulation Test Failed: "
                f"{error}"
            )
        )

        self.analyzer_sub_title.config(
            text=(
                f"Load Regulation Test Failed: "
                f"{error}"
            )
        )

        print(
            "Load Regulation page: "
            "test failed:",
            error
        )

    # ==========================================================
    # TEST STOPPED
    # ==========================================================

    def test_stopped(self):

        self.can_sub_title.config(
            text=(
                "Load Regulation Test Stopped"
            )
        )

        self.analyzer_sub_title.config(
            text=(
                "Load Regulation Test Stopped"
            )
        )

        print(
            "Load Regulation page: "
            "test stopped"
        )


        
        
    # --------------------------------------------------
        # CAN SECTION
        # --------------------------------------------------
    
    def create_hpdcdc_can_section(self):

        section = tk.Frame(
            self,
            bg="white"
        )

        section.pack(
            fill="x",
            padx=16,
            pady=10
        )

        title = tk.Label(
            section,
            text="HP DCDC - CAN Data",
            bg="#2864E8",
            fg="white",
            font=("Arial", 14, "bold")
        )

        title.pack(
            fill="x",
            padx=10,
            pady=10
        )
        sub_title = tk.Label(
        section,
        text="HV: 84 Vdc",
        bg="#EAF2FF",
        fg="#1F3F68",
        font=("Arial", 12, "bold"),
        anchor="w"
    )

        sub_title.pack(
            fill="x",
            padx=10,
            pady=(0, 5),
            ipady=6
        )
            

        columns = [
              "HV Load (%)",
            "Set HP DCDC Curren(A)",
            "Input HV Voltage CAN(V)",
            "Input HV Current CAN(V)",
        
            "Input Power CAN (W)",
            "Output HP DCDC Voltage CAN (V)",
            "Output HP DCDC Current CAN (A)",
            "Output Power CAN (W)",
            "Efficiency CAN (%)",
            "Load Regulation (%)"
        ]

        table = RegulationTable(
            section,
            columns=columns,
                row_values=[
                ( "No load","0.00"),
        ("25","6.40"),
        ("50","12.80"),
        ("75","19.20"),
        ("100","25.60"),
    ]
        )

        table.pack(
            fill="x",
            padx=10,
            pady=10
        )# --------------------------------------------------
            # POWER ANALYZER SECTION
            # --------------------------------------------------
        
    def create_hpdcdc_power_analyzer_section(self):

        section = tk.Frame(
            self,
            bg="white"
        )

        section.pack(
            fill="x",
            padx=16,
            pady=10
        )

        title = tk.Label(
            section,
            text="HP DCDC Load Regulation - Power Analyzer Data",
            bg="#2864E8",
            fg="white",
            font=("Arial", 14, "bold")
        )
        title.pack(
                    fill="x",
                    padx=10,
                    pady=10
                )
        sub_title = tk.Label(
                section,
                text="HV: 84 Vdc",
                bg="#EAF2FF",
                fg="#1F3F68",
                font=("Arial", 12, "bold"),
                anchor="w"
            )
        
        sub_title.pack(
            fill="x",
            padx=10,
            pady=(0, 5),
            ipady=6
        )

        columns = [
            "HV Load (%)",
            "Set HP DCDC Curren(A)",
            "Input HV Voltage Power Analyzer (V)",
            "Input HV Current Power Analyzer (A)",
            # "Input Power Factor (A)",
            "Input Power Power Analyzer (W)",
            "Output HP DCDC Voltage Power Analyzer (V)",
            "Output HP DCDC Current Power Analyzer (A)",
            "OBC Output Power Power Analyzer (W)",
            "Efficiency Power Analyzer (%)",
            "Load Regulation (%)"
        ]

        table = RegulationTable(
            section,
            columns=columns,
            row_values=[
                ( "No load","0.00"),
        ("25","6.40"),
        ("50","12.80"),
        ("75","19.20"),
        ("100","25.60"),
    ]
        
        )

        table.pack(
            fill="x",
            padx=10,
            pady=10
        )
        




