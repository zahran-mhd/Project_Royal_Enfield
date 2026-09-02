import tkinter as tk
from widgets.channel_frame import ChannelFrame
from widgets.table_widgets import TableWidget
from controllers.live_table_controller import LiveTableController
import time


PORT_TO_DUT = {
    "PCAN_USBBUS1": 1,
    "PCAN_USBBUS2": 2,
    "PCAN_USBBUS3": 3,
    "PCAN_USBBUS4": 4,
}


CAN_PARAMETER_MAP = {

    "Chrgr_Input_AC_Vlt": "OBC Input Voltage",

    "Chrgr_Input_AC_Curr": "OBC Input Current",

    "Chrgr_Output_DC_Vlt": "OBC Output Voltage",

    "Chrgr_Output_DC_Curr": "OBC Output Current",

    "HP_DCDC_Input_DC_Vlt": "HPDCDC Input Voltage",

    "HP_DCDC_Input_DC_Curr": "HPDCDC Input Current",

    "HP_DCDC_Output_DC_Vlt": "HPDCDC Output Voltage",

    "HP_DCDC_Output_DC_Curr": "HPDCDC Output Current",

    "OBC_temp": "OBC_TEMP",

    "OBC_FET_Temp": "OBC_FET_TEMP",

    "HPDCDC_Temp": "HPDCDC_TEMP"
}

PW3337_PARAMETER_MAP = {
    "U1": "OBC Input Voltage",
    "I1": "OBC Input Current",
    "P1": "OBC_Input_Power",

    # Add these if your table has rows for them
    "U2": "OBC Output Voltage",
    "I2": "OBC Output Current",
    "P2": "OBC_Output_Power",

    "U3": "HPDCDC Input Voltage",
    "I3": "HPDCDC Input Current",
    "P3": "HPDCDC_Input_Power",


}

HARDWARE_PARAMETER_MAP = {

    "Voltage": "OBC Output Voltage",
    "Current": "OBC Output Current",

    "U1": "OBC Input Voltage",
    "I1": "OBC Input Current",
    "P1": "OBC_Input_Power",

    "U2": "OBC Output Voltage",
    "I2": "OBC Output Current",
    "P2": "OBC_Output_Power",

    
    "U3": "HPDCDC Input Voltage",
    "I3": "HPDCDC Input Current",
    "P3": "HPDCDC_Input_Power",
}


TEMP_NAME = {
    "OBC_TEMP": "OBC",
    "OBC_FET_TEMP": "FET",
    "HPDCDC_TEMP": "HPDC"
}

class LiveTableFrame(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="white")
        self.context = context
        self.row_map = {}
        self.channel_timers = {}
        # Create Controller
        self.controller = LiveTableController(
            self,
            self.context
        )
        self.context.live_table_controller = self.controller
        self.context.live_table_frame = self
        # self.channel_id=None
        # Create card first
        self.card = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )
        self.card.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # Now create table
        self.create_table()

        # self.after(200, self.refresh_table)

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        channels = self.context.channel_repository.get_all_channels()

        self.channel_frames = []
        self.channel_map = {}

        self.can_live_values = {}
        self.hardware_live_values = {}

        for dut in range(1, 5):
            self.hardware_live_values[dut] = {}

        for dut in range(1, 5):
            self.can_live_values[dut] = {}

        for index, channel in enumerate(channels):

            
            channel_id = channel["ChannelID"]
            channel_name = channel["ChannelName"]
            dut_names = [
                f"DUT{2 * channel_id - 1}",
                f"DUT{2 * channel_id}"
            ]


            channel_frame = ChannelFrame(
                self,
                channel_name=channel_name,
                dut_names=dut_names,
                stop_callback=lambda ch=channel_id:
                    self.context.test_controller.stop_test(ch)
            )

            channel_frame.grid(
                row=1,
                column=index,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            self.channel_frames.append(channel_frame)
            self.channel_map[channel["ChannelID"]] = channel_frame
            # ======================================================
            # RESTORE RUNNING TEST STATE
            # ======================================================

            # Restore current test progress if a test is already running
            # self.after(
            #     100,
            #     self.restore_test_progress
            # )
            self.after(
                100,
                self.update_test_timer
            )
            # self.restore_channel_progress()
            
            
    def create_table(self):

        columns = (
    
            "Parameter",
            "DUT1 Hardware Data",
            "DUT1 CAN Data",
             "DUT2 Hardware Data",
            "DUT2 CAN Data",
             "DUT3 Hardware Data",
            "DUT3 CAN Data",
             "DUT4 Hardware Data",
            "DUT4 CAN Data",
            
        )

        self.table = TableWidget(
            self.card,
            columns,
            height=17,
            style_name="LiveTable.Treeview",
            
        )
        
        parameters = [
            "OBC Input Voltage",
            "OBC Input Current",
            "OBC Output Voltage",
            "OBC Output Current",
            "OBC_Input_Power",
            "OBC_Output_Power",
            "OBC Efficiency",
            "HPDCDC Input Voltage",
            "HPDCDC Input Current",
            "HPDCDC Output Voltage",
            "HPDCDC Output Current",
            "HPDCDC_Input_Power",
            "HPDCDC_Output_Power",
            "HPDCDC_Efficiency",
            "OBC_TEMP",
            "OBC_FET_TEMP",
            "HPDCDC_TEMP"
        ]

        for parameter in parameters:
            row = [
                parameter,      # 1st column: Parameter
                "",         # 2nd column: DUT1 Hardware Data
                "",             # 3rd column: DUT1 CAN Data
                "",             # 4th column: DUT2 Hardware Data
                "",             # 5th column: DUT2 CAN Data
                "",             # 6th column: DUT3 Hardware Data
                "",             # 7th column: DUT3 CAN Data
                "",             # 8th column: DUT4 Hardware Data
                ""              # 9th column: DUT4 CAN Data
            ]
            item = self.table.insert(row)

            self.row_map[parameter] = item

        self.table.pack(fill="both", expand=True, padx=20, pady=10)


    def update_can_value(self, parameter, dut_no, value):

        if parameter not in self.row_map:
            return

         # Store latest value
        try:
            self.can_live_values[dut_no][parameter] = float(value)
        except:
            self.can_live_values[dut_no][parameter] = 0.0

        item = self.row_map[parameter]

        values = list(self.table.tree.item(item)["values"])

        # CAN columns
        can_columns = {
            1: 2,
            2: 4,
            3: 6,
            4: 8
        }

        values[can_columns[dut_no]] = value

        self.table.tree.item(item, values=values)

        # Calculate powers and efficiencies
        self.calculate_can_values(dut_no)

        if parameter in (
            "OBC_TEMP",
            "OBC_FET_TEMP",
            "HPDCDC_TEMP"
        ):

            mode = self.get_dut_mode(dut_no)

            if mode is not None:
                self.controller.update_temperature(
                    dut_no,
                    mode,
                    parameter,
                    float(value)
                )
        # if parameter in (
        #     "OBC_TEMP",
        #     "OBC_FET_TEMP",
        #     "HPDCDC_TEMP"
        # ):

        #     mode = self.context.test_session.mode.lower()

        #     if mode == "charge":
        #         mode = "charging"
        #     elif mode == "discharge":
        #         mode = "discharging"
        #     else:
        #         return

        #     self.controller.update_temperature(
        #         dut_no,
        #         mode,
        #         parameter,
        #         value
        #     )
        # if dut_no in (1,2):
        #     self.channel_id=1
        # elif dut_no in(3,4):
        #     self.channel_id=2

    # def calculate_can_values(self, dut_no):

    #     d = self.can_live_values[dut_no]

    #     vin = d.get("OBC Input Voltage", 0)
    #     iin = d.get("OBC Input Current", 0)

    #     vout = d.get("OBC Output Voltage", 0)
    #     iout = d.get("OBC Output Current", 0)

    #     hp_in_v = d.get("HPDCDC Input Voltage", 0)
    #     hp_in_i = d.get("HPDCDC Input Current", 0)

    #     hp_out_v = d.get("HPDCDC Output Voltage", 0)
    #     hp_out_i = d.get("HPDCDC Output Current", 0)

    #     obc_input_power = vin * iin * 0.99
    #     obc_output_power = vout * iout

    #     if obc_input_power > 0:
    #         obc_eff = (obc_output_power / obc_input_power) * 100
    #     else:
    #         obc_eff = 0

    #     hp_input_power = hp_in_v * hp_in_i
    #     hp_output_power = hp_out_v * hp_out_i

    #     # print(hp_input_power)
    #     if hp_input_power > 0:
    #         hp_eff = (hp_output_power / hp_input_power) * 100
    #     else:
    #         hp_eff = 0

    #     self.set_can_row("OBC_Input_Power", dut_no, obc_input_power)
    #     self.set_can_row("OBC_Output_Power", dut_no, obc_output_power)
    #     self.set_can_row("OBC Efficiency", dut_no, obc_eff)


    #     if obc_eff > 0:
    #         self.context.efficiency_trend_controller.add_efficiency_sample(
    #             dut=dut_no,
    #             mode="charging",
    #             efficiency=obc_eff
    #         )

    #     self.set_can_row("HPDCDC_Input_Power", dut_no, hp_input_power)
    #     self.set_can_row("HPDCDC_Output_Power", dut_no, hp_output_power)
    #     self.set_can_row("HPDCDC_Efficiency", dut_no, hp_eff)

    #     if hp_eff > 0:
    #         self.context.efficiency_trend_controller.add_efficiency_sample(
    #         dut=dut_no,
    #         mode="discharging",
    #         efficiency=hp_eff
    #     )

    def calculate_can_values(self, dut_no):

        d = self.can_live_values[dut_no]

        vin = d.get("OBC Input Voltage", 0)
        iin = d.get("OBC Input Current", 0)

        vout = d.get("OBC Output Voltage", 0)
        iout = d.get("OBC Output Current", 0)

        hp_in_v = d.get("HPDCDC Input Voltage", 0)
        hp_in_i = d.get("HPDCDC Input Current", 0)

        hp_out_v = d.get("HPDCDC Output Voltage", 0)
        hp_out_i = d.get("HPDCDC Output Current", 0)

        # -----------------------------
        # OBC
        # -----------------------------

        obc_input_power = vin * iin * 0.99
        obc_output_power = vout * iout

        if obc_input_power > 0:
            obc_eff = (
                obc_output_power /
                obc_input_power
            ) * 100
        else:
            obc_eff = 0

        # -----------------------------
        # HPDCDC
        # -----------------------------

        hp_input_power = hp_in_v * hp_in_i
        hp_output_power = hp_out_v * hp_out_i

        if hp_input_power > 0:
            hp_eff = (
                hp_output_power /
                hp_input_power
            ) * 100
        else:
            hp_eff = 0

        # -----------------------------
        # Update live table
        # -----------------------------

        self.set_can_row(
            "OBC_Input_Power",
            dut_no,
            obc_input_power
        )

        self.set_can_row(
            "OBC_Output_Power",
            dut_no,
            obc_output_power
        )

        self.set_can_row(
            "OBC Efficiency",
            dut_no,
            obc_eff
        )

        self.set_can_row(
            "HPDCDC_Input_Power",
            dut_no,
            hp_input_power
        )

        self.set_can_row(
            "HPDCDC_Output_Power",
            dut_no,
            hp_output_power
        )

        self.set_can_row(
            "HPDCDC_Efficiency",
            dut_no,
            hp_eff
        )

        # ==================================================
        # IMPORTANT
        # Only collect the efficiency belonging to the
        # current DUT's actual operating mode.
        # ==================================================

        mode = self.get_dut_mode(dut_no)

        # print(
        #     f"[EFF] DUT={dut_no} "
        #     f"MODE={mode} "
        #     f"OBC={obc_eff:.2f} "
        #     f"HPDCDC={hp_eff:.2f}"
        # )

        if mode == "charging":

            # DUT is charging -> OBC efficiency matters
            if obc_eff > 0:

                self.context.efficiency_trend_controller.add_efficiency_sample(
                    dut=dut_no,
                    mode="charging",
                    efficiency=obc_eff
                )

        elif mode == "discharging":

            # DUT is discharging -> HPDCDC efficiency matters
            if hp_eff > 0:

                self.context.efficiency_trend_controller.add_efficiency_sample(
                    dut=dut_no,
                    mode="discharging",
                    efficiency=hp_eff
                )

    # Rest -> collect NOTHING

    def set_can_row(self, parameter, dut_no, value):

        if parameter not in self.row_map:
            return

        # Store latest calculated value
        self.can_live_values[dut_no][parameter] = value

        item = self.row_map[parameter]

        values = list(self.table.tree.item(item)["values"])

        hardware_columns = {
            1: 2,
            2: 4,
            3: 6,
            4: 8
        }

        values[hardware_columns[dut_no]] = f"{value:.2f}"

        self.table.tree.item(item, values=values)


    def update_hardware_value(self, parameter, dut_no, value):

        if parameter not in self.row_map:
            return

        try:
            self.hardware_live_values[dut_no][parameter] = float(value)
        except:
            self.hardware_live_values[dut_no][parameter] = 0.0

        item = self.row_map[parameter]

        values = list(self.table.tree.item(item)["values"])

        hardware_columns = {
            1: 1,
            2: 3,
            3: 5,
            4: 7
        }

        values[hardware_columns[dut_no]] = f"{float(value):.2f}"

        self.table.tree.item(item, values=values)

    # def update_hardware_value(self, parameter, dut_no, value):

    #     if parameter not in self.row_map:
    #         return

    #     item = self.row_map[parameter]

    #     values = list(self.table.tree.item(item)["values"])

    #     hardware_columns = {
    #         1: 1,
    #         2: 3,
    #         3: 5,
    #         4: 7
    #     }

    #     values[hardware_columns[dut_no]] = value

    #     self.table.tree.item(item, values=values)

    # def refresh_channel(self, channel_id):

    #     if channel_id == 1:
    #         duts = (1, 2)

    #     elif channel_id == 2:
    #         duts = (3, 4)

    #     for group, ports in self.context.can_values.items():

    #         for port, signals in ports.items():

    #             dut_no = PORT_TO_DUT.get(port)

    #             if dut_no not in duts:
    #                 continue

    #             for signal, value in signals.items():

    #                 table_name = CAN_PARAMETER_MAP.get(signal)

    #                 if table_name:

    #                     self.update_can_value(
    #                         table_name,
    #                         dut_no,
    #                         f"{value:.2f}"
    #                     )

    def refresh_channel(self, channel_id):

        settings = self.context.test_repository.get_channel_settings(channel_id)

        active_duts = []

        if channel_id == 1:

            if settings["use_dut_a"]:
                active_duts.append(1)

            if settings["use_dut_b"]:
                active_duts.append(2)

        elif channel_id == 2:

            if settings["use_dut_a"]:
                active_duts.append(3)

            if settings["use_dut_b"]:
                active_duts.append(4)

        for group, ports in self.context.can_values.items():

            for port, signals in ports.items():

                dut_no = PORT_TO_DUT.get(port)

                if dut_no not in active_duts:
                    continue

                for signal, value in signals.items():

                    table_name = CAN_PARAMETER_MAP.get(signal)

                    if table_name:

                        self.update_can_value(
                            table_name,
                            dut_no,
                            f"{value:.2f}"
                        )

        # print("Hardware:", self.context.hardware_values)

        for dut_no in active_duts:

            hardware = self.context.hardware_values.get(dut_no, {})

            for signal, value in hardware.items():

                # print(signal)

                table_name = PW3337_PARAMETER_MAP.get(signal)

                # print(table_name)
                if table_name:

                    self.update_hardware_value(
                        table_name,
                        dut_no,
                        f"{value:.2f}"
                    )

    def clear_dut(self, dut_no):

        hardware_columns = {
            1: 1,
            2: 3,
            3: 5,
            4: 7
        }

        can_columns = {
            1: 2,
            2: 4,
            3: 6,
            4: 8
        }

        for item in self.row_map.values():

            values = list(self.table.tree.item(item)["values"])

            values[hardware_columns[dut_no]] = ""
            values[can_columns[dut_no]] = ""

            self.table.tree.item(item, values=values)

    def start_channel_refresh(self, channel_id):

        settings = self.context.test_repository.get_channel_settings(channel_id)

        if channel_id == 1:

            if not settings["use_dut_a"]:
                self.clear_dut(1)

            if not settings["use_dut_b"]:
                self.clear_dut(2)

        elif channel_id == 2:

            if not settings["use_dut_a"]:
                self.clear_dut(3)

            if not settings["use_dut_b"]:
                self.clear_dut(4)

        interval = self.context.test_controller.get_interval_seconds(channel_id)

        if interval is None:
            interval = 1

        self.refresh_channel(channel_id)

        timer = self.after(
            interval * 1000,
            lambda ch=channel_id: self.start_channel_refresh(ch)
        )

        self.channel_timers[channel_id] = timer

    
    def get_channel_frame(self, channel_id):
        return self.channel_map[channel_id]


    def update_temperature_summary(
        self,
        dut,
        statistics
    ):

        if dut in (1, 2):
            channel_id = 1
            dut_index = dut - 1
        else:
            channel_id = 2
            dut_index = dut - 3

        channel_frame = self.channel_map[channel_id]

            # Convert parameter names to display names
        # max_name = TEMP_NAME[statistics["max"]["parameter"]]
        # min_name = TEMP_NAME[statistics["min"]["parameter"]]

        charging = statistics["charging"]

        if charging["max"] is not None:

            channel_frame.set_value(
                dut_index,
                "charging",
                "max",
                f'{charging["max"]["value"]:.1f}°C ({TEMP_NAME[charging["max"]["parameter"]]})'
            )

        if charging["min"] is not None:

            channel_frame.set_value(
                dut_index,
                "charging",
                "min",
                f'{charging["min"]["value"]:.1f}°C ({TEMP_NAME[charging["min"]["parameter"]]})'
            )


        discharging = statistics["discharging"]

        if discharging["max"] is not None:

            channel_frame.set_value(
                dut_index,
                "discharging",
                "max",
                f'{discharging["max"]["value"]:.1f}°C ({TEMP_NAME[discharging["max"]["parameter"]]})'
            )


        if discharging["min"] is not None:

            channel_frame.set_value(
                dut_index,
                "discharging",
                "min",
                f'{discharging["min"]["value"]:.1f}°C ({TEMP_NAME[discharging["min"]["parameter"]]})'
            )

        # channel_frame.set_value(
        #     dut_index,
        #     "charging",
        #     "max",
        #     f'{statistics["max"]["value"]:.1f}°C ({max_name})'
        # )

        # channel_frame.set_value(
        #     dut_index,
        #     "charging",
        #     "min",
        #     f'{statistics["min"]["value"]:.1f}°C ({min_name})'
        # )

        

        # channel_frame.set_value(
        #     dut_index,
        #     "charging",
        #     "max",
        #     f'{statistics["max"]["value"]:.1f}°C ({statistics["max"]["parameter"]})'
        # )

        # channel_frame.set_value(
        #     dut_index,
        #     "charging",
        #     "min",
        #     f'{statistics["min"]["value"]:.1f}°C ({statistics["min"]["parameter"]})'
        # )

    def get_dut_mode(self, dut_no):

        test_mode = self.context.test_session.mode

        if test_mode == "Charge":

            if dut_no in (1, 3):
                return "charging"
            else:
                return "discharging"

        elif test_mode == "Discharge":

            if dut_no in (1, 3):
                return "discharging"
            else:
                return "charging"

        return None        # Rest
    
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
            if dut_no in (1, 2):
                channel_id = 1
                dut_index = dut_no - 1
            else:
                channel_id = 2
                dut_index = dut_no - 3

            channel_frame = self.channel_map[channel_id]

            for mode in ("charging", "discharging"):

                channel_frame.set_value(
                    dut_index,
                    mode,
                    "max",
                    "-- °C"
                )

                channel_frame.set_value(
                    dut_index,
                    mode,
                    "min",
                    "-- °C"
                )


    # def restore_channel_progress(self):

    #     progress = (
    #         self.context.test_controller.channel_progress
    #     )

    #     for channel_id, state in progress.items():

    #         if not state.get("running", False):
    #             continue

    #         if channel_id not in self.channel_map:
    #             continue

    #         frame = self.channel_map[channel_id]

    #         frame.set_cycle(
    #             state.get("current_cycle", 0),
    #             state.get("total_cycles", 0)
    #         )

    #         remaining_seconds = state.get(
    #             "remaining_seconds",
    #             0
    #         )

    #         hrs = remaining_seconds // 3600

    #         mins = (
    #             remaining_seconds % 3600
    #         ) // 60

    #         secs = remaining_seconds % 60

    #         frame.set_time_remaining(
    #             f"{hrs:02}:{mins:02}:{secs:02}"
    #         )

    # def restore_test_progress(self):

    #     test_controller = self.context.test_controller

    #     for channel_id in self.channel_map:

    #         progress = test_controller.channel_progress.get(
    #             channel_id
    #         )

    #         if not progress:
    #             continue

    #         if not progress.get("running"):
    #             continue

    #         # -----------------------------
    #         # Restore cycle
    #         # -----------------------------

    #         current_cycle = progress.get(
    #             "current_cycle",
    #             0
    #         )

    #         total_cycles = progress.get(
    #             "total_cycles",
    #             0
    #         )

    #         # -----------------------------
    #         # Restore timer
    #         # -----------------------------

    #         remaining_seconds = progress.get(
    #             "remaining_seconds",
    #             0
    #         )

    #         hours = remaining_seconds // 3600

    #         minutes = (
    #             remaining_seconds % 3600
    #         ) // 60

    #         seconds = (
    #             remaining_seconds % 60
    #         )

    #         time_text = (
    #             f"{hours:02}:"
    #             f"{minutes:02}:"
    #             f"{seconds:02}"
    #         )

    #         # -----------------------------
    #         # Update current channel frame
    #         # -----------------------------

    #         channel_frame = self.channel_map.get(
    #             channel_id
    #         )

    #         if channel_frame is None:
    #             continue

    #         channel_frame.set_cycle(
    #             current_cycle,
    #             total_cycles
    #         )

    #         channel_frame.set_time_remaining(
    #             time_text
    #         )

    #     # Continue syncing while test is running
    #     self.after(
    #         1000,
    #         self.restore_test_progress
    #     )

    def update_test_timer(self):

        try:

            test_controller = self.context.test_controller

            for channel_id, progress in (
                test_controller.channel_progress.items()
            ):

                if not progress.get("running"):
                    continue

                current_cycle = progress.get(
                    "current_cycle",
                    0
                )

                total_cycles = progress.get(
                    "total_cycles",
                    0
                )

                remaining = progress.get(
                    "remaining_seconds",
                    0
                )

                # -----------------------------------------
                # FORMAT TIME
                # -----------------------------------------

                hours = remaining // 3600

                minutes = (
                    remaining % 3600
                ) // 60

                seconds = (
                    remaining % 60
                )

                text = (
                    f"{hours:02}:"
                    f"{minutes:02}:"
                    f"{seconds:02}"
                )

                # -----------------------------------------
                # UPDATE CHANNEL FRAME
                # -----------------------------------------

                frame = self.channel_map.get(
                    channel_id
                )

                if frame is None:
                    continue

                if not frame.winfo_exists():
                    continue

                frame.set_cycle(
                    current_cycle,
                    total_cycles
                )

                frame.set_time_remaining(
                    text
                )

        except Exception as e:

            print(
                f"Live timer update error: {e}"
            )

        # -----------------------------------------
        # RUN AGAIN
        # -----------------------------------------

        try:

            if self.winfo_exists():

                self.after(
                    1000,
                    self.update_test_timer
                )

        except tk.TclError:

            pass



    # def update_test_timer(self):

    #     try:

    #         test_controller = self.context.test_controller

    #         for channel_id, progress in (
    #             test_controller.channel_progress.items()
    #         ):

    #             if not progress.get("running"):
    #                 continue

    #             # -----------------------------------------
    #             # CURRENT CYCLE
    #             # -----------------------------------------

    #             current_cycle = progress.get(
    #                 "current_cycle",
    #                 0
    #             )

    #             total_cycles = progress.get(
    #                 "total_cycles",
    #                 0
    #             )

    #             # -----------------------------------------
    #             # REMAINING TIME
    #             # -----------------------------------------

    #             end_time = progress.get(
    #                 "end_time"
    #             )

    #             if end_time is not None:

    #                 remaining = max(
    #                     0,
    #                     int(end_time - time.time())
    #                 )

    #             else:

    #                 remaining = progress.get(
    #                     "remaining_seconds",
    #                     0
    #                 )

    #             # Keep controller state updated
    #             progress["remaining_seconds"] = remaining

    #             # -----------------------------------------
    #             # FORMAT TIME
    #             # -----------------------------------------

    #             hours = remaining // 3600

    #             minutes = (
    #                 remaining % 3600
    #             ) // 60

    #             seconds = remaining % 60

    #             text = (
    #                 f"{hours:02}:"
    #                 f"{minutes:02}:"
    #                 f"{seconds:02}"
    #             )

    #             # -----------------------------------------
    #             # CURRENT CHANNEL FRAME
    #             # -----------------------------------------

    #             frame = self.channel_map.get(
    #                 channel_id
    #             )

    #             if frame is None:
    #                 continue

    #             if not frame.winfo_exists():
    #                 continue

    #             frame.set_cycle(
    #                 current_cycle,
    #                 total_cycles
    #             )

    #             frame.set_time_remaining(
    #                 text
    #             )

    #     except Exception as e:

    #         print(
    #             f"Live timer update error: {e}"
    #         )

    #     # ---------------------------------------------
    #     # CONTINUE FOREVER WHILE THIS VIEW EXISTS
    #     # ---------------------------------------------

    #     try:

    #         if self.winfo_exists():

    #             self.after(
    #                 1000,
    #                 self.update_test_timer
    #             )

    #     except tk.TclError:

    #         pass
    # def restore_channel_progress(self):

    #     progress = (
    #         self.context.test_controller.channel_progress
    #     )

    #     for channel_id, state in progress.items():

    #         if not state.get("running", False):
    #             continue

    #         if channel_id not in self.channel_map:
    #             continue

    #         frame = self.channel_map[channel_id]

    #         current_cycle = state.get(
    #             "current_cycle",
    #             0
    #         )

    #         total_cycles = state.get(
    #             "total_cycles",
    #             0
    #         )

    #         remaining_seconds = state.get(
    #             "remaining_seconds",
    #             0
    #         )

    #         # ==============================================
    #         # RESTORE CYCLE
    #         # ==============================================

    #         frame.set_cycle(
    #             current_cycle,
    #             total_cycles
    #         )

    #         # ==============================================
    #         # RESTORE TIME
    #         # ==============================================

    #         hrs = remaining_seconds // 3600

    #         mins = (
    #             remaining_seconds % 3600
    #         ) // 60

    #         secs = (
    #             remaining_seconds % 60
    #         )

    #         text = (
    #             f"{hrs:02}:"
    #             f"{mins:02}:"
    #             f"{secs:02}"
    #         )

    #         frame.set_time_remaining(
    #             text
    #         )

    # def refresh_table(self):
    
        #     for group, ports in self.context.can_values.items():
    
        #         for port, signals in ports.items():
    
        #             dut_no = PORT_TO_DUT.get(port)
    
        #             if dut_no is None:
        #                 continue
    
        #             for signal, value in signals.items():
    
        #                 table_name = CAN_PARAMETER_MAP.get(signal)
    
        #                 if table_name is None:
        #                     continue
    
        #                 self.update_can_value(
        #                     table_name,
        #                     dut_no,
        #                     f"{value:.2f}"
        #                 )
    
        #     # for dut_no, values in self.context.hardware_values.items():
    
        #     #     for parameter, value in values.items():
    
        #     #         self.update_hardware_value(
        #     #             parameter,
        #     #             dut_no,
        #     #             f"{value:.2f}"
        #     #         )
    
        #     interval = self.get_interval()
            
        #     print(f"Interval: {interval}  type: {type(interval)}")
    
        #     self.after(interval, self.refresh_table)
    
    
        # def get_interval(self):
        #     return self.context.test_controller.get_interval_seconds(self.channel_id)
    