import tkinter as tk

from widgets.regulation_table import RegulationTable
from controllers.line_regulation_controller import LineRegulationController



class LineRegulationPage(tk.Frame):

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

        self.controller = LineRegulationController(
        context=self.context
    )

        self.create_title()

        self.create_can_section()

        self.create_power_analyzer_section()

    # --------------------------------------------------
    # TITLE
    # --------------------------------------------------

    def create_title(self):

        title = tk.Label(
            self,
            text="Line Regulation",
            font=("Segoe UI", 18, "bold"),
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
            text="OBC Line Regulation - CAN Data",
            bg="#2864E8",
            fg="white",
            font=("Arial", 14, "bold")
        )

        title.pack(
            fill="x",
            padx=10,
            pady=10
        )
        
        self.sub_title = tk.Label(
                    section,
                    text="Set HV Voltage: 84Vdc| HV Current 25.6A",
                    bg="#EAF2FF",
    fg="#1F3F68",
                    font=("Arial", 12, "bold"),
                    anchor="w"
                )
        
        self.sub_title.pack(
    fill="x",
    padx=10,
    pady=(0, 5),
    ipady=6
)
     

        columns = [
            "Set AC Voltage (V)",
            "Input AC Voltage CAN (V)",
            "Input AC Current CAN (A)",
            # "Input Power Factor (A)",
            "Input Power CAN (W)",
            "Output OBC Voltage CAN (V)",
            "Output OBC Current CAN (A)",
            "Output Power CAN (W)",
            "Efficiency CAN (%)",
            "Line Regulation (%)"
        ]

        self.can_table = RegulationTable(
            section,
            columns=columns,
               row_values=[
                    ("100",),
                    ("230",),
                    ("270",)
                
    ]
            
        )

        self.can_table.pack(
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
            text="OBC Line Regulation - Power Analyzer Data",
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
            text="Set HV Voltage: 84Vdc| HV Current 25.6A",
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
            "Set AC Voltage (V)",
            "Input AC Voltage Power Analyzer (V)",
            "Input AC Current Power Analyzer (A)",
            "Input Power Factor (A)",
            "Input Power Power Analyzer (W)",
            "OBC Output Voltage Power Analyzer (V)",
            "OBC Output Current Power Analyzer (A)",
            "OBC Output Power Power Analyzer (W)",
            "Efficiency Power Analyzer (%)",
            "Line Regulation (%)"
        ]

        self.power_analyzer_table = RegulationTable(
            section,
            columns=columns,
             row_values=[
                    ("100",),
                    ("230",),
                    ("270",)
                ]
            
        )

        self.power_analyzer_table.pack(
            fill="x",
            padx=10,
            pady=10
        )

    def update_test_settings(self, settings):

        print("Line Regulation settings:")
        print(settings)


    def update_active_step(
        self,
        hv_step,
        total_hv_steps,
        ac_step,
        total_ac_steps,
        hv_voltage,
        hv_current,
        ac_voltage,
        ac_frequency,
        dwell_time
    ):

        self.step_label.configure(
            text=(
                f"HV Step {hv_step}/{total_hv_steps}   |   "
                f"AC Step {ac_step}/{total_ac_steps}"
            )
        )

        self.hv_voltage_label.configure(
            text=f"HV Voltage: {hv_voltage:.2f} V"
        )

        self.hv_current_label.configure(
            text=f"HV Current: {hv_current:.2f} A"
        )

        self.ac_voltage_label.configure(
            text=f"AC Voltage: {ac_voltage:.1f} V"
        )

        self.ac_frequency_label.configure(
            text=f"AC Frequency: {ac_frequency:.1f} Hz"
        )

        self.dwell_label.configure(
            text=f"Dwell Time: {dwell_time} sec"
        )

    # def update_active_step(
    #     self,
    #     step_no,
    #     total_steps,
    #     ac_voltage,
    #     frequency,
    #     hv_voltage,
    #     hv_current,
    #     dwell_time
    # ):

    #     self.current_step_label.configure(
    #         text=f"Step {step_no} / {total_steps}"
    #     )

    #     self.ac_voltage_label.configure(
    #         text=f"AC Voltage: {ac_voltage:.1f} V"
    #     )

    #     self.frequency_label.configure(
    #         text=f"Frequency: {frequency:.1f} Hz"
    #     )

    #     self.hv_voltage_label.configure(
    #         text=f"HV Voltage: {hv_voltage:.1f} V"
    #     )

    #     self.hv_current_label.configure(
    #         text=f"HV Current: {hv_current:.2f} A"
    #     )

    #     self.dwell_label.configure(
    #         text=f"Dwell: {dwell_time} s"
    #     )