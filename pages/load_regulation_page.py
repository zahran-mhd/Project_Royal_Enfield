import tkinter as tk

from widgets.regulation_table import RegulationTable


class LoadRegulationPage(tk.Frame):

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

        self.create_title()

        self.create_can_section()

        self.create_power_analyzer_section()

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    def create_title(self):

        title = tk.Label(
            self,
            text="Load Regulation",
            font=("Arial", 18, "bold"),
            bg="#f5f5f5",
            
        )

        title.pack(
           
            padx=15
     
        )

    # --------------------------------------------------
    # CAN SECTION
    # --------------------------------------------------

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

        title = tk.Label(
            section,
            text="OBC Load  Regulation - CAN Data",
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
            "HV Load(%)",
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

    # --------------------------------------------------
    # POWER ANALYZER SECTION
    # --------------------------------------------------

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

        title = tk.Label(
            section,
            text="OBC Load Regulation - Power Analyzer Data",
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
            "Set HV Curren(A)",
            "Input AC Voltage Power Analyzer (V)",
            "Input AC Current Power Analyzer (A)",
            "Input Power Factor (A)",
            "Input Power Power Analyzer (W)",
            "OBC Output Voltage Power Analyzer (V)",
            "OBC Output Current Power Analyzer (A)",
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