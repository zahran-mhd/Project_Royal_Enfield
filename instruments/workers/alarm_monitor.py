import threading
import time
from instruments.dbc_decoder import WATCH_PARAMETERS

import threading
import time


class AlarmMonitor:

    def __init__(self, context):

        self.context = context

        self.running = False
        self.thread = None

        # -----------------------------------------
        # Currently active alarms
        # {
        #     channel_id: {
        #         (dut_id, parameter),
        #         ...
        #     }
        # }
        # -----------------------------------------

        self.active_alarms = {
            1: set(),
            2: set()
        }

        # -----------------------------------------
        # Alarm controller
        # -----------------------------------------

        self.alarm_controller = (
            self.context.alarm_controller
        )

        # -----------------------------------------
        # CAN alarm parameters
        #
        # These are the parameters that CAN can
        # report. Enabled/disabled state comes
        # from AlarmSettings database.
        # -----------------------------------------

        self.alarm_parameters = WATCH_PARAMETERS[0x50E]

        # -----------------------------------------
        # CAN bus -> DUT mapping
        # -----------------------------------------

        self.bus_to_dut = {
            "PCAN_USBBUS1": 1,
            "PCAN_USBBUS2": 2,
            "PCAN_USBBUS3": 3,
            "PCAN_USBBUS4": 4,
        }

    # =================================================
    # START
    # =================================================

    def start(self):

        if self.running:
            return

        self.running = True

        self.thread = threading.Thread(
            target=self.monitor,
            daemon=True
        )

        self.thread.start()

        print("Alarm Monitor Started")

    # =================================================
    # STOP
    # =================================================

    def stop(self):

        self.running = False

        if self.thread:

            self.thread.join(
                timeout=1
            )

        self.thread = None

        # Clear active alarms
        for channel_id in self.active_alarms:
            self.active_alarms[channel_id].clear()

        print("Alarm Monitor Stopped")

    # =================================================
    # GET ENABLED ALARMS
    # =================================================

    def get_enabled_alarm_names(self):

        """
        Get alarms enabled by the user from the
        AlarmSettings table through the controller.

        Returns:
            set of alarm names
        """

        alarms = (
            self.alarm_controller.get_enabled_alarms()
        )

        return {
            alarm["alarm_name"]
            for alarm in alarms
        }

    # =================================================
    # MONITOR
    # =================================================

    def monitor(self):

        while self.running:

            try:

                test_controller = (
                    self.context.test_controller
                )

                # =====================================
                # GET ENABLED ALARMS
                # =====================================

                enabled_alarms = (
                    self.get_enabled_alarm_names()
                )

                # =====================================
                # CAN VALUES
                # =====================================

                can_values = getattr(
                    self.context,
                    "can_values",
                    {}
                )

                # =====================================
                # CHECK EACH CHANNEL INDEPENDENTLY
                # =====================================

                for channel_id in [1, 2]:

                    # ---------------------------------
                    # IS CHANNEL RUNNING?
                    # ---------------------------------

                    if not test_controller.channel_running.get(
                        channel_id,
                        False
                    ):

                        self.active_alarms[
                            channel_id
                        ].clear()

                        continue

                    # ---------------------------------
                    # CURRENT ALARMS
                    # ---------------------------------

                    current_alarms = set()

                    buses = can_values.get(
                        channel_id,
                        {}
                    )

                    # ---------------------------------
                    # CHECK BUSES
                    # ---------------------------------

                    for bus_name, values in buses.items():

                        dut_id = self.bus_to_dut.get(
                            bus_name
                        )

                        if dut_id is None:
                            continue

                        # -----------------------------
                        # CHECK ALARM PARAMETERS
                        # -----------------------------

                        for parameter in self.alarm_parameters:

                            # ---------------------------------
                            # USER ENABLED CHECK
                            # ---------------------------------

                            if parameter not in enabled_alarms:
                                continue

                            value = values.get(
                                parameter,
                                "No Error"
                            )

                            # ---------------------------------
                            # ALARM DETECTED
                            # ---------------------------------

                            if value == "ERROR":

                                key = (
                                    dut_id,
                                    parameter
                                )

                                current_alarms.add(
                                    key
                                )

                    # =================================
                    # FIND NEW ALARMS
                    # =================================

                    new_alarms = (
                        current_alarms
                        -
                        self.active_alarms[channel_id]
                    )

                    # =================================
                    # UPDATE ACTIVE ALARMS
                    # =================================

                    self.active_alarms[
                        channel_id
                    ] = current_alarms

                    # =================================
                    # SHOW POPUP
                    # =================================

                    if new_alarms:

                        alarms = []

                        for dut_id, parameter in sorted(
                            new_alarms
                        ):

                            alarms.append({
                                "dut_id": dut_id,
                                "parameter": parameter
                            })

                            print(
                                f"ALARM DETECTED: "
                                f"Channel {channel_id} - "
                                f"DUT {dut_id} - "
                                f"{parameter}"
                            )

                        # -----------------------------
                        # PASS CHANNEL ID
                        # -----------------------------

                        test_controller.raise_alarm(
                            channel_id,
                            alarms
                        )

            except Exception as e:

                print(
                    f"Alarm Monitor Error: {e}"
                )

            time.sleep(0.1)

# import threading
# import time


# class AlarmMonitor:

#     def __init__(self, context):

#         self.context = context

#         self.running = False
#         self.thread = None

#         # -----------------------------------------
#         # Currently active alarms
#         # {(dut_id, parameter), ...}
#         # -----------------------------------------

#         # self.active_alarms = set()

#         self.active_alarms = {
#             1: set(),
#             2: set()
#         }

#         self.alarm_parameters = WATCH_PARAMETERS[0x50E]

#         self.bus_to_dut = {
#             "PCAN_USBBUS1": 1,
#             "PCAN_USBBUS2": 2,
#             "PCAN_USBBUS3": 3,
#             "PCAN_USBBUS4": 4,
#         }

#     # =================================================
#     # START
#     # =================================================

#     def start(self):

#         if self.running:
#             return

#         self.running = True

#         self.thread = threading.Thread(
#             target=self.monitor,
#             daemon=True
#         )

#         self.thread.start()

#         print("Alarm Monitor Started")

#     # =================================================
#     # STOP
#     # =================================================

#     def stop(self):

#         self.running = False

#         if self.thread:

#             self.thread.join(
#                 timeout=1
#             )

#         self.thread = None

#         # self.active_alarms.clear()
#         for channel_id in self.active_alarms:
#             self.active_alarms[channel_id].clear()

#         print("Alarm Monitor Stopped")

#     # =================================================
#     # MONITOR
#     # =================================================


#     def monitor(self):

#         while self.running:

#             test_controller = self.context.test_controller

#             # =========================================
#             # CAN VALUES
#             # =========================================

#             can_values = getattr(
#                 self.context,
#                 "can_values",
#                 {}
#             )

#             # =========================================
#             # CHECK EACH CHANNEL INDEPENDENTLY
#             # =========================================

#             for channel_id in [1, 2]:

#                 # -------------------------------------
#                 # IS THIS CHANNEL RUNNING?
#                 # -------------------------------------

#                 if not test_controller.channel_running.get(
#                     channel_id,
#                     False
#                 ):

#                     # Clear alarms for stopped channel
#                     self.active_alarms[
#                         channel_id
#                     ].clear()

#                     continue

#                 # -------------------------------------
#                 # CURRENT ALARMS FOR THIS CHANNEL
#                 # -------------------------------------

#                 current_alarms = set()

#                 buses = can_values.get(
#                     channel_id,
#                     {}
#                 )

#                 # -------------------------------------
#                 # CHECK BUSES
#                 # -------------------------------------

#                 for bus_name, values in buses.items():

#                     dut_id = self.bus_to_dut.get(
#                         bus_name
#                     )

#                     if dut_id is None:
#                         continue

#                     # ---------------------------------
#                     # CHECK ALARM PARAMETERS
#                     # ---------------------------------

#                     for parameter in self.alarm_parameters:

#                         value = values.get(
#                             parameter,
#                             "No Error"
#                         )

#                         if value == "ERROR":

#                             key = (
#                                 dut_id,
#                                 parameter
#                             )

#                             current_alarms.add(
#                                 key
#                             )

#                 # =====================================
#                 # FIND NEW ALARMS FOR THIS CHANNEL
#                 # =====================================

#                 new_alarms = (
#                     current_alarms
#                     -
#                     self.active_alarms[channel_id]
#                 )

#                 # =====================================
#                 # UPDATE ACTIVE ALARMS
#                 # =====================================

#                 self.active_alarms[
#                     channel_id
#                 ] = current_alarms

#                 # =====================================
#                 # SHOW POPUP
#                 # =====================================

#                 if new_alarms:

#                     alarms = []

#                     for dut_id, parameter in sorted(
#                         new_alarms
#                     ):

#                         alarms.append({
#                             "dut_id": dut_id,
#                             "parameter": parameter
#                         })

#                         print(
#                             f"ALARM DETECTED: "
#                             f"Channel {channel_id} - "
#                             f"DUT {dut_id} - "
#                             f"{parameter}"
#                         )

#                     # ---------------------------------
#                     # PASS CHANNEL ID
#                     # ---------------------------------

#                     test_controller.raise_alarm(
#                         channel_id,
#                         alarms
#                     )

#             time.sleep(0.1)

    