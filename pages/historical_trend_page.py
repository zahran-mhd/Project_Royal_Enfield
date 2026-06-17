import tkinter as tk
from tkinter import ttk, filedialog


class HistoricalTrendPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#E9EDF2")

        self.folder_path = tk.StringVar(value="No file selected")

        # Title
        title = tk.Label(
            self,
            text="Historical Trend",
            font=("Segoe UI", 20, "bold"),
            bg="#E9EDF2",
            fg="#0B1B44"
        )
        title.pack(anchor="w", padx=25, pady=(20, 10))

        #  Folder Section
        top_frame = tk.Frame(self, bg="#E9EDF2")
        top_frame.pack(fill="x", padx=25)

        select_btn = tk.Button(
            top_frame,
            text="Select Folder",
            font=("Segoe UI", 10, "bold"),
            bg="#4F5AE8",
            fg="white",
            activebackground="#4F5AE8",
            activeforeground="white",
            bd=0,
            width=12,
            height=2,
            command=self.select_folder
        )
        select_btn.pack(side="left")

        tk.Label(
            top_frame,
            textvariable=self.folder_path,
            bg="#E9EDF2",
            fg="#222222",
            font=("Segoe UI", 11)
        ).pack(side="left", padx=12)

        # Filter Card
        filter_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )
        filter_frame.pack(
            fill="x",
            padx=25,
            pady=20
        )

        # Row 1 Labels
        tk.Label(
            filter_frame,
            text="Cycle Number",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        tk.Label(
            filter_frame,
            text="Y-Axis Parameter",
            bg="white",
            font=("Segoe UI", 10, "bold")
        ).grid(row=0, column=2, padx=20, pady=(15, 5), sticky="w")

        # From Entry
        self.from_entry = ttk.Entry(
            filter_frame,
            width=35
        )
        self.from_entry.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15),
            sticky="ew"
        )

        # To Entry
        self.to_entry = ttk.Entry(
            filter_frame,
            width=35
        )
        self.to_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 15),
            sticky="ew"
        )

        # Dropdown
        self.parameter = ttk.Combobox(
            filter_frame,
            values=[
                "Voltage",
                "Current",
                "Power",
                "Efficiency"
            ],
            width=40
        )

        self.parameter.set("Efficiency")

        self.parameter.grid(
            row=1,
            column=2,
            padx=10,
            pady=(0, 15),
            sticky="ew"
        )

        # Plot Button
        plot_btn = tk.Button(
            filter_frame,
            text="Plot Graph",
            font=("Segoe UI", 10, "bold"),
            bg="#4F5AE8",
            fg="white",
            activebackground="#4F5AE8",
            activeforeground="white",
            bd=0,
            width=12,
            height=2
        )

        plot_btn.grid(
            row=1,
            column=3,
            padx=(10, 20),
            pady=(0, 15)
        )

        filter_frame.grid_columnconfigure(0, weight=1)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(2, weight=2)

        # Graph Preview 
        graph_frame = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )

        graph_frame.pack(
            fill="both",
            expand=True,
            padx=25,
            pady=(0, 20)
        )

        tk.Label(
            graph_frame,
            text="Graph Preview",
            bg="white",
            font=("Segoe UI", 11)
        ).pack(anchor="nw", padx=15, pady=15)

        self.canvas = tk.Canvas(
            graph_frame,
            bg="white",
            highlightthickness=0
        )

        self.canvas.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.folder_path.set(folder)