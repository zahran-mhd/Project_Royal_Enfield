import tkinter as tk

from widgets.load_regulation_table import LoadRegulationTable


class LoadRegulationPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        title = tk.Label(
            self,
            text="OBC Load Regulation",
            font=("Segoe UI", 16, "bold"),
            bg="#EEF2F7",
            fg="#0B1B44"
        )
        title.pack(anchor="w", padx=20, pady=(10, 5))

        can_columns = [
            "HV\nLoad\n(%)",
            "Set HV\nCurrent\n(A)",
            "Input AC\nVoltage\nCAN (V)",
            "Input AC\nCurrent CAN\n(A)",
            "Input\nPower\nCAN\n(W)",
            "Output\nOBC\nVoltage\nCAN (V)",
            "Output\nOBC\nCurrent\nCAN (A)",
            "Output Power\nCAN (W)",
            "Efficiency CAN\n(%)"
        ]

        pa_columns = [
            "HV\nLoad\n(%)",
            "Set HV\nCurrent\n(A)",
            "Input AC\nVoltage\nPower\nAnalyser (V)",
            "Input AC\nCurrent\nPowerAnalyser\n(A)",
            "Input\nPower\nFactor",
            "Input\nPower\nPower\nAnalyser\n(W)",
            "OBC\nOutput\nVoltage\nPower\nAnalyser\n(V)",
            "OBC Output\nCurrent Power\nAnalyser (A)",
            "OBC Output\nPower Analyser\n(W)",
            "Efficiency\nPower\nAnalyser\n(%)"
        ]

        LoadRegulationTable(
            self,
            "OBC Load Regulation - CAN Data",
            can_columns
        ).pack(pady=(5, 40))

        LoadRegulationTable(
            self,
            "OBC Load Regulation - Power Analyser Data",
            pa_columns
        ).pack(pady=(0, 20))