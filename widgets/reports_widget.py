import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class ReportsWidget(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        # ================= FILTER CARD =================
        filter_frame = tk.Frame(
            self,
            bg="white",
            bd=0
        )
        filter_frame.pack(
            fill="x",
            pady=(10, 20)
        )

        for col in range(4):
            filter_frame.grid_columnconfigure(col, weight=1)

        # Heading
        tk.Label(
            filter_frame,
            text="Filter Options",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=25,
            pady=(20, 10)
        )

        ttk.Separator(
            filter_frame,
            orient="horizontal"
        ).grid(
            row=1,
            column=0,
            columnspan=4,
            sticky="ew",
            padx=25,
            pady=(0, 20)
        )

        # Labels
        tk.Label(
            filter_frame,
            text="Report Name",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=2,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 6)
        )

        tk.Label(
            filter_frame,
            text="Report Date",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=2,
            column=1,
            sticky="w",
            padx=15,
            pady=(0, 6)
        )

        tk.Label(
            filter_frame,
            text="Report Type",
            font=("Segoe UI", 10, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=2,
            column=2,
            sticky="w",
            padx=15,
            pady=(0, 6)
        )

        # Inputs
        self.report_name = ttk.Entry(
            filter_frame,
            font=("Segoe UI", 10)
        )
        self.report_name.grid(
            row=3,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 25)
        )

        self.report_date = DateEntry(
            filter_frame,
            date_pattern="dd-mm-yyyy",
            font=("Segoe UI", 10)
        )
        self.report_date.grid(
            row=3,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 25)
        )

        self.report_type = ttk.Combobox(
            filter_frame,
            values=["Daily", "Weekly", "Monthly", "Custom"],
            state="readonly",
            font=("Segoe UI", 10)
        )

        self.report_type.set(
            "Select report type"
        )

        self.report_type.grid(
            row=3,
            column=2,
            sticky="ew",
            padx=15,
            pady=(0, 25)
        )

        # Button
        filter_btn = tk.Button(
            filter_frame,
            text="Filter",
            font=("Segoe UI", 10, "bold"),
            bg="#3567E5",
            fg="white",
            activebackground="#2F5DD0",
            activeforeground="white",
            bd=0,
            cursor="hand2"
        )

        filter_btn.grid(
            row=3,
            column=3,
            sticky="ew",
            padx=(15, 25),
            pady=(0, 25),
            ipady=8
        )

        # ================= REPORT CARD =================
        report_frame = tk.Frame(
            self,
            bg="white",
            bd=0
        )

        report_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            report_frame,
            text="Available Reports",
            font=("Segoe UI", 15, "bold"),
            bg="white",
            fg="#243B64"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        ttk.Separator(
            report_frame,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

        empty_box = tk.Frame(
            report_frame,
            bg="#F7F9FC"
        )

        empty_box.pack(
            fill="x",
            padx=20,
            pady=(0, 20)
        )

        tk.Label(
            empty_box,
            text="No reports found",
            font=("Segoe UI", 11),
            bg="#F7F9FC",
            fg="#334155"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )