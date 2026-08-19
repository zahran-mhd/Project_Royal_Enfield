# from instruments.drivers.can_driver import CANDriver

# from instruments.workers.can_worker import CANWorker

# class CANManager:

#     def __init__(self, app):

#         self.app = app
#         self.workers = {}

#     def start(self):

#         for channel in range(1, 7):

#             driver = CANDriver(
#                 channel=f"PCAN_USBBUS{channel}",
#                 bitrate=500000
#             )

#             worker = CANWorker(
#                 self.app,
#                 f"CAN{channel}",
#                 driver
#             )

#             worker.start()

#             self.register(channel, worker)
#     def register(self, channel, worker):
#         self.workers[channel] = worker

#     def send(self, channel, arbitration_id, data, extended=False):

#         if channel not in self.workers:
#             raise ValueError(f"CAN Channel {channel} not registered")

#         self.workers[channel].send(
#             arbitration_id,
#             data,
#             extended
#         )

#     def get_worker(self, channel):
#         return self.workers.get(channel)
from instruments.workers.can_worker import CANWorker
from instruments.can_constants import CHANNEL_PORTS
from instruments.can_messages import MESSAGE_SETS


class CANManager:

    def __init__(self, context):

        self.context = context

        self.workers = {}

    # --------------------------------------------------

    def connect_channel(
        self,
        channel_id,
        bitrate
    ):

        self.disconnect_channel(channel_id)

        self.workers[channel_id] = {}

        ports = CHANNEL_PORTS[channel_id]

        for port in ports:

            worker = CANWorker(

                name=port,

                channel=port,

                channel_id=channel_id,

                bitrate=bitrate,

                decoder=self.context.decoder,

                context=self.context,

                data_callback=self.on_can_data
            )

            worker.set_messages(

                MESSAGE_SETS[port]["charge"],

                MESSAGE_SETS[port]["discharge"]
            )

            worker.start()

            self.workers[channel_id][port] = worker

    # --------------------------------------------------

    def disconnect_channel(self, channel_id):

        if channel_id not in self.workers:
            return

        for worker in self.workers[channel_id].values():

            worker.stop()

        del self.workers[channel_id]

    # --------------------------------------------------

    def disconnect_all(self):

        for channel_id in list(self.workers.keys()):

            self.disconnect_channel(channel_id)

    # --------------------------------------------------

    def set_mode(
        self,
        channel_id,
        mode
    ):

        if channel_id not in self.workers:
            return

        for worker in self.workers[channel_id].values():

            worker.set_mode(mode)

    # --------------------------------------------------

    def send(
        self,
        channel_id,
        port,
        message
    ):

        if channel_id not in self.workers:
            return

        if port not in self.workers[channel_id]:
            return

        self.workers[channel_id][port].send(message)

    # --------------------------------------------------

    def on_can_data(
        self,
        port,
        decoded_data
    ):

        """
        decoded_data is a list like

        [
            {
                "parameter":"Voltage",
                "value":13.2
            },
            ...
        ]
        """

        if self.context.test_controller:

            self.context.test_controller.process_can_data(
                port,
                decoded_data
            )

    def set_charge_current(self, channel_id, port, current):

        print(
        f"set_charge_current called: "
        f"channel={channel_id}, port={port}, current={current}"
    )

        # print("Workers dict:", self.workers.keys())

        if channel_id not in self.workers:
            print("Channel not found")
            return

        worker = self.workers[channel_id].get(port)

        if worker is None:
            print("Worker is None")
            print("Available ports:", self.workers[channel_id].keys())
            return
        # print("Worker:", id(worker))
        worker.update_charge_current(current)