import threading


class PW3337Worker(threading.Thread):

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

                power = (
                    self.driver.read_power()
                )

                self.app.data_model.instrument_values[
                    "PW3337"
                ] = {

                    "Voltage": voltage,
                    "Current": current,
                    "Power": power
                }

            except Exception as ex:

                print(
                    f"PW3337 Error: {ex}"
                )

            self.stop_event.wait(1)

        self.driver.disconnect()