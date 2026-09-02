# controllers/test_controller.py

from datetime import datetime
from instruments.drivers.rp5935a_driver import RP5935ADriver
from instruments.drivers.el4935a_driver import EL4935ADriver
from instruments.drivers.el34143a_driver import EL34143ADriver
from instruments.drivers.asr3400_driver import ASR3400Driver
from instruments.drivers.adam6052_driver import Adam6052Driver
from services.csv_logger import CSVLogger
import time
import threading
from widgets.alarm_popup import AlarmPopup
from controllers.line_regulation_controller import LineRegulationController

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
class TestController:

    def __init__(self, context):

        self.context = context
        # self.pause_event = threading.Event()
        # self.pause_event.set()
        self.channel_pause_events = {
            1: threading.Event(),
            2: threading.Event()
        }

        for event in self.channel_pause_events.values():
            event.set()

        self.alarm_active = False
        self.next_cycle_requested = False
        self.channel_alarm_active = {
            1: False,
            2: False
        }
        self.channel_next_cycle_requested = {
            1: False,
            2: False
        }
        # self.channel_progress = {
        #     1: {
        #         "current_cycle": 0,
        #         "total_cycles": 0,
        #         "remaining_seconds": 0,
        #         "running": False
        #     },
        #     2: {
        #         "current_cycle": 0,
        #         "total_cycles": 0,
        #         "remaining_seconds": 0,
        #         "running": False
        #     }
        #     }

        self.channel_running = {
                1: False,
                2: False
            }
        
        self.channel_progress = {
            1: {
                "current_cycle": 0,
                "total_cycles": 0,
                "remaining_seconds": 0,
                "end_time": None,
                "running": False
            },
            2: {
                "current_cycle": 0,
                "total_cycles": 0,
                "remaining_seconds": 0,
                "end_time": None,
                "running": False
            }
        }
        self.line_regulation_controller = LineRegulationController(
    self.context
)
        # self.csv_logger = CSVLogger(
        #     base_folder="CSV_Logs"
        # )
        # self.controller = context.test_repository
    def raise_alarm(self, channel_id, alarms):

        if self.channel_alarm_active.get(
            channel_id,
            False
        ):
            return

        self.channel_alarm_active[
            channel_id
        ] = True

        print(
            f"========== ALARM CHANNEL {channel_id} =========="
        )

        # -----------------------------------------
        # PAUSE ONLY THIS CHANNEL
        # -----------------------------------------

        self.pause_test(channel_id)

        # -----------------------------------------
        # POPUP ON MAIN THREAD
        # -----------------------------------------

        self.context.root.after(
            0,
            lambda: AlarmPopup(
                self.context.root,
                self,
                alarms,
                channel_id
            )
        )
    

    # def raise_alarm(self, channel_id, alarms):

    #     if self.alarm_active:
    #         return

    #     self.alarm_active = True

    #     print(
    #         f"========== ALARM CHANNEL {channel_id} =========="
    #     )

    #     # -----------------------------------------
    #     # PAUSE ONLY THIS CHANNEL
    #     # -----------------------------------------

    #     self.pause_test(channel_id)

    #     # -----------------------------------------
    #     # CREATE POPUP ON TKINTER MAIN THREAD
    #     # -----------------------------------------

    #     self.context.root.after(
    #         0,
    #         lambda: AlarmPopup(
    #             self.context.root,
    #             self,
    #             alarms,
    #             channel_id
    #         )
    #     )
    
    # def raise_alarm(self, alarms):

    #     if self.alarm_active:
    #         return

    #     self.alarm_active = True

    #     # Pause the test
    #     self.pause_test()

    #     # Create popup on Tkinter main thread
    #     self.context.root.after(
    #         0,
    #         lambda: AlarmPopup(
    #             self.context.root,
    #             self,
    #             alarms
    #         )
    #     )
    
    # def raise_alarm(self, dut_id, parameter):

    #     if self.alarm_active:
    #         return

    #     self.alarm_active = True

    #     self.pause_test()

    #     self.context.root.after(
    #         0,
    #         lambda: AlarmPopup(
    #             self.context.root,
    #             self,
    #             dut_id,
    #             parameter
    #         )
    #     )

    # def raise_alarm(self, dut_id, parameter):

    #     if self.alarm_active:
    #         print("Alarm already active")
    #         return

    #     self.alarm_active = True

    #     print(
    #         f"Raising alarm: DUT {dut_id}, {parameter}"
    #     )

    #     # Pause endurance thread
    #     self.pause_test()

    #     # Tkinter must run in main thread
    #     self.context.root.after(
    #         0,
    #         lambda: AlarmPopup(
    #             self.context.root,
    #             self,
    #             dut_id,
    #             parameter
    #         )
    #     )
    
    # def raise_alarm(self, dut_id, parameter):

    #     if self.alarm_active:
    #         print("Alarm_active")
    #         return

    #     self.alarm_active = True

    #     self.pause_test()

    #     self.context.app.after(
    #         0,
    #         lambda: self.context.main_window.show_alarm_popup(
    #             dut_id,
    #             parameter
    #         )
    #     )

    # def wait_seconds(self, seconds):

    #     for _ in range(seconds):

    #         self.pause_event.wait()

    #         if self.next_cycle_requested:
    #             return

    #         time.sleep(1)

    # def pause_test(self):
    #     # self.pause_event.clear()
    #     self.channel_pause_events[
    #         channel_id
    #     ].clear()

    # def resume_test(self):
    #     # self.pause_event.set()
    #     self.channel_pause_events[
    #         channel_id
    #     ].set()
    #     self.alarm_active = False

    # def next_cycle(self):

    #     self.next_cycle_requested = True

    #     self.pause_event.set()

    #     self.alarm_active = False

    def pause_test(self, channel_id):

        print(
            f"Pausing Channel {channel_id}"
        )

        self.channel_pause_events[
            channel_id
        ].clear()

        self.alarm_active = True


    # def resume_test(self, channel_id):

    #     print(
    #         f"Resuming Channel {channel_id}"
    #     )

    #     self.channel_pause_events[
    #         channel_id
    #     ].set()

    #     self.alarm_active = False

    def resume_test(self, channel_id):

        print(
            f"Resuming Channel {channel_id}"
        )

        self.channel_pause_events[
            channel_id
        ].set()

        self.channel_alarm_active[
            channel_id
        ] = False


    # def next_cycle(self, channel_id):

    #     print(
    #         f"Proceeding to next cycle on Channel {channel_id}"
    #     )

    #     self.channel_next_cycle_requested[
    #         channel_id
    #     ] = True

    #     # Wake wait_seconds()
    #     self.channel_pause_events[
    #         channel_id
    #     ].set()

    #     self.alarm_active = False


    def next_cycle(self, channel_id):

        print(
            f"Next cycle requested for Channel {channel_id}"
        )

        self.channel_next_cycle_requested[
            channel_id
        ] = True

        self.channel_pause_events[
            channel_id
        ].set()

        self.channel_alarm_active[
            channel_id
        ] = False
        
    def get_can_live_values(self, dut_no):

        port_map = {
            1: "PCAN_USBBUS1",
            2: "PCAN_USBBUS2",
            3: "PCAN_USBBUS3",
            4: "PCAN_USBBUS4"
        }

        port = port_map.get(
            dut_no
        )

        values = {}

        if port is None:
            return values

        # ==========================================================
        # Find CAN data belonging to this port
        # ==========================================================

        for channel_data in self.context.can_values.values():

            if port not in channel_data:
                continue

            signals = channel_data[port]

            for signal, value in signals.items():

                parameter = CAN_PARAMETER_MAP.get(
                    signal
                )

                if parameter is None:
                    continue

                try:
                    values[parameter] = float(
                        value
                    )

                except (
                    ValueError,
                    TypeError
                ):
                    values[parameter] = value

        # ==========================================================
        # CALCULATED CAN VALUES
        # ==========================================================

        vin = values.get(
            "OBC Input Voltage",
            0
        )

        iin = values.get(
            "OBC Input Current",
            0
        )

        vout = values.get(
            "OBC Output Voltage",
            0
        )

        iout = values.get(
            "OBC Output Current",
            0
        )

        try:

            obc_input_power = (
                vin *
                iin *
                0.99
            )

            obc_output_power = (
                vout *
                iout
            )

        except (
            TypeError,
            ValueError
        ):

            obc_input_power = 0
            obc_output_power = 0

        if obc_input_power > 0:

            obc_efficiency = (
                obc_output_power /
                obc_input_power
            ) * 100

        else:

            obc_efficiency = 0

        values[
            "OBC_Input_Power"
        ] = obc_input_power

        values[
            "OBC_Output_Power"
        ] = obc_output_power

        values[
            "OBC Efficiency"
        ] = obc_efficiency

        with open("logs/efficiency_debug.txt", "a", encoding="utf-8") as f:
            f.write(
                f"DUT={dut_no}, "
                f"InputPower={obc_input_power}, "
                f"OutputPower={obc_output_power}, "
                f"Efficiency={obc_efficiency}\n"
            )

        # ==========================================================
        # HPDCDC
        # ==========================================================

        hp_in_v = values.get(
            "HPDCDC Input Voltage",
            0
        )

        hp_in_i = values.get(
            "HPDCDC Input Current",
            0
        )

        hp_out_v = values.get(
            "HPDCDC Output Voltage",
            0
        )

        hp_out_i = values.get(
            "HPDCDC Output Current",
            0
        )

        try:

            hp_input_power = (
                hp_in_v *
                hp_in_i
            )

            hp_output_power = (
                hp_out_v *
                hp_out_i
            )

        except (
            TypeError,
            ValueError
        ):

            hp_input_power = 0
            hp_output_power = 0

        if hp_input_power > 0:

            hp_efficiency = (
                hp_output_power /
                hp_input_power
            ) * 100

        else:

            hp_efficiency = 0

        values[
            "HPDCDC_Input_Power"
        ] = hp_input_power

        values[
            "HPDCDC_Output_Power"
        ] = hp_output_power

        values[
            "HPDCDC_Efficiency"
        ] = hp_efficiency

        return values

    def get_hardware_live_values(self, dut_no):

        values = {}

        hardware = self.context.hardware_values.get(
            dut_no,
            {}
        )

        # ==========================================================
        # PW3337 RAW VALUES
        # ==========================================================

        for signal, value in hardware.items():

            parameter = PW3337_PARAMETER_MAP.get(
                signal
            )

            if parameter is None:
                continue

            try:
                values[parameter] = float(
                    value
                )

            except (
                ValueError,
                TypeError
            ):
                values[parameter] = value

        # ==========================================================
        # HARDWARE POWER VALUES
        # ==========================================================

        # These may already exist from PW3337.
        # If they don't, calculate them.

        if (
            "OBC_Input_Power" not in values
            and
            "OBC Input Voltage" in values
            and
            "OBC Input Current" in values
        ):

            values[
                "OBC_Input_Power"
            ] = (
                values["OBC Input Voltage"]
                *
                values["OBC Input Current"]
            )

        if (
            "OBC_Output_Power" not in values
            and
            "OBC Output Voltage" in values
            and
            "OBC Output Current" in values
        ):

            values[
                "OBC_Output_Power"
            ] = (
                values["OBC Output Voltage"]
                *
                values["OBC Output Current"]
            )

        # ==========================================================
        # OBC EFFICIENCY
        # ==========================================================

        input_power = values.get(
            "OBC_Input_Power",
            0
        )

        output_power = values.get(
            "OBC_Output_Power",
            0
        )

        if input_power > 0:

            values[
                "OBC Efficiency"
            ] = (
                output_power /
                input_power
            ) * 100

        else:

            values[
                "OBC Efficiency"
            ] = 0

        # ==========================================================
        # HPDCDC POWER
        # ==========================================================

        if (
            "HPDCDC_Input_Power" not in values
            and
            "HPDCDC Input Voltage" in values
            and
            "HPDCDC Input Current" in values
        ):

            values[
                "HPDCDC_Input_Power"
            ] = (
                values["HPDCDC Input Voltage"]
                *
                values["HPDCDC Input Current"]
            )

        if (
            "HPDCDC_Output_Power" not in values
            and
            "HPDCDC Output Voltage" in values
            and
            "HPDCDC Output Current" in values
        ):

            values[
                "HPDCDC_Output_Power"
            ] = (
                values["HPDCDC Output Voltage"]
                *
                values["HPDCDC Output Current"]
            )

        hp_input_power = values.get(
            "HPDCDC_Input_Power",
            0
        )

        hp_output_power = values.get(
            "HPDCDC_Output_Power",
            0
        )

        if hp_input_power > 0:

            values[
                "HPDCDC_Efficiency"
            ] = (
                hp_output_power /
                hp_input_power
            ) * 100

        else:

            values[
                "HPDCDC_Efficiency"
            ] = 0

        return values

    def get_running_duts(self, channel_id):

        settings = (
            self.context
            .test_repository
            .get_channel_settings(
                channel_id
            )
        )

        running_duts = []

        if channel_id == 1:

            if settings["use_dut_a"]:
                running_duts.append(1)

            if settings["use_dut_b"]:
                running_duts.append(2)

        elif channel_id == 2:

            if settings["use_dut_a"]:
                running_duts.append(3)

            if settings["use_dut_b"]:
                running_duts.append(4)

        return running_duts
    
    # def start_test(self,channel_id,values):

    #     # Already running?
    #     if self.context.app_state.test_running:
    #         return

    #     # Update state

    #     self.context.app_state.test_running = True

    #     # Create test session

    #     self.context.test_session.start_time = (
    #         datetime.now()
    #     )

    #     self.context.test_session.status = "Running"

        
    #     self.context.test_repository.save_settings(channel_id,values)
    #     # self.run_test(channel_id)
    #     # Start instruments

    #     self.context.instrument_manager.start_channel(channel_id)

    #     print("Test Started")
    

    def start_test(self, channel_id, values):
        print(values)
        # if self.context.app_state.test_running:
        #     return

        print(
        f"========== START TEST: CHANNEL {channel_id} =========="
        )

        # -----------------------------------------
        # CHANNEL ALREADY RUNNING?
        # -----------------------------------------

        if self.channel_running.get(channel_id, False):

            print(
                f"Channel {channel_id} is already running."
            )

            return

        # -----------------------------------------
        # MARK THIS CHANNEL RUNNING
        # -----------------------------------------

        self.channel_running[channel_id] = True
        self.update_global_test_state()

        conn = self.context.database_manager.get_connection()

        if values['test_type'] == "Endurance":
            settings=self.context.parameter_repository.get_rp_initial_settings(values["dut_id"])

            current = settings["dc_output_current"]

            print("Current : ", current)

            print("Channel ID : " ,channel_id)



            # input_settings=self.

            print("DUT ID : ",values["dut_id"])

            di_load_settings=self.context.parameter_repository.get_el4935a_initial_settings(values["dut_id"])

            ch_load_settings=self.context.parameter_repository.get_el34143a_initial_settings(values["dut_id"])
                    
            dbc_path = self.context.test_repository.get_dbc_file(values["dut_id"])



            print ("dbc :" ,dbc_path)

            if dbc_path is None:
                raise RuntimeError("No DBC file assigned to this DUT.")

            self.context.decoder.load_dbc(dbc_path)

            loaded = self.context.decoder.load_dbc(dbc_path)

            print("DBC loaded:", loaded)
            print("DBC file:", self.context.decoder.dbc_file)

            dut = self.context.parameter_repository.get_by_name(
                values["dut_type"]
            )

            bitrate = dut["dut_bit_rate"]

            self.context.can_manager.connect_channel(
                channel_id=channel_id,
                bitrate=bitrate
            )

            if channel_id == 1 :
                self.context.can_manager.set_charge_current(
                    channel_id=channel_id,
                    port="PCAN_USBBUS1",
                    current=current
                )

                self.context.can_manager.set_charge_current(
                                channel_id=channel_id,
                                port="PCAN_USBBUS2",
                                current=current
                            )
            elif channel_id == 2:
                self.context.can_manager.set_charge_current(
                                channel_id=channel_id,
                                port="PCAN_USBBUS3",
                                current=current
                            )

                self.context.can_manager.set_charge_current(
                                channel_id=channel_id,
                                port="PCAN_USBBUS4",
                                current=current
                            )
                
            
            endurance = self.context.parameter_repository.get_endurance_settings(conn,
                values["dut_type"]
            )

            if endurance is None:
                raise RuntimeError("Endurance settings not found.")

            charge_time = endurance["charge_time"]
            discharge_time = endurance["discharge_time"]
            rest1 = endurance["rest_time1"]
            rest2 = endurance["rest_time2"]

            input_voltage = endurance["ac_input_voltage"]
            input_frequency = endurance["ac_input_frequency"]

            self.asr3400_driver = self.context.instrument_manager.get_driver(ASR3400Driver)

            if self.asr3400_driver is None:
                raise RuntimeError("ASR3400 is not connected")

            self.asr3400_driver.initial_setting(input_voltage,input_frequency)

            self.rp5935a_driver = self.context.instrument_manager.get_driver(RP5935ADriver)

            if self.rp5935a_driver is None:
                raise RuntimeError("RP5935A is not connected")

            self.rp5935a_driver.initial_setting(settings)

            self.el4935a_driver = self.context.instrument_manager.get_driver(EL4935ADriver)

            if self.el4935a_driver is None:
                raise RuntimeError("EL4935A is not connected")

            self.el4935a_driver.initial_setting(di_load_settings)

            self.el34143a_driver = self.context.instrument_manager.get_driver(EL34143ADriver)

            if self.el34143a_driver is None:
                raise RuntimeError("EL34143A is not connected")

            self.el34143a_driver.initial_setting(ch_load_settings)
            # self.context.instrument_manager.rp5935a_driver.initial_setting()

            # RP5935ADriver.initial_setting()


            self.context.app_state.test_running = True

            self.context.test_session.start_time = datetime.now()
            self.context.test_session.status = "Running"

            self.context.test_repository.save_settings(
                channel_id,
                values
            )

            self.context.data_logger.start_test(
                values["test_name"]
            )

            # endurance = self.context.parameter_repository.get_endurance_settings(conn,
            #     values["dut_type"]
            # )

            # if endurance is None:
            #     raise RuntimeError("Endurance settings not found.")

            # charge_time = endurance["charge_time"]
            # discharge_time = endurance["discharge_time"]
            # rest1 = endurance["rest_time1"]
            # rest2 = endurance["rest_time2"]

            # channel_settings = self.context.test_repository.get_channel_settings(
            #     channel_id
            # )

            channel_settings = self.context.test_repository.get_channel_settings(channel_id)

            if channel_settings is None:
                raise RuntimeError(f"No settings found for channel {channel_id}")

            

            # dut_id = channel_settings["dut_id"]
            # test_type = channel_settings["test_type"]
            # test_name = channel_settings["test_name"]
            # cycles = channel_settings["no_of_cycles"]
            # interval = channel_settings["interval_seconds"]
            # use_dut_a = channel_settings["use_dut_a"]
            # use_dut_b = channel_settings["use_dut_b"]
            cycles = channel_settings["no_of_cycles"]
            interval = channel_settings["interval_seconds"]


            self.context.instrument_manager.start_channel(channel_id)
            # self.csv_logger.start_test(
            #     values["test_name"]
            # )

            import threading

            threading.Thread(
                target=self.run_endurance_cycle,
                args=(
                    channel_id,
                    charge_time,
                    discharge_time,
                    rest1,
                    rest2,
                    cycles,
                    interval
                ),
                daemon=True
            ).start()
            

            print("Test Started")

            for frame in self.get_all_channel_frames(channel_id):

                frame.after(
                    0,
                    lambda f=frame: f.stop_btn.configure(state="normal")
                )
            self.context.app_controller.show_page("Endurance-Live Monitoring")


        # elif values['test_type'] == "Line Regulation":
        #     print("Line Regulation Test")

        elif values["test_type"] == "Line Regulation":

            print("Line Regulation Test")

            self.line_regulation_controller.start_test(
                channel_id=channel_id,
                values=values
            )

            # for frame in self.get_all_channel_frames(channel_id):

            #     frame.after(
            #         0,
            #         lambda f=frame:
            #         f.stop_btn.configure(
            #             state="normal"
            #         )
            #     )

            self.context.app_controller.show_page(
                "Line Regulation"
            )

        elif values['test_type'] == "Load Regulation":
            print("Load Regulation Test")

        else:
            print(values['test_type']," No such test")
        # decoded = self.context.dbc_decoder.decode(
        #     msg.arbitration_id,
        #     msg.data
        # )

        # if decoded:

        #     for signal in decoded:

        #         print(signal["parameter"], signal["value"])

        
    # def stop_test(self, channel_id):

    #     if not self.context.app_state.test_running:
    #         return

    #     self.context.app_state.test_running = False

    #     self.context.instrument_manager.stop_channel(channel_id)

    #     # Stop CAN workers
    #     self.context.can_manager.disconnect_channel(channel_id)

    #     self.rp5935a_driver.off()
    #     self.el34143a_driver.off()
    #     self.el4935a_driver.off()
    #     self.asr3400_driver.off()

    #     self.context.test_session.status = "Completed"

    #     # channel_frame = (
    #     #     self.context
    #     #     .efficiency_trend_controller
    #     #     .view
    #     #     .channel_map[channel_id]
    #     # )

    #     # channel_frame.after(
    #     #     0,
    #     #     lambda: channel_frame.set_time_remaining("00:00:00")
    #     # )

    #     self.reset_channel_ui(channel_id)
    #     card = self.context.channel_cards.get(channel_id)

    #     if card:
    #         card.after(
    #             0,
    #             card.enable_start_button
    #         )
    #     print("Test Stopped")


    # def stop_test(self, channel_id):

    #     print(
    #         f"========== STOP TEST: CHANNEL {channel_id} =========="
    #     )

    #     # =====================================================
    #     # STOP TEST STATE FIRST
    #     # =====================================================

    #     self.context.app_state.test_running = False

    #     self.channel_progress[channel_id]["running"] = False
    #     self.channel_progress[channel_id]["remaining_seconds"] = 0

    #     # =====================================================
    #     # STOP INSTRUMENTS
    #     # =====================================================

    #     try:

    #         self.context.instrument_manager.stop_channel(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"Instrument stop error: {e}"
    #         )

    #     # =====================================================
    #     # STOP CAN
    #     # =====================================================

    #     try:

    #         self.context.can_manager.disconnect_channel(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"CAN stop error: {e}"
    #         )

    #     # =====================================================
    #     # TURN OFF POWER INSTRUMENTS
    #     # =====================================================

    #     drivers = [
    #         getattr(self, "rp5935a_driver", None),
    #         getattr(self, "el34143_driver", None),
    #         getattr(self, "el4935_driver", None),
    #         getattr(self, "asr3400_driver", None)
    #     ]

    #     for driver in drivers:

    #         if driver is None:
    #             continue

    #         try:

    #             driver.off()

    #         except Exception as e:

    #             print(
    #                 f"Driver OFF error: {e}"
    #             )

    #     # =====================================================
    #     # TEST SESSION
    #     # =====================================================

    #     self.context.test_session.status = "Completed"
    #     self.context.test_session.mode = "Rest"

    #     # =====================================================
    #     # RESET GUI
    #     # =====================================================

    #     try:

    #         self.reset_channel_ui(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"GUI reset error: {e}"
    #         )

    #     # =====================================================
    #     # ENABLE START BUTTON
    #     # =====================================================

    #     try:

    #         card = self.context.channel_cards.get(
    #             channel_id
    #         )

    #         if card:

    #             card.after(
    #                 0,
    #                 card.enable_start_button
    #             )

    #     except Exception as e:

    #         print(
    #             f"Start button enable error: {e}"
    #         )

    #     print(
    #         f"========== CHANNEL {channel_id} STOPPED =========="
    #     )

    def stop_test(self, channel_id):

        print(
            f"========== STOP TEST: CHANNEL {channel_id} =========="
        )

        # ==========================================================
        # STOP CHANNEL
        # ==========================================================

        self.channel_running[channel_id] = False

        # -----------------------------------------
        # WAKE UP wait_seconds()
        # -----------------------------------------

        self.channel_pause_events[channel_id].set()

        # ==========================================================
        # STOP TIMER
        # ==========================================================

        if channel_id in self.channel_progress:

            self.channel_progress[channel_id][
                "running"
            ] = False

            self.channel_progress[channel_id][
                "remaining_seconds"
            ] = 0

            self.channel_progress[channel_id][
                "end_time"
            ] = None

        # ==========================================================
        # WAKE CHANNEL PAUSE
        # ==========================================================

        if channel_id in self.channel_pause_events:

            self.channel_pause_events[
                channel_id
            ].set()

        # ==========================================================
        # STOP HARDWARE
        # ==========================================================

        try:
            self.context.instrument_manager.stop_channel(
                channel_id
            )
        except Exception as e:
            print("Instrument stop error:", e)

        try:
            self.context.can_manager.disconnect_channel(
                channel_id
            )
        except Exception as e:
            print("CAN disconnect error:", e)

        # ==========================================================
        # TURN OFF DRIVERS
        # ==========================================================

        for driver in [
            getattr(self, "rp5935a_driver", None),
            getattr(self, "el34143_driver", None),
            getattr(self, "el4935_driver", None),
            getattr(self, "asr3400_driver", None),
        ]:

            if driver is not None:

                try:
                    driver.off()
                except Exception as e:
                    print("Driver OFF error:", e)

        # ==========================================================
        # SESSION
        # ==========================================================

        self.context.test_session.status = "Completed"
        self.context.test_session.mode = "Rest"

        # ==========================================================
        # GUI
        # ==========================================================

        try:
            self.reset_channel_ui(channel_id)
        except Exception as e:
            print("GUI reset error:", e)

        card = self.context.channel_cards.get(
            channel_id
        )

        if card:

            card.after(
                0,
                card.enable_start_button
            )

        # ==========================================================
        # GLOBAL STATE
        # ==========================================================

        self.update_global_test_state()

        print(
            f"Channel {channel_id} stopped."
        )

    # def stop_test(self, channel_id):

    #     print(
    #         f"========== STOP TEST: CHANNEL {channel_id} =========="
    #     )

    #     # ==========================================================
    #     # CHECK CHANNEL STATE
    #     # ==========================================================

    #     if not self.channel_running.get(channel_id, False):

    #         print(
    #             f"Channel {channel_id} is already stopped."
    #         )

    #         return

    #     # ==========================================================
    #     # STOP ONLY THIS CHANNEL
    #     # ==========================================================

    #     self.channel_running[channel_id] = False
    #     self.update_global_test_state()

    #     # ==========================================================
    #     # STOP TIMER STATE
    #     # ==========================================================

    #     if channel_id in self.channel_progress:

    #         self.channel_progress[channel_id][
    #             "running"
    #         ] = False

    #         self.channel_progress[channel_id][
    #             "remaining_seconds"
    #         ] = 0

    #         self.channel_progress[channel_id][
    #             "end_time"
    #         ] = None

    #     # ==========================================================
    #     # WAKE CHANNEL IF IT IS WAITING FOR ALARM RESUME
    #     # ==========================================================

    #     if channel_id in self.channel_pause_events:

    #         self.channel_pause_events[
    #             channel_id
    #         ].set()

    #     # ==========================================================
    #     # STOP INSTRUMENTS
    #     # ==========================================================

    #     try:

    #         self.context.instrument_manager.stop_channel(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"Instrument stop error: {e}"
    #         )

    #     # ==========================================================
    #     # STOP CAN
    #     # ==========================================================

    #     try:

    #         self.context.can_manager.disconnect_channel(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"CAN disconnect error: {e}"
    #         )

    #     # ==========================================================
    #     # TURN OFF INSTRUMENT DRIVERS
    #     # ==========================================================

    #     for driver in [
    #         getattr(self, "rp5935a_driver", None),
    #         getattr(self, "el34143_driver", None),
    #         getattr(self, "el4935_driver", None),
    #         getattr(self, "asr3400_driver", None),
    #     ]:

    #         if driver is None:
    #             continue

    #         try:

    #             driver.off()

    #         except Exception as e:

    #             print(
    #                 f"Driver OFF error: {e}"
    #             )

    #     # ==========================================================
    #     # TEST SESSION
    #     # ==========================================================

    #     self.context.test_session.status = "Completed"

    #     self.context.test_session.mode = "Rest"

    #     # ==========================================================
    #     # RESET CHANNEL GUI
    #     # ==========================================================

    #     try:

    #         self.reset_channel_ui(
    #             channel_id
    #         )

    #     except Exception as e:

    #         print(
    #             f"GUI reset error: {e}"
    #         )

    #     # ==========================================================
    #     # ENABLE START BUTTON
    #     # ==========================================================

    #     card = self.context.channel_cards.get(
    #         channel_id
    #     )

    #     if card:

    #         card.after(
    #             0,
    #             card.enable_start_button
    #         )

    #     # ==========================================================
    #     # UPDATE GLOBAL STATUS
    #     # ==========================================================

    #     self.context.app_state.test_running = any(
    #         self.channel_running.values()
    #     )

    #     print(
    #         f"Channel {channel_id} stopped."
    #     )

    #     print(
    #         "Global test_running =",
    #         self.context.app_state.test_running
    #     )

    # def stop_test(self, channel_id):

    #     if not self.context.app_state.test_running:
    #         return

    #     self.context.app_state.test_running = False

    #     # -----------------------------------------
    #     # STOP TIMER STATE
    #     # -----------------------------------------

    #     self.channel_progress[channel_id]["running"] = False
    #     self.channel_progress[channel_id]["remaining_seconds"] = 0
    #     self.channel_progress[channel_id]["end_time"] = None

    #     # -----------------------------------------
    #     # STOP INSTRUMENTS
    #     # -----------------------------------------

    #     self.context.instrument_manager.stop_channel(
    #         channel_id
    #     )

    #     self.context.can_manager.disconnect_channel(
    #         channel_id
    #     )

    #     self.rp5935a_driver.off()
    #     self.el34143a_driver.off()
    #     self.el4935a_driver.off()
    #     self.asr3400_driver.off()

    #     self.context.test_session.status = "Completed"

    #     self.reset_channel_ui(channel_id)

    #     card = self.context.channel_cards.get(
    #         channel_id
    #     )

    #     if card:

    #         card.after(
    #             0,
    #             card.enable_start_button
    #         )

    #     print("Test Stopped")

    def reset_channel_ui(self, channel_id):

        for frame in self.get_all_channel_frames(channel_id):

            frame.after(
                0,
                lambda f=frame: (
                    # f.set_cycle(0, 0),
                    f.set_time_remaining("00:00:00"),
                    f.stop_btn.configure(state="disabled")
                )
            )


    def process_can_data(self, port, decoded_data):

        channel_map = {
            "PCAN_USBBUS1": 1,
            "PCAN_USBBUS2": 1,
            "PCAN_USBBUS3": 2,
            "PCAN_USBBUS4": 2,
        }

        channel_id = channel_map[port]

        for signal in decoded_data:

            self.context.can_values[channel_id][port][
                signal["parameter"]
            ] = signal["value"]

    def get_interval_seconds(self, channel_id):
        conn = self.context.database_manager.get_connection()
        return self.context.test_repository.get_interval_seconds(
            conn,
            channel_id
        )

    # import time

    # def run_endurance_cycle(self, channel_id, values, endurance):

    #     charge_time = endurance["charge_time"]
    #     discharge_time = endurance["discharge_time"]
    #     rest1 = endurance["rest_time1"]
    #     rest2 = endurance["rest_time2"]
    #     cycles = endurance["no_of_cycles"]

    #     # adam = self.context.instrument_manager.get_driver(Adam6052Driver)

    #     for cycle in range(cycles):

    #         if not self.context.app_state.test_running:
    #             break

    #         print(f"Cycle {cycle+1}/{cycles}")

    #         ####################################
    #         # CHARGE
    #         ####################################

    #         print("Charging...")

    #         # adam.set_charge_mode(channel_id)

    #         self.context.test_session.mode = "Charge"

    #         self.wait_seconds(charge_time)

    #         ####################################
    #         # REST
    #         ####################################

    #         print("Rest after charge")

    #         # adam.output_off(channel_id)

    #         self.context.test_session.mode = "Rest"

    #         self.wait_seconds(rest1)

    #         ####################################
    #         # DISCHARGE
    #         ####################################

    #         print("Discharging...")

    #         # adam.set_discharge_mode(channel_id)

    #         self.context.test_session.mode = "Discharge"

    #         self.wait_seconds(discharge_time)

    #         ####################################
    #         # REST
    #         ####################################

    #         print("Rest after discharge")

    #         # adam.output_off(channel_id)

    #         self.context.test_session.mode = "Rest"

    #         self.wait_seconds(rest2)

    #     print("Endurance Completed")

    #     self.context.app_state.test_running = False


    

    # def run_endurance_cycle(
    #     self,
    #     channel_id,
    #     charge_time,
    #     discharge_time,
    #     rest1,
    #     rest2,
    #     cycles,
    #     interval
    # ):

    #     total_test_seconds = int(
    #         (
    #             charge_time +
    #             rest1 +
    #             discharge_time +
    #             rest2
    #         ) * cycles * 60
    #     )

    #     self.channel_progress[channel_id] = {
    #         "current_cycle": 1,
    #         "total_cycles": cycles,
    #         "remaining_seconds": total_test_seconds,
    #         "end_time": time.time() + total_test_seconds,
    #         "running": True
    #     }

    #     # adam_driver = self.context.instrument_manager.get_driver(Adam6052Driver)

    #     # adam_driver = (
    #     #     self.context
    #     #     .instrument_manager
    #     #     .get_adam_driver(
    #     #         channel_id
    #     #     )
    #     # )

    #             # All times are in minutes
    #     cycle_time = (
    #         charge_time +
    #         rest1 +
    #         discharge_time +
    #         rest2
    #     )

    #     print(
    #         f"""
    #         charge_time     = {charge_time}
    #         discharge_time  = {discharge_time}
    #         rest1           = {rest1}
    #         rest2           = {rest2}
    #         cycles          = {cycles}
    #         interval        = {interval}
    #         """
    #     )

    #     total_seconds_remaining = int(cycle_time * cycles * 60)
    #     for cycle in range(cycles):

    #         if not self.context.app_state.test_running:
    #             break

            

    #         current_cycle = cycle + 1

    #         cycle_elapsed = 0

    #         self.channel_progress[channel_id]["current_cycle"] = current_cycle

    #         running_duts = self.get_running_duts(
    #             channel_id
    #         )

    #         channel_settings = (
    #             self.context
    #             .test_repository
    #             .get_channel_settings(
    #                 channel_id
    #             )
    #         )

    #         test_name = channel_settings[
    #             "test_name"
    #         ]

    #         # ==================================================
    #         # CREATE CSV FOR EACH ACTIVE DUT
    #         # ==================================================

    #         for dut_no in running_duts:

    #             if dut_no == 1:
    #                 serial_no = channel_settings["dut_a_serial_no"]

    #             elif dut_no == 2:
    #                 serial_no = channel_settings["dut_b_serial_no"]

    #             else:
    #                 serial_no = ""

    #             username = self.context.app_state.current_user

    #             # self.csv_logger.start_cycle(
    #             #     test_name=test_name,
    #             #     dut_no=dut_no,
    #             #     cycle_no=current_cycle
    #             # )
    #             # self.csv_logger.start_cycle(
    #             #     dut_no=dut_no,
    #             #     cycle_no=current_cycle
    #             # )
    #             self.context.data_logger.start_cycle(
    #                 test_name=self.context.data_logger.test_name,
    #                 dut_no=dut_no,
    #                 cycle_no=current_cycle,
    #                 serial_number=serial_no,
    #                 user_name=username
    #             )

    #         print(
    #             f"========== "
    #             f"Cycle {current_cycle} "
    #             f"of {cycles} "
    #             f"=========="
    #         )
    #         remaining_cycles = cycles - current_cycle

    #         # channel_frame = (
    #         #     self.context
    #         #     .efficiency_trend_controller
    #         #     .view
    #         #     .channel_map[channel_id]
    #         # )

    #         # channel_frame.after(
    #         #     0,
    #         #     lambda c=cycle+1: channel_frame.set_cycle(c)
    #         # )

    #         print(f"========== Cycle {cycle + 1} of {cycles} ==========")

    #         # -------------------------
    #         # Charge
    #         # -------------------------
    #         print("Charging...")

    #         # adam_driver.set_charge_mode(channel_id)

    #         self.context.test_session.mode = "Charge"

    #         # self.wait_seconds(charge_time,channel_id)

    #         remaining = (
    #             (charge_time + rest1 + discharge_time + rest2 - charge_time)
    #             + remaining_cycles * cycle_time
    #         )

    #         result, cycle_elapsed = self.wait_seconds(
    #             charge_time,
    #             channel_id,
    #             current_cycle,
    #             cycles,
    #             remaining,
    #             cycle_elapsed,
    #             interval=interval
    #         )

    #         if result == "next_cycle":
    #             self.context.efficiency_trend_controller.discard_current_cycle(
    #                 running_duts
    #             )

    #             self.next_cycle_requested = False

    #             for dut_no in running_duts:

    #                 # self.csv_logger.close_cycle(
    #                 #     dut_no,
    #                 #     current_cycle
    #                 # )
    #                 self.context.data_logger.finish_cycle(
    #                                     dut_no=dut_no,
    #                                     cycle_no=current_cycle
    #                                 )

    #             continue

    #         # self.wait_seconds(
    #         #     charge_time,
    #         #     channel_id,
    #         #     current_cycle,
    #         #     cycles,
    #         #     remaining
    #         # )

    #         # if self.next_cycle_requested:

    #         #     self.next_cycle_requested = False

    #         #     continue
    #         if not self.context.app_state.test_running:
    #             break

    #         # -------------------------
    #         # Rest after Charge
    #         # -------------------------
    #         print("Rest 1")

    #         # adam_driver.output_off(channel_id)

    #         self.context.test_session.mode = "Rest"

    #         # self.wait_seconds(rest1,channel_id)

    #         remaining = (
    #             (rest1 + discharge_time + rest2 - rest1)
    #             + remaining_cycles * cycle_time
    #         )

    #         result, cycle_elapsed = self.wait_seconds(
    #             rest1,
    #             channel_id,
    #             current_cycle,
    #             cycles,
    #             remaining,
    #             cycle_elapsed,
    #             interval=interval
    #         )

    #         if result == "next_cycle":

    #             self.context.efficiency_trend_controller.discard_current_cycle(
    #                 running_duts
    #             )

    #             self.next_cycle_requested = False

    #             for dut_no in running_duts:

    #                 # self.csv_logger.close_cycle(
    #                 #     dut_no,
    #                 #     current_cycle
    #                 # )
    #                 self.context.data_logger.finish_cycle(
    #                                     dut_no=dut_no,
    #                                     cycle_no=current_cycle
    #                                 )
    #             continue
    #         # result = self.wait_seconds(
    #         #     rest1,
    #         #     channel_id,
    #         #     current_cycle,
    #         #     cycles,
    #         #     remaining
    #         # )

    #         # if result == "next_cycle":
    #         #     self.next_cycle_requested = False
    #         #     continue

    #         # self.wait_seconds(
    #         #     rest1,
    #         #     channel_id,
    #         #     current_cycle,
    #         #     cycles,
    #         #     remaining
    #         # )

            
    #         # if self.next_cycle_requested:

    #         #     self.next_cycle_requested = False

    #         #     continue

    #         if not self.context.app_state.test_running:
    #             break

    #         # -------------------------
    #         # Discharge
    #         # -------------------------

    #         print("Discharging...")

    #         # adam_driver.set_discharge_mode(channel_id)

    #         self.context.test_session.mode = "Discharge"

    #         # self.wait_seconds(discharge_time,channel_id)

    #         remaining = (
    #             (discharge_time + rest2 - discharge_time)
    #             + remaining_cycles * cycle_time
    #         )

    #         result, cycle_elapsed = self.wait_seconds(
    #             discharge_time,
    #             channel_id,
    #             current_cycle,
    #             cycles,
    #             remaining,
    #             cycle_elapsed,
    #             interval=interval
    #         )

    #         if result == "next_cycle":

    #             self.context.efficiency_trend_controller.discard_current_cycle(
    #                 running_duts
    #             )

    #             self.next_cycle_requested = False

    #             for dut_no in running_duts:

    #                 # self.csv_logger.close_cycle(
    #                 #     dut_no,
    #                 #     current_cycle
    #                 # )
    #                 self.context.data_logger.finish_cycle(
    #                                     dut_no=dut_no,
    #                                     cycle_no=current_cycle
    #                                 )

    #             continue
            

    #         # self.wait_seconds(
    #         #     discharge_time,
    #         #     channel_id,
    #         #     current_cycle,
    #         #     cycles,
    #         #     remaining
    #         # )

            
    #         # if self.next_cycle_requested:

    #         #     self.next_cycle_requested = False

    #         #     continue

    #         channel_settings = self.context.test_repository.get_channel_settings(channel_id)

    #         running_duts = []

    #         if channel_id == 1:
    #             if channel_settings["use_dut_a"]:
    #                 running_duts.append(1)

    #             if channel_settings["use_dut_b"]:
    #                 running_duts.append(2)

    #         elif channel_id == 2:
    #             if channel_settings["use_dut_a"]:
    #                 running_duts.append(3)

    #             if channel_settings["use_dut_b"]:
    #                 running_duts.append(4)

    #         # for dut_no in running_duts:
    #         #     self.context.efficiency_trend_controller.finish_cycle(dut_no)
    #         if not self.context.app_state.test_running:
    #             break

    #         # -------------------------
    #         # Rest after Discharge
    #         # -------------------------
    #         print("Rest 2")

    #         # adam_driver.output_off(channel_id)

    #         self.context.test_session.mode = "Rest"

    #         # 
    #         # self.wait_seconds(rest2,channel_id)

    #         remaining = remaining_cycles * cycle_time

    #         result, cycle_elapsed = self.wait_seconds(
    #             rest2,
    #             channel_id,
    #             current_cycle,
    #             cycles,
    #             remaining,
    #             cycle_elapsed,
    #             interval=interval
    #         )

    #         if result == "next_cycle":

    #             self.context.efficiency_trend_controller.discard_current_cycle(
    #                 running_duts
    #             )

    #             self.next_cycle_requested = False

    #             for dut_no in running_duts:

    #                 # self.csv_logger.close_cycle(
    #                 #     dut_no,
    #                 #     current_cycle
    #                 # )
    #                 self.context.data_logger.finish_cycle(
    #                                     dut_no=dut_no,
    #                                     cycle_no=current_cycle
    #                                 )

    #             continue
            

    #         # self.wait_seconds(
    #         #     rest2,
    #         #     channel_id,
    #         #     current_cycle,
    #         #     cycles,
    #         #     remaining
    #         # )

            
    #         # if self.next_cycle_requested:

    #         #     self.next_cycle_requested = False

    #         #     continue   

    #         for dut_no in running_duts:

    #             # self.csv_logger.close_cycle(
    #             #     dut_no,
    #             #     current_cycle
    #             # )

    #             self.context.data_logger.finish_cycle(
    #                 dut_no=dut_no,
    #                 cycle_no=current_cycle
    #             )

    #             self.context.efficiency_trend_controller.finish_cycle(
    #                 dut_no
    #             )
    #     if self.context.app_state.test_running:
    #         print("Endurance Test Completed")
    #         self.stop_test(channel_id)

    
    def run_endurance_cycle(
        self,
        channel_id,
        charge_time,
        discharge_time,
        rest1,
        rest2,
        cycles,
        interval
    ):
        print(
        f"Starting endurance test on channel {channel_id}"
        )

        self.channel_running[channel_id] = True
        self.update_global_test_state()
        # ==========================================================
        # INITIAL TEST STATE
        # ==========================================================

        cycle_time = (
            charge_time +
            rest1 +
            discharge_time +
            rest2
        )

        adam = self.context.instrument_manager.get_driver(Adam6052Driver)

        total_test_seconds = int(
            cycle_time * cycles * 60
        )

        self.channel_progress[channel_id] = {
            "current_cycle": 1,
            "total_cycles": cycles,
            "remaining_seconds": total_test_seconds,
            "end_time": time.time() + total_test_seconds,
            "running": True
        }

        # self.next_cycle_requested = False
        self.channel_next_cycle_requested[channel_id] = False

        print(
            f"""
    ==================================================
    ENDURANCE TEST STARTED
    ==================================================
    Channel          : {channel_id}
    Charge           : {charge_time} min
    Rest 1           : {rest1} min
    Discharge        : {discharge_time} min
    Rest 2           : {rest2} min
    Cycles           : {cycles}
    Logging interval : {interval} sec
    Total time       : {total_test_seconds} sec
    ==================================================
    """
        )

        try:

            # ======================================================
            # CYCLE LOOP
            # ======================================================

            for cycle in range(cycles):

                # --------------------------------------------------
                # TEST STOPPED
                # --------------------------------------------------

                # if not self.context.app_state.test_running:
                #     print("Endurance test stopped by user.")
                #     break

                if not self.channel_running.get(
                    channel_id,
                    False
                ):

                    print(
                        f"Endurance test stopped "
                        f"for channel {channel_id}."
                    )

                    break

                # --------------------------------------------------
                # CURRENT CYCLE
                # --------------------------------------------------

                current_cycle = cycle + 1

                self.channel_progress[channel_id][
                    "current_cycle"
                ] = current_cycle

                self.channel_progress[channel_id][
                    "running"
                ] = True

                # --------------------------------------------------
                # REMAINING TOTAL TEST TIME
                # --------------------------------------------------

                remaining_cycles = cycles - current_cycle

                # --------------------------------------------------
                # ACTIVE DUTs
                # --------------------------------------------------

                running_duts = self.get_running_duts(
                    channel_id
                )

                # --------------------------------------------------
                # CHANNEL SETTINGS
                # --------------------------------------------------

                channel_settings = (
                    self.context
                    .test_repository
                    .get_channel_settings(
                        channel_id
                    )
                )

                test_name = channel_settings["test_name"]

                print(
                    f"\n========== "
                    f"Cycle {current_cycle} "
                    f"of {cycles} "
                    f"=========="
                )

                # ==================================================
                # CREATE DATA LOGGER CYCLE
                # ==================================================

                for dut_no in running_duts:

                    if dut_no == 1:

                        serial_no = channel_settings[
                            "dut_a_serial_no"
                        ]

                    elif dut_no == 2:

                        serial_no = channel_settings[
                            "dut_b_serial_no"
                        ]

                    elif dut_no == 3:

                        serial_no = channel_settings[
                            "dut_a_serial_no"
                        ]

                    elif dut_no == 4:

                        serial_no = channel_settings[
                            "dut_b_serial_no"
                        ]

                    else:

                        serial_no = ""

                    username = (
                        self.context
                        .app_state
                        .current_user
                    )

                    self.context.data_logger.start_cycle(
                        test_name=self.context.data_logger.test_name,
                        dut_no=dut_no,
                        cycle_no=current_cycle,
                        serial_number=serial_no,
                        user_name=username
                    )

                # ==================================================
                # CYCLE ELAPSED
                # ==================================================

                cycle_elapsed = 0

                # ==================================================
                # CHARGE
                # ==================================================

                print("Charging...")

                # adam.set_charge_mode(channel_id)

                self.context.test_session.mode = "Charge"

                remaining = (
                    (rest1 +
                    discharge_time +
                    rest2)
                    +
                    remaining_cycles * cycle_time
                )

                result, cycle_elapsed = self.wait_seconds(
                    charge_time,
                    channel_id,
                    current_cycle,
                    cycles,
                    remaining,
                    cycle_elapsed,
                    interval
                )

                # --------------------------------------------------
                # STOPPED
                # --------------------------------------------------

                if result == "stopped":

                    break

                # --------------------------------------------------
                # NEXT CYCLE
                # --------------------------------------------------

                if result == "next_cycle":

                    self._finish_current_cycle(
                        running_duts,
                        current_cycle
                    )

                    # self.next_cycle_requested = False
                    self.channel_next_cycle_requested[channel_id] = False

                    continue

                # --------------------------------------------------
                # TEST STOPPED
                # --------------------------------------------------

                # if not self.context.app_state.test_running:

                #     break

                if not self.channel_running.get(
                    channel_id,
                    False
                ):

                    break

                # ==================================================
                # REST 1
                # ==================================================

                print("Rest 1")

                # adam.output_off(channel_id)

                self.context.test_session.mode = "Rest"

                remaining = (
                    (discharge_time +
                    rest2)
                    +
                    remaining_cycles * cycle_time
                )

                result, cycle_elapsed = self.wait_seconds(
                    rest1,
                    channel_id,
                    current_cycle,
                    cycles,
                    remaining,
                    cycle_elapsed,
                    interval
                )

                # --------------------------------------------------
                # STOPPED
                # --------------------------------------------------

                if result == "stopped":

                    break

                # --------------------------------------------------
                # NEXT CYCLE
                # --------------------------------------------------

                if result == "next_cycle":

                    self._finish_current_cycle(
                        running_duts,
                        current_cycle
                    )

                    # self.next_cycle_requested = False
                    self.channel_next_cycle_requested[channel_id] = False

                    continue

                # if not self.context.app_state.test_running:

                #     break

                if not self.channel_running.get(
                    channel_id,
                    False
                ):

                    break

                # ==================================================
                # DISCHARGE
                # ==================================================

                print("Discharging...")

                # adam.set_discharge_mode(channel_id)

                self.context.test_session.mode = "Discharge"

                remaining = (
                    rest2 +
                    remaining_cycles * cycle_time
                )

                result, cycle_elapsed = self.wait_seconds(
                    discharge_time,
                    channel_id,
                    current_cycle,
                    cycles,
                    remaining,
                    cycle_elapsed,
                    interval
                )

                # --------------------------------------------------
                # STOPPED
                # --------------------------------------------------

                if result == "stopped":

                    break

                # --------------------------------------------------
                # NEXT CYCLE
                # --------------------------------------------------

                if result == "next_cycle":

                    self._finish_current_cycle(
                        running_duts,
                        current_cycle
                    )

                    # self.next_cycle_requested = False
                    self.channel_next_cycle_requested[channel_id] = False

                    continue

                # if not self.context.app_state.test_running:

                #     break

                if not self.channel_running.get(
                    channel_id,
                    False
                ):

                    break

                # ==================================================
                # REST 2
                # ==================================================

                print("Rest 2")

                # adam.output_off(channel_id)

                self.context.test_session.mode = "Rest"

                remaining = (
                    remaining_cycles *
                    cycle_time
                )

                result, cycle_elapsed = self.wait_seconds(
                    rest2,
                    channel_id,
                    current_cycle,
                    cycles,
                    remaining,
                    cycle_elapsed,
                    interval
                )

                # --------------------------------------------------
                # STOPPED
                # --------------------------------------------------

                if result == "stopped":

                    break

                # --------------------------------------------------
                # NEXT CYCLE
                # --------------------------------------------------

                if result == "next_cycle":

                    self._finish_current_cycle(
                        running_duts,
                        current_cycle
                    )

                    # self.next_cycle_requested = False
                    self.channel_next_cycle_requested[channel_id] = False

                    continue

                # if not self.context.app_state.test_running:

                #     break

                if not self.channel_running.get(
                    channel_id,
                    False
                ):

                    break

                # ==================================================
                # FINISH CURRENT CYCLE
                # ==================================================

                self._finish_current_cycle(
                    running_duts,
                    current_cycle
                )

            # ======================================================
            # TEST FINISHED / STOPPED
            # ======================================================

            # if self.context.app_state.test_running:

            #     print(
            #         "\n=========================================="
            #     )
            #     print("Endurance Test Completed")
            #     print(
            #         "=========================================="
            #     )

            #     self.channel_progress[channel_id][
            #         "remaining_seconds"
            #     ] = 0

            #     self.channel_progress[channel_id][
            #         "running"
            #     ] = False

            #     self.channel_progress[channel_id][
            #         "end_time"
            #     ] = None

            #     self.stop_test(channel_id)

            # else:

            #     print(
            #         "Endurance test stopped."
            #     )

            #     self.channel_progress[channel_id][
            #         "remaining_seconds"
            #     ] = 0

            #     self.channel_progress[channel_id][
            #         "running"
            #     ] = False

            #     self.channel_progress[channel_id][
            #         "end_time"
            #     ] = None

            if self.channel_running.get(
                channel_id,
                False
            ):

                # ==================================================
                # NORMAL COMPLETION
                # ==================================================

                print(
                    "\n=========================================="
                )

                print(
                    f"Endurance Test Completed "
                    f"for Channel {channel_id}"
                )

                print(
                    "=========================================="
                )

                self.channel_progress[channel_id][
                    "remaining_seconds"
                ] = 0

                self.channel_progress[channel_id][
                    "running"
                ] = False

                self.channel_progress[channel_id][
                    "end_time"
                ] = None

                # Mark channel stopped
                self.channel_running[channel_id] = False

                # Update global status
                self.update_global_test_state()

                # Stop hardware / GUI
                self.stop_test(channel_id)

            else:

                # ==================================================
                # USER STOPPED CHANNEL
                # ==================================================

                print(
                    f"Endurance test stopped "
                    f"for Channel {channel_id}."
                )

                self.channel_progress[channel_id][
                    "remaining_seconds"
                ] = 0

                self.channel_progress[channel_id][
                    "running"
                ] = False

                self.channel_progress[channel_id][
                    "end_time"
                ] = None

                self.update_global_test_state()

        except Exception as e:

            print(
                f"Endurance cycle error: {e}"
            )

            self.channel_progress[channel_id][
                "running"
            ] = False

            self.channel_progress[channel_id][
                "end_time"
            ] = None

            raise

    
    def _finish_current_cycle(
        self,
        running_duts,
        current_cycle
    ):

        for dut_no in running_duts:

            self.context.data_logger.finish_cycle(
                dut_no=dut_no,
                cycle_no=current_cycle
            )

            self.context.efficiency_trend_controller.finish_cycle(
                dut_no
            )



    # def wait_seconds(
    #         self,
    #         step_minutes,
    #         channel_id,
    #         current_cycle,
    #         total_cycles,
    #         remaining_minutes_after_step
    # ):

    #     # channel_frame = (
    #     #     self.context
    #     #     .efficiency_trend_controller
    #     #     .view
    #     #     .channel_map[channel_id]
    #     # )

    #     # Show cycle
    #     # channel_frame.after(
    #     #     0,
    #     #     lambda: channel_frame.set_cycle(
    #     #         current_cycle,
    #     #         total_cycles
    #     #     )
    #     # )

    #     for frame in self.get_all_channel_frames(channel_id):

    #         frame.after(
    #             0,
    #             lambda f=frame:
    #                 f.set_cycle(
    #                     current_cycle,
    #                     total_cycles
    #                 )
    #         )

    #     # seconds = int(step_minutes * 60)
    #     # remaining_seconds_after_step = int(remaining_minutes_after_step * 60)

    #     # while seconds > 0:

    #     #     if not self.context.app_state.test_running:
    #     #         break

    #     #     total_remaining = seconds + remaining_seconds_after_step

    #     #     hrs = total_remaining // 3600
    #     #     mins = (total_remaining % 3600) // 60
    #     #     secs = total_remaining % 60

    #     #     channel_frame.after(
    #     #         0,
    #     #         lambda t=f"{hrs:02}:{mins:02}:{secs:02}":
    #     #         channel_frame.set_time_remaining(t)
    #     #     )

    #     #     time.sleep(1)

    #     #     seconds -= 1

    #     seconds = int(step_minutes * 60)
    #     remaining_seconds_after_step = int(remaining_minutes_after_step * 60)

    #     while seconds > 0:

    #         if not self.context.app_state.test_running:
    #             break

    #         total_remaining = seconds + remaining_seconds_after_step

    #         hrs = total_remaining // 3600
    #         mins = (total_remaining % 3600) // 60
    #         secs = total_remaining % 60

    #         text = f"{hrs:02}:{mins:02}:{secs:02}"

    #         for frame in self.get_all_channel_frames(channel_id):

    #             frame.after(
    #                 0,
    #                 lambda f=frame, t=text:
    #                     f.set_time_remaining(t)
    #             )

    #         time.sleep(1)

    #         seconds -= 1
    #     # for frame in self.get_all_channel_frames(channel_id):
    #     #     frame.after(
    #     #         0,
    #     #         lambda f=frame, t=text:
    #     #             f.set_time_remaining(t)
    #     #     )

    #     # channel_frame.after(
    #     #     0,
    #     #     lambda: channel_frame.set_time_remaining("00:00:00")
    #     # )

    #     for frame in self.get_all_channel_frames(channel_id):

    #         frame.after(
    #             0,
    #             lambda f=frame:
    #                 f.set_time_remaining("00:00:00")
    #         )

    # def wait_seconds(
    #             self,
    #             step_minutes,
    #             channel_id,
    #             current_cycle,
    #             total_cycles,
    #             remaining_minutes_after_step
    #     ):

    #         for frame in self.get_all_channel_frames(channel_id):

    #             frame.after(
    #                 0,
    #                 lambda f=frame:
    #                     f.set_cycle(
    #                         current_cycle,
    #                         total_cycles
    #                     )
    #             )

    #         seconds = int(step_minutes * 60)
    #         remaining_seconds_after_step = int(
    #             remaining_minutes_after_step * 60
    #         )

    #         while seconds > 0:

    #             # ==========================================
    #             # TEST STOPPED
    #             # ==========================================
    #             if not self.context.app_state.test_running:
    #                 break

    #             # ==========================================
    #             # WAIT IF ALARM HAS PAUSED THE TEST
    #             # ==========================================
    #             self.pause_event.wait()

    #             # ==========================================
    #             # USER SELECTED "NEXT CYCLE"
    #             # ==========================================
    #             if self.next_cycle_requested:
    #                 return "next_cycle"

    #             # ==========================================
    #             # UPDATE REMAINING TIME
    #             # ==========================================
    #             total_remaining = (
    #                 seconds +
    #                 remaining_seconds_after_step
    #             )

    #             hrs = total_remaining // 3600
    #             mins = (total_remaining % 3600) // 60
    #             secs = total_remaining % 60

    #             text = f"{hrs:02}:{mins:02}:{secs:02}"

    #             for frame in self.get_all_channel_frames(channel_id):

    #                 frame.after(
    #                     0,
    #                     lambda f=frame, t=text:
    #                         f.set_time_remaining(t)
    #                 )

    #             # ==========================================
    #             # WAIT ONE SECOND
    #             # ==========================================
    #             time.sleep(1)

    #             seconds -= 1

    #         # ==============================================
    #         # RESET TIMER
    #         # ==============================================
    #         for frame in self.get_all_channel_frames(channel_id):

    #             frame.after(
    #                 0,
    #                 lambda f=frame:
    #                     f.set_time_remaining("00:00:00")
    #             )

    #         return "completed"


    # def wait_seconds(
    #         self,
    #         step_minutes,
    #         channel_id,
    #         current_cycle,
    #         total_cycles,
    #         remaining_minutes_after_step,
    #         cycle_elapsed
    #     ):

    #         running_duts = self.get_running_duts(
    #             channel_id
    #         )

    #         for frame in self.get_all_channel_frames(
    #             channel_id
    #         ):

    #             frame.after(
    #                 0,
    #                 lambda f=frame:
    #                     f.set_cycle(
    #                         current_cycle,
    #                         total_cycles
    #                     )
    #             )

    #         seconds = int(
    #             step_minutes * 60
    #         )

    #         remaining_seconds_after_step = int(
    #             remaining_minutes_after_step * 60
    #         )

    #         # while seconds > 0:

    #         #     # ==================================================
    #         #     # TEST STOPPED
    #         #     # ==================================================

    #         #     if not self.context.app_state.test_running:
    #         #         break

    #         #     # ==================================================
    #         #     # ALARM PAUSE
    #         #     # ==================================================

    #         #     self.pause_event.wait()

    #         #     # ==================================================
    #         #     # NEXT CYCLE
    #         #     # ==================================================

    #         #     if self.next_cycle_requested:

    #         #         return (
    #         #             "next_cycle",
    #         #             cycle_elapsed
    #         #         )

    #         #     # ==================================================
    #         #     # CURRENT MODE
    #         #     # ==================================================

    #         #     mode = self.context.test_session.mode

    #         #     # ==================================================
    #         #     # GET LIVE CAN + HARDWARE DATA
    #         #     # ==================================================

    #         #     for dut_no in running_duts:

    #         #         can_values = (
    #         #             self.get_can_live_values(
    #         #                 dut_no
    #         #             )
    #         #         )

    #         #         hardware_values = (
    #         #             self.get_hardware_live_values(
    #         #                 dut_no
    #         #             )
    #         #         )

    #         #         # ==================================================
    #         #         # WRITE ONE ROW
    #         #         # ==================================================

    #         #         self.csv_logger.write_row(
    #         #             dut_no=dut_no,
    #         #             cycle_no=current_cycle,
    #         #             elapsed_seconds=cycle_elapsed,
    #         #             mode=mode,
    #         #             can_values=can_values,
    #         #             hardware_values=hardware_values
    #         #         )

    #         #     # ==================================================
    #         #     # UPDATE REMAINING TIME
    #         #     # ==================================================

    #         #     total_remaining = (
    #         #         seconds +
    #         #         remaining_seconds_after_step
    #         #     )

    #         #     hrs = total_remaining // 3600
    #         #     mins = (
    #         #         total_remaining % 3600
    #         #     ) // 60
    #         #     secs = (
    #         #         total_remaining % 60
    #         #     )

    #         #     text = (
    #         #         f"{hrs:02}:"
    #         #         f"{mins:02}:"
    #         #         f"{secs:02}"
    #         #     )

    #         #     for frame in self.get_all_channel_frames(
    #         #         channel_id
    #         #     ):

    #         #         frame.after(
    #         #             0,
    #         #             lambda f=frame, t=text:
    #         #                 f.set_time_remaining(t)
    #         #         )

    #         #     # ==================================================
    #         #     # ONE SECOND
    #         #     # ==================================================

    #         #     time.sleep(1)

    #         #     seconds -= 1

    #         while seconds > 0:

    #             # ==========================================
    #             # TEST STOPPED
    #             # ==========================================

    #             if not self.context.app_state.test_running:
    #                 break

    #             # ==========================================
    #             # WAIT IF ALARM HAS PAUSED THE TEST
    #             # ==========================================

    #             self.pause_event.wait()

    #             # ==========================================
    #             # NEXT CYCLE
    #             # ==========================================

    #             if self.next_cycle_requested:
    #                 return "next_cycle"

    #             # ==========================================
    #             # ELAPSED TIME
    #             # ==========================================

    #             elapsed_seconds = (
    #                 int(step_minutes * 60)
    #                 - seconds
    #             )

    #             # ==========================================
    #             # LOG CAN + HARDWARE
    #             # ==========================================

    #             self.log_live_values(
    #                 channel_id=channel_id,
    #                 cycle_no=current_cycle,
    #                 elapsed_seconds=elapsed_seconds
    #             )

    #             # ==========================================
    #             # UPDATE GUI TIMER
    #             # ==========================================

    #             total_remaining = (
    #                 seconds +
    #                 remaining_seconds_after_step
    #             )

    #             hrs = total_remaining // 3600
    #             mins = (total_remaining % 3600) // 60
    #             secs = total_remaining % 60

    #             text = (
    #                 f"{hrs:02}:"
    #                 f"{mins:02}:"
    #                 f"{secs:02}"
    #             )

    #             for frame in self.get_all_channel_frames(
    #                 channel_id
    #             ):

    #                 frame.after(
    #                     0,
    #                     lambda f=frame, t=text:
    #                         f.set_time_remaining(t)
    #                 )

    #             time.sleep(1)

    #             seconds -= 1

    #             cycle_elapsed += 1

    #         # ======================================================
    #         # RESET TIMER
    #         # ======================================================

    #         for frame in self.get_all_channel_frames(
    #             channel_id
    #         ):

    #             frame.after(
    #                 0,
    #                 lambda f=frame:
    #                     f.set_time_remaining(
    #                         "00:00:00"
    #                     )
    #             )

    #         return (
    #             "completed",
    #             cycle_elapsed
    #         )

    # def wait_seconds(
    #     self,
    #     step_minutes,
    #     channel_id,
    #     current_cycle,
    #     total_cycles,
    #     remaining_minutes_after_step,
    #     cycle_elapsed,
    #     interval
    # ):

    #     running_duts = self.get_running_duts(
    #         channel_id
    #     )

    #     # ======================================================
    #     # SAVE CURRENT CYCLE STATE
    #     # ======================================================

    #     self.channel_progress[channel_id]["current_cycle"] = current_cycle
    #     self.channel_progress[channel_id]["total_cycles"] = total_cycles
    #     self.channel_progress[channel_id]["running"] = True

    #     # ======================================================
    #     # UPDATE CYCLE DISPLAY
    #     # ======================================================

    #     # for frame in self.get_all_channel_frames(
    #     #     channel_id
    #     # ):

    #     #     frame.after(
    #     #         0,
    #     #         lambda f=frame,
    #     #             cycle=current_cycle,
    #     #             total=total_cycles:
    #     #             f.set_cycle(
    #     #                 cycle,
    #     #                 total
    #     #             )
    #     #     )

    #     live_table = self.get_live_table_frame()

    #     if live_table is not None:

    #         frame = live_table.get_channel_frame(
    #             channel_id
    #         )

    #         if frame is not None:

    #             frame.after(
    #                 0,
    #                 lambda f=frame,
    #                     cycle=current_cycle,
    #                     total=total_cycles:

    #                     f.set_cycle(
    #                         cycle,
    #                         total
    #                     )
    #             )

    #     seconds = int(
    #         step_minutes * 60
    #     )

    #     remaining_seconds_after_step = int(
    #         remaining_minutes_after_step * 60
    #     )

    #     # ======================================================
    #     # LOGGING INTERVAL
    #     # ======================================================

    #     interval = max(
    #         1,
    #         int(interval)
    #     )

    #     next_log_time = 0

    #     while seconds > 0:

    #         # ==============================================
    #         # TEST STOPPED
    #         # ==============================================

    #         if not self.context.app_state.test_running:

    #             self.channel_progress[channel_id]["running"] = False

    #             break

    #         # ==============================================
    #         # WAIT IF ALARM HAS PAUSED THE TEST
    #         # ==============================================

    #         self.pause_event.wait()

    #         # ==============================================
    #         # NEXT CYCLE
    #         # ==============================================

    #         if self.next_cycle_requested:

    #             return "next_cycle"

    #         # ==============================================
    #         # ELAPSED TIME
    #         # ==============================================

    #         elapsed_seconds = (
    #             int(step_minutes * 60)
    #             - seconds
    #         )

    #         # ==============================================
    #         # LOG ONLY AT USER INTERVAL
    #         # ==============================================

    #         if elapsed_seconds >= next_log_time:

    #             self.log_live_values(
    #                 channel_id=channel_id,
    #                 cycle_no=current_cycle,
    #                 elapsed_seconds=elapsed_seconds
    #             )

    #             next_log_time += interval

    #         # ==============================================
    #         # CALCULATE TOTAL REMAINING TIME
    #         # ==============================================

    #         # total_remaining = (
    #         #     seconds +
    #         #     remaining_seconds_after_step
    #         # )

    #         # # ==============================================
    #         # # SAVE CURRENT REMAINING TIME
    #         # # ==============================================

    #         # self.channel_progress[channel_id][
    #         #     "remaining_seconds"
    #         # ] = total_remaining

    #         # self.channel_progress[channel_id][
    #         #     "remaining_seconds"
    #         # ] = total_remaining

    #         now = time.time()

    #         end_time = self.channel_progress[
    #             channel_id
    #         ].get("end_time")

    #         if end_time is not None:

    #             total_remaining = max(
    #                 0,
    #                 int(end_time - now)
    #             )

    #         else:

    #             total_remaining = (
    #                 seconds +
    #                 remaining_seconds_after_step
    #             )

    #         self.channel_progress[channel_id][
    #             "remaining_seconds"
    #         ] = total_remaining

    #         # ==============================================
    #         # CONVERT TO HH:MM:SS
    #         # ==============================================

    #         hrs = total_remaining // 3600

    #         mins = (
    #             total_remaining % 3600
    #         ) // 60

    #         secs = (
    #             total_remaining % 60
    #         )

    #         text = (
    #             f"{hrs:02}:"
    #             f"{mins:02}:"
    #             f"{secs:02}"
    #         )

    #         # ==============================================
    #         # UPDATE GUI
    #         # ==============================================

    #         # for frame in self.get_all_channel_frames(
    #         #     channel_id
    #         # ):

    #         #     frame.after(
    #         #         0,
    #         #         lambda f=frame, t=text:
    #         #             f.set_time_remaining(t)
    #         #     )

    #         live_table = self.get_live_table_frame()

    #         if live_table is not None:

    #             frame = live_table.get_channel_frame(
    #                 channel_id
    #             )

    #             if frame is not None:

    #                 frame.after(
    #                     0,
    #                     lambda f=frame, t=text:
    #                         f.set_time_remaining(t)
    #                 )

    #         # ==============================================
    #         # ONE SECOND TIMER
    #         # ==============================================

    #         time.sleep(1)

    #         seconds -= 1

    #         cycle_elapsed += 1

    #     # ======================================================
    #     # RESET TIMER ONLY IF STEP COMPLETED
    #     # ======================================================

    #     if seconds <= 0:

    #         self.channel_progress[channel_id][
    #             "remaining_seconds"
    #         ] = remaining_seconds_after_step

    #         # for frame in self.get_all_channel_frames(
    #         #     channel_id
    #         # ):

    #         #     frame.after(
    #         #         0,
    #         #         lambda f=frame:
    #         #             f.set_time_remaining(
    #         #                 "00:00:00"
    #         #             )
    #         #     )

    #     return (
    #         "completed",
    #         cycle_elapsed
    #     )


    # def wait_seconds(
    #     self,
    #     step_minutes,
    #     channel_id,
    #     current_cycle,
    #     total_cycles,
    #     remaining_minutes_after_step,
    #     cycle_elapsed,
    #     interval
    # ):

    #     running_duts = self.get_running_duts(
    #         channel_id
    #     )

    #     # ---------------------------------------------
    #     # UPDATE CYCLE DISPLAY
    #     # ---------------------------------------------

    #     for frame in self.get_all_channel_frames(channel_id):

    #         try:
    #             frame.after(
    #                 0,
    #                 lambda f=frame:
    #                     f.set_cycle(
    #                         current_cycle,
    #                         total_cycles
    #                     )
    #             )
    #         except tk.TclError:
    #             pass

    #     seconds = int(
    #         step_minutes * 60
    #     )

    #     remaining_seconds_after_step = int(
    #         remaining_minutes_after_step * 60
    #     )

    #     interval = max(
    #         1,
    #         int(interval)
    #     )

    #     next_log_time = 0

    #     while seconds > 0:

    #         # ==========================================
    #         # TEST STOPPED
    #         # ==========================================

    #         if not self.context.app_state.test_running:

    #             self.channel_progress[channel_id]["running"] = False

    #             return (
    #                 "stopped",
    #                 cycle_elapsed
    #             )

    #         # ==========================================
    #         # WAIT IF ALARM PAUSED
    #         # ==========================================

    #         self.pause_event.wait()

    #         # ==========================================
    #         # NEXT CYCLE
    #         # ==========================================

    #         if self.next_cycle_requested:

    #             return (
    #                 "next_cycle",
    #                 cycle_elapsed
    #             )

    #         # ==========================================
    #         # ELAPSED TIME
    #         # ==========================================

    #         elapsed_seconds = (
    #             int(step_minutes * 60)
    #             - seconds
    #         )

    #         # ==========================================
    #         # REMAINING TIME
    #         # ==========================================

    #         total_remaining = (
    #             seconds +
    #             remaining_seconds_after_step
    #         )

    #         # IMPORTANT:
    #         # Store the current timer in shared state.
    #         # The GUI will read this even after logout/login.

    #         self.channel_progress[channel_id][
    #             "remaining_seconds"
    #         ] = total_remaining

    #         self.channel_progress[channel_id][
    #             "current_cycle"
    #         ] = current_cycle

    #         self.channel_progress[channel_id][
    #             "total_cycles"
    #         ] = total_cycles

    #         self.channel_progress[channel_id][
    #             "running"
    #         ] = True

    #         # ==========================================
    #         # LOGGING
    #         # ==========================================

    #         if elapsed_seconds >= next_log_time:

    #             self.log_live_values(
    #                 channel_id=channel_id,
    #                 cycle_no=current_cycle,
    #                 elapsed_seconds=elapsed_seconds
    #             )

    #             next_log_time += interval

    #         # ==========================================
    #         # GUI TIMER
    #         # ==========================================

    #         hrs = total_remaining // 3600

    #         mins = (
    #             total_remaining % 3600
    #         ) // 60

    #         secs = (
    #             total_remaining % 60
    #         )

    #         text = (
    #             f"{hrs:02}:"
    #             f"{mins:02}:"
    #             f"{secs:02}"
    #         )

    #         for frame in self.get_all_channel_frames(
    #             channel_id
    #         ):

    #             try:

    #                 if frame.winfo_exists():

    #                     frame.after(
    #                         0,
    #                         lambda f=frame, t=text:
    #                             f.set_time_remaining(t)
    #                     )

    #             except tk.TclError:

    #                 pass

    #         # ==========================================
    #         # ONE SECOND
    #         # ==========================================

    #         time.sleep(1)

    #         seconds -= 1

    #         cycle_elapsed += 1

    #     # ==========================================
    #     # STEP FINISHED
    #     # ==========================================

    #     self.channel_progress[channel_id][
    #         "remaining_seconds"
    #     ] = remaining_seconds_after_step

    #     # ==========================================
    #     # RESET GUI TIMER ONLY IF STEP IS COMPLETE
    #     # ==========================================

    #     for frame in self.get_all_channel_frames(
    #         channel_id
    #     ):

    #         try:

    #             if frame.winfo_exists():

    #                 frame.after(
    #                     0,
    #                     lambda f=frame:
    #                         f.set_time_remaining(
    #                             "00:00:00"
    #                         )
    #                 )

    #         except tk.TclError:

    #             pass

    #     return (
    #         "completed",
    #         cycle_elapsed
    #     )


    
    # def wait_seconds(
    #     self,
    #     step_minutes,
    #     channel_id,
    #     current_cycle,
    #     total_cycles,
    #     remaining_minutes_after_step,
    #     cycle_elapsed,
    #     interval
    # ):

    #     running_duts = self.get_running_duts(
    #         channel_id
    #     )

    #     # ======================================================
    #     # UPDATE CYCLE ON ALL CURRENTLY EXISTING FRAMES
    #     # ======================================================

    #     for frame in self.get_all_channel_frames(
    #         channel_id
    #     ):

    #         frame.after(
    #             0,
    #             lambda f=frame:
    #                 f.set_cycle(
    #                     current_cycle,
    #                     total_cycles
    #                 )
    #         )

    #     seconds = int(
    #         step_minutes * 60
    #     )

    #     remaining_seconds_after_step = int(
    #         remaining_minutes_after_step * 60
    #     )

    #     interval = max(
    #         1,
    #         int(interval)
    #     )

    #     next_log_time = 0

    #     # ======================================================
    #     # TIMER LOOP
    #     # ======================================================

    #     while seconds > 0:

    #         # --------------------------------------------------
    #         # TEST STOPPED
    #         # --------------------------------------------------

    #         if not self.context.app_state.test_running:

    #             self.channel_progress[
    #                 channel_id
    #             ]["running"] = False

    #             return (
    #                 "stopped",
    #                 cycle_elapsed
    #             )

    #         # --------------------------------------------------
    #         # ALARM PAUSE
    #         # --------------------------------------------------

    #         self.pause_event.wait()

    #         # --------------------------------------------------
    #         # NEXT CYCLE
    #         # --------------------------------------------------

    #         if self.next_cycle_requested:

    #             return (
    #                 "next_cycle",
    #                 cycle_elapsed
    #             )

    #         # --------------------------------------------------
    #         # ELAPSED TIME OF CURRENT STEP
    #         # --------------------------------------------------

    #         elapsed_seconds = (
    #             int(step_minutes * 60)
    #             - seconds
    #         )

    #         # --------------------------------------------------
    #         # UPDATE GLOBAL REMAINING TIME
    #         #
    #         # IMPORTANT:
    #         # This value is shared between the old and new GUI.
    #         # --------------------------------------------------

    #         progress = self.channel_progress[
    #             channel_id
    #         ]

    #         end_time = progress.get(
    #             "end_time"
    #         )

    #         if end_time is not None:

    #             remaining_total = max(
    #                 0,
    #                 int(
    #                     end_time -
    #                     time.time()
    #                 )
    #             )

    #         else:

    #             remaining_total = max(
    #                 0,
    #                 seconds +
    #                 remaining_seconds_after_step
    #             )

    #         progress[
    #             "remaining_seconds"
    #         ] = remaining_total

    #         progress[
    #             "current_cycle"
    #         ] = current_cycle

    #         progress[
    #             "total_cycles"
    #         ] = total_cycles

    #         progress[
    #             "running"
    #         ] = True

    #         # --------------------------------------------------
    #         # LOGGING
    #         # --------------------------------------------------

    #         if elapsed_seconds >= next_log_time:

    #             self.log_live_values(
    #                 channel_id=channel_id,
    #                 cycle_no=current_cycle,
    #                 elapsed_seconds=elapsed_seconds
    #             )

    #             next_log_time += interval

    #         # --------------------------------------------------
    #         # UPDATE CURRENT GUI
    #         # --------------------------------------------------

    #         hours = remaining_total // 3600

    #         minutes = (
    #             remaining_total % 3600
    #         ) // 60

    #         secs = (
    #             remaining_total % 60
    #         )

    #         text = (
    #             f"{hours:02}:"
    #             f"{minutes:02}:"
    #             f"{secs:02}"
    #         )

    #         for frame in self.get_all_channel_frames(
    #             channel_id
    #         ):

    #             try:

    #                 if frame.winfo_exists():

    #                     frame.after(
    #                         0,
    #                         lambda f=frame, t=text:
    #                             f.set_time_remaining(t)
    #                     )

    #             # except tk.TclError:
    #             except:
    #                 pass

    #         # --------------------------------------------------
    #         # ONE SECOND
    #         # --------------------------------------------------

    #         time.sleep(1)

    #         seconds -= 1

    #         cycle_elapsed += 1

    #     # ======================================================
    #     # STEP COMPLETED
    #     # ======================================================

    #     return (
    #         "completed",
    #         cycle_elapsed
    #     )

    def wait_seconds(
            self,
            step_minutes,
            channel_id,
            current_cycle,
            total_cycles,
            remaining_minutes_after_step,
            cycle_elapsed,
            interval
        ):

        running_duts = self.get_running_duts(channel_id)

        # ======================================================
        # UPDATE CYCLE ON ALL CURRENTLY EXISTING FRAMES
        # ======================================================

        for frame in self.get_all_channel_frames(channel_id):

            frame.after(
                0,
                lambda f=frame:
                    f.set_cycle(
                        current_cycle,
                        total_cycles
                    )
            )

        # ======================================================
        # STEP TIME
        # ======================================================

        step_seconds = max(
            0,
            int(step_minutes * 60)
        )

        remaining_seconds_after_step = max(
            0,
            int(remaining_minutes_after_step * 60)
        )

        interval = max(
            1,
            int(interval)
        )

        # ======================================================
        # USE REAL CLOCK
        # ======================================================

        step_start = time.monotonic()

        step_end = (
            step_start +
            step_seconds
        )

        # Used to keep track of alarm pause time
        pause_started = None

        next_log_time = 0

        # ======================================================
        # TIMER LOOP
        # ======================================================

        while True:

            # --------------------------------------------------
            # TEST STOPPED
            # --------------------------------------------------

            # if not self.context.app_state.test_running:

            #     self.channel_progress[
            #         channel_id
            #     ]["running"] = False

            #     return (
            #         "stopped",
            #         cycle_elapsed
            #     )


            if not self.channel_running.get(
                channel_id,
                False
            ):

                self.channel_progress[
                    channel_id
                ]["running"] = False

                return (
                    "stopped",
                    cycle_elapsed
                )
            # --------------------------------------------------
            # ALARM PAUSE
            # --------------------------------------------------

            # if not self.pause_event.is_set():

            #     # Start measuring pause duration
            #     if pause_started is None:

            #         pause_started = time.monotonic()

            #     # # Wait until alarm is cleared
            #     self.channel_pause_events[
            #         channel_id
            #     ].wait()
            #     # self.pause_event.wait()

            #     # Test was resumed
            #     pause_duration = (
            #         time.monotonic() -
            #         pause_started
            #     )

            #     # Extend step deadline by pause duration
            #     step_end += pause_duration

            #     pause_started = None

            channel_pause_event = (
                self.channel_pause_events[channel_id]
            )

            if not channel_pause_event.is_set():

                if pause_started is None:

                    pause_started = time.monotonic()

                # Wait until this channel is resumed
                channel_pause_event.wait()

                pause_duration = (
                    time.monotonic()
                    - pause_started
                )

                step_end += pause_duration

                pause_started = None

            # --------------------------------------------------
            # NEXT CYCLE
            # --------------------------------------------------

            # if self.next_cycle_requested:

            #     return (
            #         "next_cycle",
            #         cycle_elapsed
            #     )

            if self.channel_next_cycle_requested.get(channel_id, False):
                return "next_cycle", cycle_elapsed

            # --------------------------------------------------
            # ACTUAL ELAPSED TIME
            # --------------------------------------------------

            now = time.monotonic()

            elapsed_seconds = max(
                0,
                int(
                    now - step_start
                )
            )

            # --------------------------------------------------
            # STEP COMPLETE
            # --------------------------------------------------

            if now >= step_end:

                # Make sure elapsed time is exactly
                # the allocated step duration
                elapsed_seconds = step_seconds

                cycle_elapsed += max(
                    0,
                    step_seconds - cycle_elapsed
                )

                break

            # --------------------------------------------------
            # GLOBAL REMAINING TIME
            # --------------------------------------------------

            progress = self.channel_progress[
                channel_id
            ]

            end_time = progress.get(
                "end_time"
            )

            if end_time is not None:

                remaining_total = max(
                    0,
                    int(
                        end_time -
                        time.time()
                    )
                )

            else:

                step_remaining = max(
                    0,
                    int(
                        step_end -
                        now
                    )
                )

                remaining_total = (
                    step_remaining +
                    remaining_seconds_after_step
                )

            progress[
                "remaining_seconds"
            ] = remaining_total

            progress[
                "current_cycle"
            ] = current_cycle

            progress[
                "total_cycles"
            ] = total_cycles

            progress[
                "running"
            ] = True

            # --------------------------------------------------
            # LOGGING
            # --------------------------------------------------

            if elapsed_seconds >= next_log_time:

                self.log_live_values(
                    channel_id=channel_id,
                    cycle_no=current_cycle,
                    elapsed_seconds=cycle_elapsed
                )

                next_log_time += interval

            # --------------------------------------------------
            # UPDATE GUI
            # --------------------------------------------------

            hours = remaining_total // 3600

            minutes = (
                remaining_total % 3600
            ) // 60

            secs = (
                remaining_total % 60
            )

            text = (
                f"{hours:02}:"
                f"{minutes:02}:"
                f"{secs:02}"
            )

            for frame in self.get_all_channel_frames(
                channel_id
            ):

                try:

                    if frame.winfo_exists():

                        frame.after(
                            0,
                            lambda f=frame, t=text:
                                f.set_time_remaining(t)
                        )

                except Exception:
                    pass

            # --------------------------------------------------
            # SLEEP ONLY UNTIL NEXT 1-SECOND UPDATE
            # --------------------------------------------------

            remaining_step = (
                step_end -
                time.monotonic()
            )

            sleep_time = min(
                1.0,
                max(0.01, remaining_step)
            )

            time.sleep(sleep_time)

        # ======================================================
        # STEP COMPLETED
        # ======================================================

        cycle_elapsed += step_seconds

        return (
            "completed",
            cycle_elapsed
        )

    def get_live_table_frame(self):

        return getattr(
            self.context,
            "live_table_frame",
            None
        )


    # def wait_seconds(
    #     self,
    #     step_minutes,
    #     channel_id,
    #     current_cycle,
    #     total_cycles,
    #     remaining_minutes_after_step,
    #     cycle_elapsed,
    #     interval
    # ):

    #     running_duts = self.get_running_duts(
    #         channel_id
    #     )

    #     for frame in self.get_all_channel_frames(
    #         channel_id
    #     ):

    #         frame.after(
    #             0,
    #             lambda f=frame:
    #                 f.set_cycle(
    #                     current_cycle,
    #                     total_cycles
    #                 )
    #         )

    #     seconds = int(
    #         step_minutes * 60
    #     )

    #     remaining_seconds_after_step = int(
    #         remaining_minutes_after_step * 60
    #     )

    #     self.channel_progress[channel_id]["remaining_seconds"] = remaining_seconds_after_step
    #     # ======================================================
    #     # LOGGING INTERVAL
    #     # ======================================================

    #     interval = max(
    #         1,
    #         int(interval)
    #     )

    #     next_log_time = 0

    #     while seconds > 0:

    #         # ==============================================
    #         # TEST STOPPED
    #         # ==============================================

    #         if not self.context.app_state.test_running:
    #             break

    #         # ==============================================
    #         # WAIT IF ALARM HAS PAUSED THE TEST
    #         # ==============================================

    #         self.pause_event.wait()

    #         # ==============================================
    #         # NEXT CYCLE
    #         # ==============================================

    #         if self.next_cycle_requested:

    #             return "next_cycle"

    #         # ==============================================
    #         # ELAPSED TIME
    #         # ==============================================

    #         elapsed_seconds = (
    #             int(step_minutes * 60)
    #             - seconds
    #         )

    #         # ==============================================
    #         # LOG ONLY AT USER INTERVAL
    #         # ==============================================

    #         if elapsed_seconds >= next_log_time:

    #             self.log_live_values(
    #                 channel_id=channel_id,
    #                 cycle_no=current_cycle,
    #                 elapsed_seconds=elapsed_seconds
    #             )

    #             next_log_time += interval

    #         # ==============================================
    #         # UPDATE GUI TIMER
    #         # ==============================================

    #         total_remaining = (
    #             seconds +
    #             remaining_seconds_after_step
    #         )

    #         hrs = total_remaining // 3600

    #         mins = (
    #             total_remaining % 3600
    #         ) // 60

    #         secs = (
    #             total_remaining % 60
    #         )

    #         text = (
    #             f"{hrs:02}:"
    #             f"{mins:02}:"
    #             f"{secs:02}"
    #         )

    #         for frame in self.get_all_channel_frames(
    #             channel_id
    #         ):

    #             frame.after(
    #                 0,
    #                 lambda f=frame, t=text:
    #                     f.set_time_remaining(t)
    #             )

    #         # ==============================================
    #         # ONE SECOND TIMER
    #         # ==============================================

    #         time.sleep(1)

    #         seconds -= 1

    #         cycle_elapsed += 1

    #     # ======================================================
    #     # RESET TIMER
    #     # ======================================================

    #     for frame in self.get_all_channel_frames(
    #         channel_id
    #     ):

    #         frame.after(
    #             0,
    #             lambda f=frame:
    #                 f.set_time_remaining(
    #                     "00:00:00"
    #                 )
    #         )

    #     return (
    #         "completed",
    #         cycle_elapsed
    #     )
    
    # def get_all_channel_frames(self, channel_id):

    #     frames = []

    #     if hasattr(self.context, "efficiency_trend_controller"):
    #         frames.append(
    #             self.context.efficiency_trend_controller
    #             .view
    #             .get_channel_frame(channel_id)
    #         )

    #     if hasattr(self.context, "live_table_controller"):
    #         frames.append(
    #             self.context.live_table_controller
    #             .view
    #             .get_channel_frame(channel_id)
    #         )

    #     if hasattr(self.context, "live_temp_controller"):
    #         frames.append(
    #             self.context.live_temp_controller
    #             .view
    #             .get_channel_frame(channel_id)
    #         )

    #     return frames

    def get_all_channel_frames(self, channel_id):

        frames = []

        # =====================================================
        # CURRENT LIVE TABLE
        # =====================================================

        live_table = getattr(
            self.context,
            "live_table_frame",
            None
        )

        if live_table is not None:

            try:

                frame = live_table.get_channel_frame(
                    channel_id
                )

                if frame is not None and frame.winfo_exists():
                    frames.append(frame)

            except Exception as e:

                print(
                    f"LiveTable frame unavailable: {e}"
                )

        # =====================================================
        # EFFICIENCY TREND
        # =====================================================

        efficiency_controller = getattr(
            self.context,
            "efficiency_trend_controller",
            None
        )

        if efficiency_controller is not None:

            try:

                view = getattr(
                    efficiency_controller,
                    "view",
                    None
                )

                if view is not None:

                    frame = view.get_channel_frame(
                        channel_id
                    )

                    if frame is not None and frame.winfo_exists():
                        frames.append(frame)

            except Exception as e:

                print(
                    f"Efficiency frame unavailable: {e}"
                )

        # =====================================================
        # LIVE TEMPERATURE
        # =====================================================

        temp_controller = getattr(
            self.context,
            "live_temp_controller",
            None
        )

        if temp_controller is not None:

            try:

                view = getattr(
                    temp_controller,
                    "view",
                    None
                )

                if view is not None:

                    frame = view.get_channel_frame(
                        channel_id
                    )

                    if frame is not None and frame.winfo_exists():
                        frames.append(frame)

            except Exception as e:

                print(
                    f"Temperature frame unavailable: {e}"
                )

        return frames

    def discard_current_cycle(self, dut_list):

        for dut in dut_list:

            data = self.cycle_data[dut]

            data["charging_samples"].clear()
            data["discharging_samples"].clear()

            print(
                f"Discarded samples for DUT {dut}"
            )

    def get_dut_mode_for_channel(
            self,
            channel_id,
            dut_no,
            channel_mode
        ):

            if channel_mode == "Rest":
                return "Rest"

            if channel_id == 1:

                if dut_no == 1:

                    return channel_mode

                elif dut_no == 2:

                    if channel_mode == "Charge":
                        return "Discharge"

                    elif channel_mode == "Discharge":
                        return "Charge"

            elif channel_id == 2:

                if dut_no == 3:

                    return channel_mode

                elif dut_no == 4:

                    if channel_mode == "Charge":
                        return "Discharge"

                    elif channel_mode == "Discharge":
                        return "Charge"

            return "Rest"

    def log_live_values(
        self,
        channel_id,
        cycle_no,
        elapsed_seconds
        ):

        # ==========================================================
        # GET DUTs FOR THIS CHANNEL
        # ==========================================================

        if channel_id == 1:
            running_duts = [1, 2]
        else:
            running_duts = [3, 4]

        # ==========================================================
        # GET CURRENT CHANNEL MODE
        #
        # This is the mode controlled by the endurance cycle:
        # Charge / Discharge / Rest
        # ==========================================================

        channel_mode = self.context.test_session.mode

        print(
            f"\n========== CHANNEL {channel_id} =========="
        )

        print(
            "Channel Mode :",
            channel_mode
        )

        # ==========================================================
        # LOG EACH DUT
        # ==========================================================

        for dut_no in running_duts:

            # ======================================================
            # DETERMINE DUT-SPECIFIC MODE
            #
            # Channel 1:
            #   DUT1 Charge  -> DUT2 Discharge
            #   DUT1 Discharge -> DUT2 Charge
            #
            # Channel 2:
            #   DUT3 Charge  -> DUT4 Discharge
            #   DUT3 Discharge -> DUT4 Charge
            #
            # Rest:
            #   Both DUTs Rest
            # ======================================================

            mode = self.get_dut_mode_for_channel(
                channel_id=channel_id,
                dut_no=dut_no,
                channel_mode=channel_mode
            )

            # ======================================================
            # GET LIVE CAN DATA
            # ======================================================

            can_values = self.get_can_live_values(
                dut_no
            )

            # ======================================================
            # GET LIVE HARDWARE DATA
            # ======================================================

            hardware_values = self.get_hardware_live_values(
                dut_no
            )

            # ======================================================
            # DEBUG
            # ======================================================

            # print(
            #     f"\n========== LOG DUT{dut_no} =========="
            # )

            # print(
            #     "Mode     :",
            #     mode
            # )

            # print(
            #     "CAN      :",
            #     can_values
            # )

            # print(
            #     "Hardware :",
            #     hardware_values
            # )

            # ======================================================
            # CSV
            # ======================================================

            # if self.csv_logger:

            #     self.csv_logger.write_row(
            #         dut_no=dut_no,
            #         cycle_no=cycle_no,
            #         elapsed_seconds=elapsed_seconds,
            #         mode=mode,
            #         can_values=can_values,
            #         hardware_values=hardware_values
            #     )

            # ======================================================
            # EXCEL
            # ======================================================

            if self.context.data_logger:

                self.context.data_logger.log_data(
                    dut_no=dut_no,
                    cycle_no=cycle_no,
                    mode=mode,
                    can_values=can_values,
                    hardware_values=hardware_values,
                    time_sec=elapsed_seconds
                )

    def update_global_test_state(self):

        self.context.app_state.test_running = any(
            self.channel_running.values()
        )

        return self.context.app_state.test_running

                
    # def log_live_values(
    #         self,
    #         channel_id,
    #         cycle_no,
    #         elapsed_seconds
    #     ):

    #         # ==========================================================
    #         # GET DUTs FOR THIS CHANNEL
    #         # ==========================================================

    #         if channel_id == 1:
    #             running_duts = [1, 2]
    #         else:
    #             running_duts = [3, 4]

    #         # ==========================================================
    #         # LOG EACH DUT
    #         # ==========================================================

    #         for dut_no in running_duts:

    #             # ======================================================
    #             # GET DUT-SPECIFIC MODE
    #             # ======================================================

    #             mode = self.get_dut_mode_for_channel(
    #                 channel_id=channel_id,
    #                 dut_no=dut_no,
    #                 channel_mode=channel_mode
    #             )

    #             # ======================================================
    #             # GET LIVE CAN DATA
    #             # ======================================================

    #             can_values = self.get_can_live_values(
    #                 dut_no
    #             )

    #             # ======================================================
    #             # GET LIVE HARDWARE DATA
    #             # ======================================================

    #             hardware_values = self.get_hardware_live_values(
    #                 dut_no
    #             )

    #             # ======================================================
    #             # DEBUG
    #             # ======================================================

    #             print(
    #                 f"\n========== LOG DUT{dut_no} =========="
    #             )

    #             print(
    #                 "Mode     :",
    #                 mode
    #             )

    #             print(
    #                 "CAN      :",
    #                 can_values
    #             )

    #             print(
    #                 "Hardware :",
    #                 hardware_values
    #             )

    #             # ======================================================
    #             # CSV
    #             # ======================================================

    #             if self.csv_logger:

    #                 self.csv_logger.write_row(
    #                     dut_no=dut_no,
    #                     cycle_no=cycle_no,
    #                     elapsed_seconds=elapsed_seconds,
    #                     mode=mode,
    #                     can_values=can_values,
    #                     hardware_values=hardware_values
    #                 )

    #             # ======================================================
    #             # EXCEL
    #             # ======================================================

    #             if self.excel_logger:

    #                 self.excel_logger.write_row(
    #                     dut_no=dut_no,
    #                     cycle_no=cycle_no,
    #                     elapsed_seconds=elapsed_seconds,
    #                     mode=mode,
    #                     can_values=can_values,
    #                     hardware_values=hardware_values
    #                 )

    # def log_live_values(
    #         self,
    #         channel_id,
    #         cycle_no,
    #         elapsed_seconds
    #     ):

    #         channel_settings = (
    #             self.context.test_repository
    #             .get_channel_settings(channel_id)
    #         )

    #         active_duts = []

    #         if channel_id == 1:

    #             if channel_settings["use_dut_a"]:
    #                 active_duts.append(1)

    #             if channel_settings["use_dut_b"]:
    #                 active_duts.append(2)

    #         elif channel_id == 2:

    #             if channel_settings["use_dut_a"]:
    #                 active_duts.append(3)

    #             if channel_settings["use_dut_b"]:
    #                 active_duts.append(4)

    #         # ------------------------------------------------------
    #         # Channel mode
    #         # ------------------------------------------------------

    #         channel_mode = self.context.test_session.mode

    #         # ------------------------------------------------------
    #         # Each DUT
    #         # ------------------------------------------------------

    #         for dut_no in active_duts:

    #             dut_mode = self.get_dut_mode_for_channel(
    #                 channel_id,
    #                 dut_no,
    #                 channel_mode
    #             )

    #             # ==================================================
    #             # CAN VALUES
    #             # ==================================================

    #             can_values = {}

    #             # Determine CAN port
    #             port = {
    #                 1: "PCAN_USBBUS1",
    #                 2: "PCAN_USBBUS2",
    #                 3: "PCAN_USBBUS3",
    #                 4: "PCAN_USBBUS4"
    #             }.get(dut_no)

    #             if port:

    #                 channel_can = (
    #                     self.context.can_values
    #                     .get(channel_id, {})
    #                 )

    #                 can_values = (
    #                     channel_can
    #                     .get(port, {})
    #                     .copy()
    #                 )

    #             # ==================================================
    #             # HARDWARE VALUES
    #             # ==================================================

    #             hardware_values = (
    #                 self.context.hardware_values
    #                 .get(dut_no, {})
    #                 .copy()
    #             )

    #             # ==================================================
    #             # LOG
    #             # ==================================================

    #             self.context.data_logger.log_data(
    #                 dut_no=dut_no,
    #                 cycle_no=cycle_no,
    #                 mode=dut_mode,
    #                 can_values=can_values,
    #                 hardware_values=hardware_values,
    #                 time_sec=elapsed_seconds
    #             )
    

    # def wait_seconds(self, min):

    #     end_time = time.time() + (min * 60)

    #     while time.time() < end_time:

    #         if not self.context.app_state.test_running:
    #             break

    #         time.sleep(0.5)


    # def wait_seconds(self, min, channel_id):

    #     channel_frame = (
    #         self.context
    #         .efficiency_trend_controller
    #         .view
    #         .channel_map[channel_id]
    #     )
    #     seconds=min*60
    #     while seconds > 0:

    #         if not self.context.app_state.test_running:
    #             break

    #         hrs = seconds // 3600
    #         mins = (seconds % 3600) // 60
    #         secs = seconds % 60

    #         text = f"{hrs:02}:{mins:02}:{secs:02}"

    #         channel_frame.after(
    #             0,
    #             lambda t=text: channel_frame.set_time_remaining(t)
    #         )

    #         time.sleep(1)

    #         seconds -= 1

    #     channel_frame.after(
    #         0,
    #         lambda: channel_frame.set_time_remaining("00:00:00")
    #     )

    # def wait_seconds(self, minutes, channel_id, total_seconds_remaining):

    #     channel_frame = (
    #         self.context
    #         .efficiency_trend_controller
    #         .view
    #         .channel_map[channel_id]
    #     )

    #     step_seconds = int(minutes * 60)

    #     while step_seconds > 0:

    #         if not self.context.app_state.test_running:
    #             break

    #         hrs = total_seconds_remaining // 3600
    #         mins = (total_seconds_remaining % 3600) // 60
    #         secs = total_seconds_remaining % 60

    #         text = f"{hrs:02}:{mins:02}:{secs:02}"

    #         channel_frame.after(
    #             0,
    #             lambda t=text: channel_frame.set_time_remaining(t)
    #         )

    #         time.sleep(1)

    #         step_seconds -= 1
    #         total_seconds_remaining -= 1

    #     return total_seconds_remaining