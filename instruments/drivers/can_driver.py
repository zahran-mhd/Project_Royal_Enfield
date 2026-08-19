# import can
# import cantools


# class CANDriver:

#     def __init__(self, channel, bitrate, dbc_file=None):

#         self.bus = can.interface.Bus(
#             interface="pcan",
#             channel=channel,
#             bitrate=bitrate
#         )

#         self.db = None

#         if dbc_file:
#             self.db = cantools.database.load_file(dbc_file)

#     def receive(self, timeout=0.01):

#         return self.bus.recv(timeout)

#     def send(self, arbitration_id, data, extended=False):

#         msg = can.Message(
#             arbitration_id=arbitration_id,
#             data=data,
#             is_extended_id=extended
#         )

#         self.bus.send(msg)

#     def shutdown(self):

#         self.bus.shutdown()

import can


class CANDriver:

    def __init__(
        self,
        channel,
        bitrate
    ):

        self.channel = channel
        self.bitrate = bitrate

        self.bus = None

    #################################################

    def connect(self):

        if self.bus:
            return

        self.bus = can.Bus(
            interface="pcan",
            channel=self.channel,
            bitrate=self.bitrate
        )

        print(f"{self.channel} Connected")

    #################################################

    def disconnect(self):

        if self.bus:

            self.bus.shutdown()

            self.bus = None

            print(f"{self.channel} Disconnected")

    #################################################

    def send(self, msg):

        if self.bus:

            self.bus.send(msg)

    #################################################

    def receive(self, timeout=0.2):

        if self.bus:

            return self.bus.recv(timeout)

        return None