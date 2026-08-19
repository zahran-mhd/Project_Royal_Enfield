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

        self.context.efficiency_trend_controller = self.controller
        
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
            1: self.canvas1,
            2: self.canvas2,
            3: self.canvas3,
            4: self.canvas4,
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
                items=efficiency_items,
                value_width=11,
                stop_callback=lambda ch=channel_id:
                    self.context.test_controller.stop_test(ch)
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

    def update_efficiency_summary(self, dut, statistics):

        # Determine channel and DUT index
        if dut in (1, 2):
            channel_id = 1
            dut_index = dut - 1      # DUT1->0, DUT2->1
        else:
            channel_id = 2
            dut_index = dut - 3      # DUT3->0, DUT4->1

        channel_frame = self.channel_map[channel_id]

        charging = statistics["charging"]

        print(dut_index)
        print(charging)
        print("\n========== EFFICIENCY SUMMARY ==========")
        print("DUT:", dut)
        print("Charging statistics:", charging)
        print("Charging MAX:", charging["max"]["value"])
        print("Charging MIN:", charging["min"]["value"])
        print("Charging AVG:", charging["avg"])

        channel_frame.set_value(
            dut_index,
            "charging",
            "max",
            f'{charging["max"]["value"]:.2f}% (C{charging["max"]["cycle"]})'
        )

        channel_frame.set_value(
            dut_index,
            "charging",
            "min",
            f'{charging["min"]["value"]:.2f}% (C{charging["min"]["cycle"]})'
        )

        channel_frame.set_value(
            dut_index,
            "charging",
            "avg",
            f'{charging["avg"]:.2f}%'
        )

        discharging = statistics["discharging"]

        
        print(dut_index)
        print(discharging)
        channel_frame.set_value(
            dut_index,
            "discharging",
            "max",
            f'{discharging["max"]["value"]:.2f}% (C{discharging["max"]["cycle"]})'
        )

        channel_frame.set_value(
            dut_index,
            "discharging",
            "min",
            f'{discharging["min"]["value"]:.2f}% (C{discharging["min"]["cycle"]})'
        )

        channel_frame.set_value(
            dut_index,
            "discharging",
            "avg",
            f'{discharging["avg"]:.2f}%'
        )


    def get_channel_frame(self, channel_id):
        return self.channel_map[channel_id]

    def reset(self, channel_id):

        if channel_id == 1:
            duts = [1, 2]
        else:
            duts = [3, 4]

        self.controller.reset(duts)

    def reset_display(self, selected_duts):

        for dut in selected_duts:

            if isinstance(dut, str):
                dut_no = int(dut.replace("DUT", ""))
            else:
                dut_no = dut

            # Reset graph
            canvas = self.canvas_map[dut_no]

            canvas.charging_points.clear()
            canvas.discharging_points.clear()
            canvas.draw_graph()

            # Reset summary
            if dut in (1, 2):
                channel_id = 1
                dut_index = dut - 1
            else:
                channel_id = 2
                dut_index = dut - 3

            channel_frame = self.channel_map[channel_id]

            for mode in ("charging", "discharging"):

                channel_frame.set_value(
                    dut_index,
                    mode,
                    "max",
                    "-- %"
                )

                channel_frame.set_value(
                    dut_index,
                    mode,
                    "min",
                    "-- %"
                )

                channel_frame.set_value(
                    dut_index,
                    mode,
                    "avg",
                    "-- %"
                )

    # def reset_display(self, selected_duts):

    #     # Reset controller data
    #     self.controller.reset(selected_duts)

    #     # Reset graphs
    #     for dut in selected_duts:

    #         self.canvas_map[f"DUT{dut}"].reset()

    #     # Reset statistics panel
    #     for dut in selected_duts:

    #         if dut in (1, 2):
    #             channel_id = 1
    #             dut_index = dut - 1
    #         else:
    #             channel_id = 2
    #             dut_index = dut - 3

    #         frame = self.channel_map[channel_id]

    #         for mode in ("charging", "discharging"):
    #             frame.set_value(dut_index, mode, "max", "-- %")
    #             frame.set_value(dut_index, mode, "min", "-- %")
    #             frame.set_value(dut_index, mode, "avg", "-- %")