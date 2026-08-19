import threading
import time
from instruments.dbc_decoder import WATCH_PARAMETERS


# class AlarmMonitor:

#     def __init__(self, context):
#         self.context = context
#         self.running = False
#         self.thread = None
#         # Prevent the same alarm from repeatedly
#         # opening popup while the bit remains 1
#         self.active_alarms = set()

#         self.alarm_parameters = WATCH_PARAMETERS[0x50E]

#     def start(self):
#         if self.running:
#             return

#         self.running = True

#         self.thread = threading.Thread(
#             target=self.monitor,
#             daemon=True
#         )

#         self.thread.start()

#     def stop(self):
#         self.running = False


#     def monitor(self):

#         while self.running:

#             if not self.context.app_state.test_running:
#                 time.sleep(0.1)
#                 continue

#             for channel_id, buses in self.context.can_values.items():

#                 for bus_name, values in buses.items():

#                     for parameter in self.alarm_parameters:

#                         value = values.get(parameter, "No Error")

#                         key = (
#                             channel_id,
#                             bus_name,
#                             parameter
#                         )

#                         if value == "ERROR":

#                             if key not in self.active_alarms:

#                                 self.active_alarms.add(key)

#                                 print("Error detected")

#                                 self.context.test_controller.raise_alarm(
#                                     channel_id,
#                                     bus_name,
#                                     parameter
#                                 )

#                         else:

#                             self.active_alarms.discard(key)

#             time.sleep(0.1)


#     # def monitor(self):

#     #     while self.running:

#     #         if not self.context.app_state.test_running:
#     #             time.sleep(0.1)
#     #             continue

#     #         for dut_id, values in self.context.can_values.items():

#     #             for parameter in self.alarm_parameters:

#     #                 value = values.get(parameter, 0)

#     #                 key = (dut_id, parameter)

#     #                 if value == 1:

#     #                     # Alarm has not been handled yet
#     #                     if key not in self.active_alarms:

#     #                         self.active_alarms.add(key)

#     #                         self.context.test_controller.raise_alarm(
#     #                             dut_id,
#     #                             parameter
#     #                         )

#     #                 else:
#     #                     print(parameter, value)

#     #                     # Alarm bit returned to 0
#     #                     self.active_alarms.discard(key)

#     #         time.sleep(0.1)


#     # def monitor(self):

#     #     while self.running:

#     #         if not self.context.test_controller.is_test_running():
#     #             time.sleep(0.2)
#     #             continue

#     #         for dut_id, values in self.context.can_values.items():

#     #             for parameter in self.alarm_parameters:

#     #                 if values.get(parameter, 0) == 1:

#     #                     self.context.test_controller.raise_alarm(
#     #                         dut_id,
#     #                         parameter
#     #                     )

#     #         time.sleep(0.1)



# class AlarmMonitor:

#     def __init__(self, context):
#         self.context = context
#         self.running = False
#         self.thread = None

#         # Prevent repeated popup while alarm remains ERROR
#         self.active_alarms = set()

#         self.alarm_parameters = WATCH_PARAMETERS[0x50E]

#         self.bus_to_dut = {
#             "PCAN_USBBUS1": 1,
#             "PCAN_USBBUS2": 2,
#             "PCAN_USBBUS3": 3,
#             "PCAN_USBBUS4": 4,
#         }

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

#     def stop(self):

#         self.running = False

#         if self.thread:
#             self.thread.join(timeout=1)

#         print("Alarm Monitor Stopped")

#     def monitor(self):

#         while self.running:

#             if not self.context.app_state.test_running:
#                 time.sleep(0.1)
#                 continue

#             can_values = getattr(
#                 self.context,
#                 "can_values",
#                 {}
#             )

#             for channel_id, buses in can_values.items():

#                 for bus_name, values in buses.items():

#                     dut_id = self.bus_to_dut.get(bus_name)

#                     if dut_id is None:
#                         continue

#                     for parameter in self.alarm_parameters:

#                         value = values.get(
#                             parameter,
#                             "No Error"
#                         )

#                         key = (
#                             dut_id,
#                             parameter
#                         )

#                         if value == "ERROR":

#                             if key not in self.active_alarms:

#                                 self.active_alarms.add(key)

#                                 print(
#                                     f"ALARM DETECTED: "
#                                     f"DUT {dut_id} - "
#                                     f"{parameter}"
#                                 )

#                                 # self.context.test_controller.raise_alarm(
#                                 #     dut_id,
#                                 #     parameter
#                                 # )

#                                 dut_id = self.bus_to_dut[bus_name]

#                                 self.context.test_controller.raise_alarm(
#                                     dut_id,
#                                     parameter
#                                 )
#                         else:

#                             self.active_alarms.discard(key)

#             time.sleep(0.1)

import threading
import time


class AlarmMonitor:

    def __init__(self, context):
        self.context = context
        self.running = False
        self.thread = None

        # Currently active alarms
        # {(dut_id, parameter), ...}
        self.active_alarms = set()

        self.alarm_parameters = WATCH_PARAMETERS[0x50E]

        self.bus_to_dut = {
            "PCAN_USBBUS1": 1,
            "PCAN_USBBUS2": 2,
            "PCAN_USBBUS3": 3,
            "PCAN_USBBUS4": 4,
        }

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

    def stop(self):

        self.running = False

        if self.thread:
            self.thread.join(timeout=1)

        print("Alarm Monitor Stopped")

    def monitor(self):

        while self.running:

            if not self.context.app_state.test_running:
                time.sleep(0.1)
                continue

            can_values = getattr(
                self.context,
                "can_values",
                {}
            )

            # =====================================================
            # COLLECT ALL CURRENTLY FAILING ALARMS
            # =====================================================

            current_alarms = set()

            for channel_id, buses in can_values.items():

                for bus_name, values in buses.items():

                    dut_id = self.bus_to_dut.get(bus_name)

                    if dut_id is None:
                        continue

                    for parameter in self.alarm_parameters:

                        value = values.get(
                            parameter,
                            "No Error"
                        )

                        if value == "ERROR":

                            key = (
                                dut_id,
                                parameter
                            )

                            current_alarms.add(key)

            # =====================================================
            # FIND NEW ALARMS
            # =====================================================

            new_alarms = current_alarms - self.active_alarms

            # =====================================================
            # UPDATE ACTIVE ALARMS
            # =====================================================

            self.active_alarms = current_alarms

            # =====================================================
            # SHOW ONE POPUP FOR ALL NEW FAILURES
            # =====================================================

            if new_alarms:

                alarms = []

                for dut_id, parameter in sorted(new_alarms):

                    alarms.append({
                        "dut_id": dut_id,
                        "parameter": parameter
                    })

                    print(
                        f"ALARM DETECTED: "
                        f"DUT {dut_id} - {parameter}"
                    )

                # ONE call containing ALL alarms
                self.context.test_controller.raise_alarm(
                    alarms
                )

            time.sleep(0.1)