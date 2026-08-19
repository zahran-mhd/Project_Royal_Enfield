import threading

from instruments.drivers.asr3400_driver import ASR3400Driver
from instruments.drivers.pw3337_driver import PW3337Driver
from instruments.drivers.rp5935a_driver import RP5935ADriver
from instruments.drivers.el4935a_driver import EL4935ADriver
from instruments.drivers.el34143a_driver import EL34143ADriver
from instruments.drivers.daq970a_driver import (DAQ970ADriver)


from instruments.workers.asr3400_worker import ASR3400Worker
from instruments.workers.pw3337_worker import PW3337Worker
from instruments.workers.rp5935a_worker import RP5935AWorker
from instruments.workers.el4935a_worker import EL4935AWorker
from instruments.workers.el34143a_worker import EL34143AWorker
from instruments.workers.daq970a_worker import (DAQ970AWorker)


DRIVER_MAP = {
    "ASR3400Driver": ASR3400Driver,
    "PW3337Driver": PW3337Driver,
    # "DAQ970ADriver": DAQ970ADriver,
    "RP5935ADriver": RP5935ADriver,
    "EL4935ADriver": EL4935ADriver,
    "EL34143ADriver": EL34143ADriver,
    "DAQ970ADriver": DAQ970ADriver
}

WORKER_MAP = {
    "ASR3400Worker": ASR3400Worker,
    "PW3337Worker": PW3337Worker,
    "DAQ970AWorker": DAQ970AWorker,
    "RP5935AWorker": RP5935AWorker,
    "EL4935AWorker": EL4935AWorker,
    "EL34143AWorker": EL34143AWorker,
}

class InstrumentManager:

    def __init__(self, context):

        self.context = context

        # InstrumentID -> Driver
        self.drivers = {}

        # InstrumentID -> Worker
        self.workers = {}

        # InstrumentID -> Channel IDs using it
        self.users = {}

        self.lock = threading.Lock()

    # def connect_all(self):

    #     configs = self.app.instrument_repository.get_all_instruments()

    #     for config in configs:

    #         instrument_id = config["InstrumentID"]

    #         try:

    #             if config["InstrumentName"] == "ASR3400":

    #                 driver = ASR3400Driver(
    #                     config["Address"]
    #                 )

    #             elif config["InstrumentName"] == "PW3337":

    #                 driver = PW3337Driver(
    #                     config["Address"]
    #                 )

    #             else:
    #                 continue

    #             driver.connect()

    #             self.drivers[instrument_id] = driver

    #             self.users[instrument_id] = set()

    #             self.app.instrument_repository.update_connection_status(
    #                 instrument_id,
    #                 1
    #             )

    #             print(f"{config['InstrumentName']} Connected")

    #         except Exception as ex:

    #             print(ex)

    #             self.app.instrument_repository.update_connection_status(
    #                 instrument_id,
    #                 0
    #             )


    # def connect_all(self):

    #     configs = self.app.instrument_repository.get_all()

    #     for config in configs:

    #         instrument_id = config.instrument_id

    #         try:

    #             driver = None

    #             if config.instrument_name == "ASR3400":

    #                 driver = ASR3400Driver(
    #                     config.address
    #                 )

    #             elif config.instrument_name == "PW3337":

    #                 driver = PW3337Driver(
    #                     config.address
    #                 )

    #             if driver is None:
    #                 continue

    #             driver.connect()

    #             self.drivers[instrument_id] = driver

    #             self.users[instrument_id] = set()

    #             self.app.instrument_repository.update_connection_status(
    #                 instrument_id,
    #                 1
    #             )

    #             print(f"{config.instrument_name} Connected")

    #         except Exception as ex:

    #             print(f"{config.instrument_name} Connection Failed: {ex}")

    #             self.app.instrument_repository.update_connection_status(
    #                 instrument_id,
    #                 0
    #             )

    def connect_all(self):

        configs = self.context.instrument_repository.get_all()

        for config in configs:

            instrument_id = config.instrument_id

            try:

                # Skip if already connected
                if instrument_id in self.drivers:
                    continue

                # Get driver class from registry
                driver_class = DRIVER_MAP.get(
                    config.driver_class
                )

                if driver_class is None:

                    print(
                        f"No driver registered for "
                        f"{config.instrument_type}"
                    )

                    self.context.instrument_repository.update_connection_status(
                        instrument_id,
                        0
                    )

                    continue

                # Create driver
                driver = driver_class(
                    config.address
                )

                # Connect
                driver.connect()

                # Store connected driver
                self.drivers[instrument_id] = driver

                # Initialize channel users
                self.users[instrument_id] = set()

                # Update database
                self.context.instrument_repository.update_connection_status(
                    instrument_id,
                    1
                )

                print(
                    f"{config.instrument_name} "
                    f"({config.instrument_type}) Connected"
                )

            except Exception as ex:

                print(
                    f"{config.instrument_name} "
                    f"Connection Failed : {ex}"
                )

                self.context.instrument_repository.update_connection_status(
                    instrument_id,
                    0
                )

    # def start_channel(self, channel_id):

    #     configs = self.context.instrument_repository.get_by_channel(channel_id)

    #     for config in configs:

    #         instrument_id = config.instrument_id

    #         # Driver not connected
    #         if instrument_id not in self.drivers:
    #             continue

    #         # Register this channel as a user
    #         self.users.setdefault(instrument_id, set()).add(channel_id)

    #         # Worker already running
    #         if instrument_id in self.workers:
    #             continue

    #         worker_class = WORKER_MAP.get(config.worker_class)

    #         if worker_class is None:

    #             print(
    #                 f"No worker registered for "
    #                 f"{config.instrument_name}"
    #             )
    #             continue

    #         driver = self.drivers[instrument_id]

    #         try:

    #             worker = worker_class(
    #                 self.context,
    #                 driver
    #             )

    #             worker.start()

    #             self.workers[instrument_id] = worker

    #             print(
    #                 f"{config.instrument_name} worker started"
    #             )

    #         except Exception as ex:

    #             print(
    #                 f"Failed to start "
    #                 f"{config.instrument_name}: {ex}"
    #             )


    # def start_channel(self, channel_id):

    #     configs = (
    #         self.context.instrument_repository
    #         .get_by_channel(channel_id)
    #     )

    #     for config in configs:

    #         instrument_id = config.instrument_id

    #         # -------------------------------------------------
    #         # DRIVER NOT CONNECTED
    #         # -------------------------------------------------

    #         if instrument_id not in self.drivers:

    #             print(
    #                 f"Instrument {instrument_id} "
    #                 f"not connected"
    #             )

    #             continue

    #         # -------------------------------------------------
    #         # REGISTER CHANNEL USER
    #         # -------------------------------------------------

    #         self.users.setdefault(
    #             instrument_id,
    #             set()
    #         ).add(
    #             channel_id
    #         )

    #         # -------------------------------------------------
    #         # DAQ970A SPECIAL HANDLING
    #         # -------------------------------------------------

    #         if config.instrument_type == "DAQ970A":

    #             self.start_daq_channel(
    #                 channel_id,
    #                 config
    #             )

    #             continue

    #         # -------------------------------------------------
    #         # NORMAL INSTRUMENT
    #         # -------------------------------------------------

    #         if instrument_id in self.workers:

    #             continue

    #         worker_class = WORKER_MAP.get(
    #             config.worker_class
    #         )

    #         if worker_class is None:

    #             print(
    #                 f"No worker registered for "
    #                 f"{config.instrument_name}"
    #             )

    #             continue

    #         driver = self.drivers[
    #             instrument_id
    #         ]

    #         try:

    #             worker = worker_class(
    #                 self.context,
    #                 driver
    #             )

    #             worker.start()

    #             self.workers[
    #                 instrument_id
    #             ] = worker

    #             print(
    #                 f"{config.instrument_name} "
    #                 f"worker started"
    #             )

    #         except Exception as ex:

    #             print(
    #                 f"Failed to start "
    #                 f"{config.instrument_name}: {ex}"
    #             )

    def start_channel(self, channel_id):

        configs = (
            self.context
            .instrument_repository
            .get_by_channel(channel_id)
        )

        for config in configs:

            instrument_id = config.instrument_id

            # ---------------------------------------------
            # Driver not connected
            # ---------------------------------------------

            if instrument_id not in self.drivers:

                print(
                    f"Instrument {instrument_id} "
                    f"not connected"
                )

                continue

            # ---------------------------------------------
            # Register channel as user
            # ---------------------------------------------

            self.users.setdefault(
                instrument_id,
                set()
            ).add(
                channel_id
            )

            # ---------------------------------------------
            # Worker already running
            # ---------------------------------------------

            if instrument_id in self.workers:

                continue

            # ---------------------------------------------
            # Get worker class
            # ---------------------------------------------

            worker_class = WORKER_MAP.get(
                config.worker_class
            )

            if worker_class is None:

                print(
                    f"No worker registered for "
                    f"{config.instrument_name}"
                )

                continue

            driver = self.drivers[
                instrument_id
            ]

            try:

                # -----------------------------------------
                # DAQ970A
                # -----------------------------------------

                if config.instrument_type == "DAQ970A":

                    worker = worker_class(
                        self.context,
                        driver,
                        instrument_id
                    )

                # -----------------------------------------
                # Other instruments
                # -----------------------------------------

                else:

                    worker = worker_class(
                        self.context,
                        driver
                    )

                worker.start()

                self.workers[
                    instrument_id
                ] = worker

                print(
                    f"{config.instrument_name} "
                    f"worker started"
                )

            except Exception as ex:

                print(
                    f"Failed to start "
                    f"{config.instrument_name}: {ex}"
                )

                import traceback
                traceback.print_exc()

    def stop_channel(self, channel_id):

        for instrument_id in list(self.users.keys()):

            users = self.users[instrument_id]

            if channel_id not in users:
                continue

            users.remove(channel_id)

            # Another channel is still using it
            if users:
                continue

            worker = self.workers.pop(
                instrument_id,
                None
            )

            if worker is None:
                continue

            try:

                worker.stop()
                worker.join()

                print(
                    f"Worker stopped for "
                    f"Instrument {instrument_id}"
                )

            except Exception as ex:

                print(ex)

    def start_daq_channel(
        self,
        channel_id,
        config
    ):

        instrument_id = config.instrument_id

        driver = self.drivers.get(
            instrument_id
        )

        if driver is None:

            print(
                f"DAQ driver not found: "
                f"{instrument_id}"
            )

            return

        # -----------------------------------------------------
        # GET DAQ CHANNELS
        # -----------------------------------------------------

        channels = (
            self.context.instrument_repository
            .get_daq_channels(
                channel_id,
                instrument_id
            )
        )

        if not channels:

            print(
                f"No DAQ channels configured "
                f"for Channel {channel_id}, "
                f"Instrument {instrument_id}"
            )

            return

        # -----------------------------------------------------
        # WORKER ALREADY EXISTS
        # -----------------------------------------------------

        if instrument_id in self.workers:

            worker = self.workers[
                instrument_id
            ]

            worker.update_channels(
                channels
            )

            return

        # -----------------------------------------------------
        # CREATE WORKER
        # -----------------------------------------------------

        worker_class = WORKER_MAP.get(
            config.worker_class
        )

        if worker_class is None:

            print(
                "DAQ970AWorker not registered"
            )

            return

        try:

            daq_config = [
                {
                    "daq_channel": "205",
                    "slot": 2,
                    "parameter_name": "OBC_TEMP",
                    "measurement_type": "temperature",
                    "thermocouple_type": "K"
                },
                {
                    "daq_channel": "206",
                    "slot": 2,
                    "parameter_name": "FET_TEMP",
                    "measurement_type": "temperature",
                    "thermocouple_type": "K"
                }
                ]

            worker = worker_class(
                self.context,
                driver,
                instrument_id,
                daq_config,
                interval=1.0
            )

            worker.start()

            self.workers[
                instrument_id
            ] = worker

            print(
                f"DAQ worker started "
                f"for {instrument_id}"
            )

        except Exception as ex:

            print(
                f"Failed to start DAQ worker "
                f"{instrument_id}: {ex}"
            )


    # def start_channel(self, channel_id):

    #     configs = self.app.instrument_repository.get_by_channel(
    #         channel_id
    #     )

    #     for config in configs:

    #         instrument_id = config.instrument_id

    #         self.users[instrument_id].add(channel_id)

    #         if instrument_id in self.workers:
    #             continue

    #         driver = self.drivers[instrument_id]

    #         if config.instrument_name == "ASR3400":

    #             worker = ASR3400Worker(
    #                 self.app,
    #                 driver
    #             )

    #         elif config.instrument_name == "PW3337":

    #             worker = PW3337Worker(
    #                 self.app,
    #                 driver
    #             )

    #         else:
    #             continue

    #         worker.start()

    #         self.workers[instrument_id] = worker


    # def stop_channel(self, channel_id):

    #     for instrument_id in list(self.users.keys()):

    #         if channel_id not in self.users[instrument_id]:
    #             continue

    #         self.users[instrument_id].remove(channel_id)

    #         if len(self.users[instrument_id]) != 0:
    #             continue

    #         worker = self.workers.pop(
    #             instrument_id,
    #             None
    #         )

    #         if worker:

    #             worker.stop()

    #             worker.join()

    def disconnect_all(self):

        for worker in self.workers.values():

            worker.stop()

        for worker in self.workers.values():

            worker.join()

        self.workers.clear()

        for instrument_id, driver in self.drivers.items():

            try:

                driver.disconnect()

                self.context.instrument_repository.update_connection_status(
                    instrument_id,
                    0
                )

            except:
                pass

        self.drivers.clear()


    def get_driver(self, driver_type):
        for driver in self.drivers.values():
            if isinstance(driver, driver_type):
                return driver
        return None