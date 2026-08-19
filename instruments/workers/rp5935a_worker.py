import threading


class RP5935AWorker(threading.Thread):

    def __init__(
        self,
        app,
        driver
    ):

        super().__init__(
            daemon=True
        )

        self.app = app

        self.driver = driver

        self.stop_event = threading.Event()

    def stop(self):

        self.stop_event.set()

    def run(self):

        while not self.stop_event.is_set():

            try:

                voltage = (
                    self.driver.read_voltage()
                )

                current = (
                    self.driver.read_current()
                )

                self.app.data_model.instrument_values[
                    "RP5935A"
                ] = {

                    "Voltage": voltage,
                    "Current": current
                }

            except Exception as ex:

                print(
                    f"RP5935A Error: {ex}"
                )

            self.stop_event.wait(1)

        # self.driver.disconnect()