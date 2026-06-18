from instruments.drivers.asr3400_driver import ASR3400Driver
from instruments.drivers.pw3337_driver import PW3337Driver

from instruments.workers.asr3400_worker import ASR3400Worker
from instruments.workers.pw3337_worker import PW3337Worker

class InstrumentManager:

    def __init__(self, app):

        self.app = app

        self.workers = []

        self.running = False

    def start(self):

        if self.running:

            return

        self.running = True

        configs = (
            self.app.instrument_repo
            .get_all_instruments()
        )

        for config in configs:

            if not config["Status"]:

                continue

            if config["InstrumentName"] == "ASR3400":

                driver = ASR3400Driver(
                    config["Address"]
                )

                driver.connect()

                worker = ASR3400Worker(
                    self.app,
                    driver
                )

                worker.start()

                self.workers.append(
                    worker
                )

            elif config["InstrumentName"] == "PW3337":

                driver = PW3337Driver(
                    config["Address"]
                )

                driver.connect()

                worker = PW3337Worker(
                    self.app,
                    driver
                )

                worker.start()

                self.workers.append(
                    worker
                )


    def stop(self):

        if not self.running:

            return

        self.running = False

        for worker in self.workers:

            worker.stop()

        for worker in self.workers:

            worker.join(timeout=5)

        self.workers.clear()