import tkinter as tk
from tkinter import ttk, filedialog

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure


class HistoricalTrendWidget(tk.Frame):

    def __init__(self, parent, app):
        super().__init__(parent, bg="#E9EDF2")

        self.app = app
        self.controller = app.historical_trend_controller

        self.folder_path = tk.StringVar(value="No file selected")

        # Folder Section
        top_frame = tk.Frame(self, bg="#E9EDF2")
        top_frame.pack(fill="x")

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
            pady=20
        )

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

        self.from_entry = ttk.Entry(filter_frame, width=35)
        self.from_entry.grid(
            row=1,
            column=0,
            padx=(20, 10),
            pady=(0, 15),
            sticky="ew"
        )

        self.to_entry = ttk.Entry(filter_frame, width=35)
        self.to_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=(0, 15),
            sticky="ew"
        )

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
            expand=True
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
            start_cycle = int(self.from_entry.get())
            end_cycle = int(self.to_entry.get())

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

    def draw_graph(
        self,
        x_values,
        y_values,
        parameter
    ):

        for widget in self.graph_container.winfo_children():
            widget.destroy()

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

        canvas = FigureCanvasTkAgg(
            fig,
            master=self.graph_container
        )

        canvas.draw()

        canvas.get_tk_widget().pack(
            fill="both",
            expand=True
        )