# import threading
# import queue


# class CANWorker(threading.Thread):

#     def __init__(self, app, name, driver):

#         super().__init__(daemon=True)

#         self.app = app

#         self.name = name

#         self.driver = driver

#         self.rx_queue = queue.Queue()

#         self.tx_queue = queue.Queue()

#         self.stop_event = threading.Event()

#     def stop(self):

#         self.stop_event.set()

#     def send(self, arbitration_id, data, extended=False):

#         self.tx_queue.put(
#             (arbitration_id, data, extended)
#         )

#     def run(self):

#         while not self.stop_event.is_set():

#             #
#             # Receive
#             #

#             msg = self.driver.receive()

#             if msg:

#                 self.rx_queue.put(msg)

#             #
#             # Transmit
#             #

#             while not self.tx_queue.empty():

#                 arbitration_id, data, extended = self.tx_queue.get()

#                 self.driver.send(
#                     arbitration_id,
#                     data,
#                     extended
#                 )

#         self.driver.shutdown()

import threading
import queue
import time

from instruments.drivers.can_driver import CANDriver
from can.interfaces.pcan.pcan import PcanCanOperationError


class CANWorker:

    # def __init__(
    #     self,
    #     name,
    #     channel,
    #     bitrate,
    #     decoder,
    #     data_callback=None
    # ):

    #     self.name = name
    #     self.decoder = decoder
    #     self.data_callback = data_callback

    #     self.driver = CANDriver(
    #         channel=channel,
    #         bitrate=bitrate
    #     )

    #     self.running = False

    #     self.mode = "charge"

    #     self.messages = {
    #         "charge": [],
    #         "discharge": []
    #     }
    #     self.rx_thread = None
    #     self.tx_thread = None

    #     self.tx_queue = queue.Queue()

    def __init__(
            self,
            name,
            channel,
            channel_id,
            bitrate,
            decoder,
            context,
            data_callback=None
        ):

            self.name = name
            self.channel = channel
            self.decoder = decoder
            self.context = context
            self.data_callback = data_callback
            self.channel_id = channel_id

            self.driver = CANDriver(
                channel=channel,
                bitrate=bitrate
            )

            self.running = False

            self.mode = "charge"

            self.messages = {
                "charge": [],
                "discharge": []
            }

            self.rx_thread = None
            self.tx_thread = None

            self.tx_queue = queue.Queue()

    # --------------------------------------------------

    def set_messages(self, charge_messages, discharge_messages):

        self.messages["charge"] = charge_messages
        self.messages["discharge"] = discharge_messages

    # --------------------------------------------------

    def set_mode(self, mode):

        self.mode = mode.lower()

    # --------------------------------------------------

    def start(self):

        self.driver.connect()

        self.running = True

        self.rx_thread = threading.Thread(
            target=self.receive_loop,
            daemon=True
        )

        self.tx_thread = threading.Thread(
            target=self.transmit_loop,
            daemon=True
        )

        self.rx_thread.start()
        self.tx_thread.start()

        print(f"{self.name} Started")

    # --------------------------------------------------

    # def stop(self):

    #     self.running = False

    #     self.driver.disconnect()

    #     print(f"{self.name} Stopped")

    # def stop(self):

    #     self.running = False

    #     # Close CAN interface
    #     self.driver.disconnect()

    #     # Wait for threads to exit
    #     if self.rx_thread and self.rx_thread.is_alive():
    #         self.rx_thread.join(timeout=1)

    #     if self.tx_thread and self.tx_thread.is_alive():
    #         self.tx_thread.join(timeout=1)

    #     print(f"{self.name} Stopped")


    def stop(self):

        self.running = False

        if self.rx_thread:
            self.rx_thread.join(timeout=1)

        if self.tx_thread:
            self.tx_thread.join(timeout=1)

        self.driver.disconnect()

        print(f"{self.name} Stopped")

    # --------------------------------------------------

    def send(self, message):

        self.tx_queue.put(message)

    # --------------------------------------------------

    def transmit_loop(self):

        last_periodic = 0

        while self.running:

            now = time.time()

            # Send periodic messages every 100 ms
            if now - last_periodic >= 0.1:

                for msg in self.messages[self.mode]:
                    # if msg.arbitration_id == 0x12C:
                        # print("TX msg id:", id(msg), list(msg.data))

                    self.driver.send(msg)

                last_periodic = now

            # Send queued messages immediately
            try:

                msg = self.tx_queue.get_nowait()

                self.driver.send(msg)

            except queue.Empty:

                pass

            time.sleep(0.005)

    # --------------------------------------------------

    # def receive_loop(self):

    #     while self.running:

    #         msg = self.driver.receive(timeout=0.2)

    #         if msg is None:
    #             continue

    #         # print("inside receive_loop")
    #         # print(f"RX ID: 0x{msg.arbitration_id:X}")
    #         # print(f"DATA : {msg.data.hex()}")
    #         decoded = self.decoder.decode(
    #             msg.arbitration_id,
    #             msg.data
    #         )

    #         # print(decoded)

    #         if decoded is None:
    #             continue

    #         # print(f"RX: 0x{msg.arbitration_id:X}")

    #         decoded = self.decoder.decode(
    #             msg.arbitration_id,
    #             msg.data
    #         )

    #         # print(decoded)

    #         if self.data_callback:

    #             self.data_callback(
    #                 self.name,
    #                 decoded
    #             )

    

    # def receive_loop(self):

    #     while self.running:

    #         try:
    #             msg = self.driver.receive(timeout=0.2)

    #         except PcanCanOperationError:
    #             # CAN channel was disconnected while waiting for data
    #             break

    #         except Exception as e:
    #             print(f"{self.name}: {e}")
    #             break

    #         if msg is None:
    #             continue

    #         decoded = self.decoder.decode(
    #             msg.arbitration_id,
    #             msg.data
    #         )

    #         if decoded is None:
    #             continue

    #         if decoded:

    #             values = {
    #                 item["parameter"]: item["value"]
    #                 for item in decoded
    #             }

    #             self.context.can_values[dut_id].update(values)

    #         if self.data_callback:
    #             self.data_callback(
    #                 self.name,
    #                 decoded
    #             )

    #     print(f"{self.name} Receive thread exited")

    # def receive_loop(self):

    #     while self.running:

    #         try:
    #             msg = self.driver.receive(timeout=0.2)

    #         except PcanCanOperationError:
    #             print(f"{self.name}: CAN channel disconnected")
    #             break

    #         except Exception as e:
    #             print(f"{self.name}: {e}")
    #             break

    #         if msg is None:
    #             continue

    #         decoded = self.decoder.decode(
    #             msg.arbitration_id,
    #             msg.data
    #         )

    #         if decoded is None:
    #             continue

    #         if decoded:

    #             values = {
    #                 item["parameter"]: item["value"]
    #                 for item in decoded
    #             }

    #             self.context.can_values[
    #                 self.channel_id
    #             ][self.name].update(values)

    #         if self.data_callback:

    #             self.data_callback(
    #                 self.name,
    #                 decoded
    #             )

    #     print(f"{self.name} Receive thread exited")

    def receive_loop(self):

        while self.running:

            try:
                msg = self.driver.receive(timeout=0.2)

            except PcanCanOperationError:
                print(f"{self.name}: CAN channel disconnected")
                break

            except Exception as e:
                print(f"{self.name}: {e}")
                break

            if msg is None:
                continue

            decoded = self.decoder.decode(
                msg.arbitration_id,
                msg.data
            )

            if decoded is None:
                continue

            if decoded:

                values = {
                    item["parameter"]: item["value"]
                    for item in decoded
                }

                self.context.can_values[
                    self.channel_id
                ][self.name].update(values)

                # # # DEBUG
                # if msg.arbitration_id == 0x50E:

                #     print("\n========== ALARM CAN ==========")
                #     print("Channel :", self.channel_id)
                #     print("Bus     :", self.name)
                #     print("Values  :", values)
                #     print(
                #         "Stored  :",
                #         self.context.can_values[
                #             self.channel_id
                #         ][self.name]
                #     )
                #     print("===============================\n")

            if self.data_callback:

                self.data_callback(
                    self.name,
                    decoded
                )

        print(f"{self.name} Receive thread exited")

    def update_charge_current(self, current):

        for msg in self.messages["charge"]:
            if msg.arbitration_id == 0x12C:
                print("Update msg id:", id(msg))
                print("Before:", list(msg.data))

                raw = int(current * 100)
                msg.data[0] = raw & 0xFF
                msg.data[1] = (raw >> 8) & 0xFF

                print("After :", list(msg.data))

        # raw = int(current * 100)

        # for msg in self.messages["charge"]:

        #     if msg.arbitration_id == 0x12C:

        #         msg.data[0] = raw & 0xFF
        #         msg.data[1] = (raw >> 8) & 0xFF

        #         print("Updated:", list(msg.data))
        #         break



    