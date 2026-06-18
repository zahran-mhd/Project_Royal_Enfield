import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry


class ReportsPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        # Title
        title = tk.Label(
            self,
            text="Reports",
            font=("Segoe UI", 20, "bold"),
            bg="#EEF2F7",
            fg="#0B1B44"
        )
        title.pack(anchor="w", padx=25, pady=(20, 10))

        # ---------------- FILTER FRAME ----------------
        filter_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )
        filter_frame.pack(fill="x", padx=25, pady=20)

        filter_frame.grid_columnconfigure(0, weight=1)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(2, weight=1)

        # Filter Heading
        tk.Label(
            filter_frame,
            text="Filter Options",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).grid(
            row=0,
            column=0,
            columnspan=4,
            sticky="w",
            padx=15,
            pady=(15, 15)
        )

        # ---------------- Report Name ----------------
        tk.Label(
            filter_frame,
            text="Report Name",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=1,
            column=0,
            padx=(15, 20),
            pady=(5, 5),
            sticky="w"
        )

        self.report_name = ttk.Entry(
            filter_frame,
            width=28
        )
        self.report_name.grid(
            row=2,
            column=0,
            padx=(15, 20),
            pady=(0, 15),
            sticky="w"
        )

        # ---------------- Report Date ----------------
        tk.Label(
            filter_frame,
            text="Report Date",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=1,
            column=1,
            padx=(15, 20),
            pady=(5, 5),
            sticky="w"
        )

        self.report_date = DateEntry(
            filter_frame,
            width=25,
            date_pattern="dd-mm-yyyy"
        )
        self.report_date.grid(
            row=2,
            column=1,
            padx=(15, 20),
            pady=(0, 15),
            sticky="w"
        )

        # ---------------- Report Type ----------------
        tk.Label(
            filter_frame,
            text="Report Type",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(
            row=1,
            column=2,
            padx=(15, 20),
            pady=(5, 5),
            sticky="w"
        )

        self.report_type = ttk.Combobox(
            filter_frame,
            values=["Daily", "Weekly", "Monthly", "Custom"],
            width=25
        )
        self.report_type.set("Select report type")
        self.report_type.grid(
            row=2,
            column=2,
            padx=(15, 20),
            pady=(0, 15),
            sticky="w"
        )

        # ---------------- Filter Button ----------------
        tk.Button(
            filter_frame,
            text="Filter",
            font=("Segoe UI", 10, "bold"),
            bg="#4F5AE8",
            fg="white",
            activebackground="#4F5AE8",
            activeforeground="white",
            bd=0,
            width=12,
            height=2
        ).grid(
            row=2,
            column=3,
            padx=(10, 20),
            pady=(0, 15)
        )

        # ---------------- REPORT FRAME ----------------
        report_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )
        report_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        tk.Label(
            report_frame,
            text="Available Reports",
            font=("Segoe UI", 14, "bold"),
            bg="white"
        ).pack(
            anchor="w",
            padx=15,
            pady=15
        )