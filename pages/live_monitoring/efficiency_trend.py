import tkinter as tk

from widgets.efficiencyTrend_canvas import EfficiencyTrendCanvas
from widgets.channel_frame import ChannelFrame


class EfficiencyTrendFrame(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(parent, bg="white")

        self.context = context
        
        self.running_duts = []

        # =====================================
        # Configure Main Layout
        # =====================================
        self.grid_rowconfigure(0, weight=1)   # Graph area
        self.grid_rowconfigure(1, weight=0)   # Channel cards
        self.grid_columnconfigure(0, weight=1)
                
                # =====================================
        # Top Frame (Graphs)
        # =====================================
        self.plot_frame = tk.Frame(self, bg="white")
        self.plot_frame.grid(row=0, column=0, sticky="nsew")

        self.plot_frame.grid_columnconfigure(0, weight=1)
        self.plot_frame.grid_columnconfigure(1, weight=1)

        self.plot_frame.grid_rowconfigure(0, weight=1)
        self.plot_frame.grid_rowconfigure(1, weight=1)

        # Create canvases
        self.canvas1 = EfficiencyTrendCanvas(
    self.plot_frame,
   "DUT1", "Channel 1",
   
)
        self.canvas1.grid(row=0, column=0, sticky="nsew", padx=(15, 8), pady=(15, 8))

        self.canvas2 = EfficiencyTrendCanvas(self.plot_frame,"DUT2", "Channel 1",)
        self.canvas2.grid(row=1, column=0, sticky="nsew", padx=(15, 8), pady=(8, 15))

        self.canvas3 = EfficiencyTrendCanvas(self.plot_frame,"DUT3", "Channel 2",)
        self.canvas3.grid(row=0, column=1, sticky="nsew", padx=(8, 15), pady=(15, 8))

        self.canvas4 = EfficiencyTrendCanvas(self.plot_frame,"DUT4","Channel 2",)
        self.canvas4.grid(row=1, column=1, sticky="nsew", padx=(8, 15), pady=(8, 15))

        # Now create the map
        self.canvas_map = {
            "DUT1": self.canvas1,
            "DUT2": self.canvas2,
            "DUT3": self.canvas3,
            "DUT4": self.canvas4,
        }

        
                # =====================================
        # Bottom Frame (Channel Cards)
        # =====================================
        self.bottom_frame = tk.Frame(self, bg="white")
        self.bottom_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))

        # Configure columns dynamically
        channels = self.context.channel_repository.get_all_channels()

        for i in range(len(channels)):
            self.bottom_frame.grid_columnconfigure(i, weight=1)

        efficiency_items = [
            ("max", "Max Efficiency", "-- %"),
            ("min", "Min Efficiency", "-- %"),
            ("avg", "Avg Efficiency", "-- %"),
        ]

        self.channel_frames = []
        self.channel_map = {}

        for index, channel in enumerate(channels):

            channel_id = int(channel["ChannelID"])
            channel_name = channel["ChannelName"]

            channel_frame = ChannelFrame(
                self.bottom_frame,
                channel_name=channel_name,
                dut_names=[
                    f"DUT{2 * channel_id - 1}",
                    f"DUT{2 * channel_id}"
                ],
                items=efficiency_items
            )

            channel_frame.grid(
                row=0,
                column=index,
                padx=10,
                pady=5,
                sticky="nsew"
            )

            self.channel_frames.append(channel_frame)
            self.channel_map[channel["ChannelID"]] = channel_frame
            
    def start_live_plot(self, selected_duts):
        
        
         # Add newly started DUTs
        for dut in selected_duts:
            if dut not in self.running_duts:
                self.running_duts.append(dut)

        selected_duts = self.running_duts

        # Hide all canvases first
        for canvas in self.canvas_map.values():
            canvas.grid_forget()

        count = len(selected_duts)

        if count == 0:
            return

        # Reset grid configuration
        for r in range(2):
            self.plot_frame.grid_rowconfigure(r, weight=1)

        for c in range(2):
            self.plot_frame.grid_columnconfigure(c, weight=1)

        # =========================
        # COLUMN-WISE DUT MAPPING
        # =========================
        if count == 1:
            positions = [(0, 0)]

            self.plot_frame.grid_columnconfigure(0, weight=1)
            self.plot_frame.grid_columnconfigure(1, weight=0)

        elif count == 2:
            # DUT1 top-left, DUT2 bottom-left (same column)
            positions = [
                (0, 0),  # DUT 1
                (1, 0)   # DUT 2
            ]

            self.plot_frame.grid_columnconfigure(0, weight=1)
            self.plot_frame.grid_columnconfigure(1, weight=0)

        elif count == 3:
            # DUT1 & DUT2 left column, DUT3 right top
            positions = [
                (0, 0),  # DUT 1
                (1, 0),  # DUT 2
                (0, 1)   # DUT 3
            ]

            self.plot_frame.grid_columnconfigure(0, weight=1)
            self.plot_frame.grid_columnconfigure(1, weight=1)

        else:
            # DUT1-2 left column, DUT3-4 right column
            positions = [
                (0, 0),  # DUT 1
                (1, 0),  # DUT 2
                (0, 1),  # DUT 3
                (1, 1)   # DUT 4
            ]

            self.plot_frame.grid_columnconfigure(0, weight=1)
            self.plot_frame.grid_columnconfigure(1, weight=1)

        # =========================
        # PLACE CANVASES
        # =========================
        for idx, (dut, (row, col)) in enumerate(zip(selected_duts, positions), start=1):

            canvas = self.canvas_map[dut]

            canvas.grid(
                row=row,
                column=col,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # =========================
            # CHANNEL LABEL
            # =========================
            canvas.delete("title")

            canvas.create_text(
                10, 10,
                text=f"Channel {idx}",
                anchor="nw",
                font=("Segoe UI", 12, "bold"),
                fill="black",
                tags="title"
            )


            # test data
            canvas.add_charging_points(88.2)
            canvas.add_charging_points(89.5)
            canvas.add_charging_points(90.8)

            canvas.add_discharging_points(91.3)
            canvas.add_discharging_points(89.7)
            canvas.add_discharging_points(87.5)