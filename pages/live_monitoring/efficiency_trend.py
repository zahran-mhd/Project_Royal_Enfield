import tkinter as tk

from widgets.efficiencyTrend_canvas import EfficiencyTrendCanvas
from widgets.channel_frame import ChannelFrame

from controllers.efficiency_trend_controller import (
    EfficiencyTrendController
)


class EfficiencyTrendFrame(tk.Frame):

    def __init__(self, parent, context):

        super().__init__(
            parent,
            bg="white"
        )

        self.context = context

        # Create Controller
        self.controller = EfficiencyTrendController(
            self,
            self.context
        )
        
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=0)
        self.rowconfigure(0,weight=1)

        self.create_ui()

    def create_ui(self):

        self.create_plot_area()

        self.create_channel_area()

    # =====================================
    # GRAPH AREA
    # =====================================

    def create_plot_area(self):

        self.plot_frame = tk.Frame(
            self,
            bg="white"
        )

        self.plot_frame.grid(
            row=0,
            column=0,
            sticky="nsew"
        )

        self.plot_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.plot_frame.grid_columnconfigure(
            1,
            weight=1
        )

        self.plot_frame.grid_rowconfigure(
            0,
            weight=1
        )

        self.plot_frame.grid_rowconfigure(
            1,
            weight=1
        )

        # Create canvases
        self.canvas1 = EfficiencyTrendCanvas(
            self.plot_frame,
            "DUT1",
            "Channel 1"
        )

        self.canvas1.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(15, 8),
            pady=(15, 8)
        )

        self.canvas2 = EfficiencyTrendCanvas(
            self.plot_frame,
            "DUT2",
            "Channel 1"
        )

        self.canvas2.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=(15, 8),
            pady=(8, 15)
        )

        self.canvas3 = EfficiencyTrendCanvas(
            self.plot_frame,
            "DUT3",
            "Channel 2"
        )

        self.canvas3.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(15, 8)
        )

        self.canvas4 = EfficiencyTrendCanvas(
            self.plot_frame,
            "DUT4",
            "Channel 2"
        )

        self.canvas4.grid(
            row=1,
            column=1,
            sticky="nsew",
            padx=(8, 15),
            pady=(8, 15)
        )

        # Canvas map
        self.canvas_map = {

            "DUT1": self.canvas1,
            "DUT2": self.canvas2,
            "DUT3": self.canvas3,
            "DUT4": self.canvas4
        }

    # =====================================
    # CHANNEL AREA
    # =====================================

    def create_channel_area(self):

        self.bottom_frame = tk.Frame(
            self,
            bg="white"
        )

        self.bottom_frame.grid(
    row=1,
    column=0,
    sticky="nsew",
    padx=8,
    pady=8
)

        channels = (
            self.context
            .channel_repository
            .get_all_channels()
        )
        self.grid_columnconfigure(0, weight=1)

        for index in range(len(channels)):
            self.bottom_frame.grid_columnconfigure(
                index,
                weight=1
            )

        efficiency_items = [

            (
                "max",
                "Max Efficiency",
                "-- %"
            ),

            (
                "min",
                "Min Efficiency",
                "-- %"
            ),

            (
                "avg",
                "Avg Efficiency",
                "-- %"
            )
        ]

        self.channel_frames = []

        self.channel_map = {}

        for index, channel in enumerate(channels):

            channel_id = int(
                channel["ChannelID"]
            )

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
            padx=4,
            pady=1,
            sticky="nsew"
        )

            self.channel_frames.append(
                channel_frame
            )

            self.channel_map[
                channel["ChannelID"]
            ] = channel_frame

    # =====================================
    # PUBLIC METHOD
    # =====================================

    def start_live_plot(self, selected_duts):

        self.controller.start_live_plot(
            selected_duts
        )