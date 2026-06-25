import tkinter as tk
from tkinter import ttk, filedialog

import os
import pandas as pd

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.ticker import MaxNLocator
from controllers.historical_trend_controller import (
    HistoricalTrendController
)

class HistoricalTrendPage(tk.Frame):

    def __init__(self, parent,app):
        super().__init__(parent, bg="#E9EDF2")

        self.app = app

        self.controller = (app.historical_trend_controller)

        self.folder_path = tk.StringVar(value="No file selected")

        self.current_figure = None

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
        ).grid(row=0, column=2, padx=(5, 20), pady=(15, 5), sticky="w")
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


        self.upload_btn = tk.Button(
            filter_frame,
            text="Upload CSV",
            font=("Segoe UI", 10, "bold"),
            bg="#4F5AE8",
            fg="white",
            bd=0,
            command=self.load_csv_columns
        )

        self.upload_btn.grid(
            row=1,
            column=2,
            padx=10,
            pady=(0, 15)
        )


        # Dropdown
        self.parameter = ttk.Combobox(
            filter_frame,
            state="readonly",
            width=35
        )

        self.parameter.grid(
            row=1,
            column=3,
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
            height=2,
            command=self.plot_graph
        )

        plot_btn.grid(
            row=1,
            column=4,
            padx=10,
            pady=(0, 15)
        )

        export_btn = tk.Button(
            filter_frame,
            text="Export Graph",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            bd=0,
            command=self.export_graph
        )

        export_btn.grid(
            row=1,
            column=5,
            padx=(10, 20),
            pady=(0, 15)
        )

        filter_frame.grid_columnconfigure(0, weight=1)
        filter_frame.grid_columnconfigure(1, weight=1)
        filter_frame.grid_columnconfigure(2, weight=1)
        filter_frame.grid_columnconfigure(3, weight=2)

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

        self.graph_container = tk.Frame(
            graph_frame,
            bg="white"
        )

        self.graph_container.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=(0, 10)
        )

    def select_folder(self):
        folder = filedialog.askdirectory()

        if folder:
            self.folder_path.set(folder)

    def plot_graph(self):

        folder = self.folder_path.get()

        try:

            start_cycle = int(
                self.from_entry.get()
            )

            end_cycle = int(
                self.to_entry.get()
            )

        except ValueError:

            return

        parameter = self.parameter.get()

        x_values, y_values = (
            self.controller.get_graph_data(
                folder,
                start_cycle,
                end_cycle,
                parameter
            )
        )

        self.draw_graph(
            x_values,
            y_values,
            parameter
        )

    def draw_graph(self, x_values, y_values, parameter):

        for widget in self.graph_container.winfo_children():
            widget.destroy()

        from matplotlib.figure import Figure
        from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
        
        fig = Figure(
            figsize=(8, 4),
            dpi=100
        )

        ax = fig.add_subplot(111)

        ax.plot(
            x_values,
            y_values,
            marker="o"
        )

        ax.set_xticks(x_values)

        ax.set_title(
            f"{parameter} vs Cycle Number"
        )

        ax.set_xlabel("Cycle Number")

        ax.set_ylabel(parameter)

        ax.grid(True)

        self.current_figure = fig

        # Display graph
        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_container
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )


    # def load_csv_columns(self):

    #     folder = self.folder_path.get()

    #     try:

    #         start_cycle = int(
    #             self.from_entry.get()
    #         )

    #     except ValueError:

    #         return

    #     file_path = os.path.join(
    #         folder,
    #         f"Cycle_{start_cycle}.csv"
    #     )

    #     if not os.path.exists(file_path):

    #         return

    #     try:

    #         df = pd.read_csv(file_path)

    #         columns = list(df.columns)

    #         self.parameter["values"] = columns

    #         if columns:

    #             self.parameter.set(
    #                 columns[0]
    #             )

    #     except Exception as ex:

    #         print(ex)

    def export_graph(self):

        if self.current_figure is None:

            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[
                ("PNG Image", "*.png"),
                ("JPEG Image", "*.jpg"),
                ("PDF File", "*.pdf")
            ]
        )

        if not file_path:

            return

        self.current_figure.savefig(
            file_path,
            dpi=300,
            bbox_inches="tight"
        )

    def load_csv_columns(self):

        folder = self.folder_path.get()

        try:
            start_cycle = int(
                self.from_entry.get()
            )

        except ValueError:
            return

        columns = self.controller.get_columns(
            folder,
            start_cycle
        )

        self.parameter["values"] = columns

        if columns:
            self.parameter.set(columns[0])
    
   