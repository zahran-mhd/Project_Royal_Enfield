import threading
import queue


class CANWorker(threading.Thread):

    def __init__(self, app, name, driver):

        super().__init__(daemon=True)

        self.app = app

        self.name = name

        self.driver = driver

        self.rx_queue = queue.Queue()

        self.tx_queue = queue.Queue()

        self.stop_event = threading.Event()

    def stop(self):

        self.stop_event.set()

    def send(self, arbitration_id, data, extended=False):

        self.tx_queue.put(
            (arbitration_id, data, extended)
        )

    def run(self):

        while not self.stop_event.is_set():

            #
            # Receive
            #

            msg = self.driver.receive()

            if msg:

                self.rx_queue.put(msg)

            #
            # Transmit
            #

            while not self.tx_queue.empty():

                arbitration_id, data, extended = self.tx_queue.get()

                self.driver.send(
                    arbitration_id,
                    data,
                    extended
                )

        self.driver.shutdown()