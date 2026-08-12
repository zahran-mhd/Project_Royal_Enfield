from instruments.drivers.can_driver import CANDriver

from instruments.workers.can_worker import CANWorker

class CANManager:

    def __init__(self, app):

        self.app = app
        self.workers = {}

    def start(self):

        for channel in range(1, 7):

            driver = CANDriver(
                channel=f"PCAN_USBBUS{channel}",
                bitrate=500000
            )

            worker = CANWorker(
                self.app,
                f"CAN{channel}",
                driver
            )

            worker.start()

            self.register(channel, worker)
    def register(self, channel, worker):
        self.workers[channel] = worker

    def send(self, channel, arbitration_id, data, extended=False):

        if channel not in self.workers:
            raise ValueError(f"CAN Channel {channel} not registered")

        self.workers[channel].send(
            arbitration_id,
            data,
            extended
        )

    def get_worker(self, channel):
        return self.workers.get(channel)