import pyvisa


class ASR3400Driver:

    def __init__(self, address):

        self.address = address

        self.rm = None

        self.instrument = None

    def connect(self):

        self.rm = pyvisa.ResourceManager()

        self.instrument = self.rm.open_resource(
            self.address
        )

        self.instrument.timeout = 3000

    def disconnect(self):

        if self.instrument:

            self.instrument.close()

            self.instrument = None

    def read_voltage(self):

        return float(
            self.instrument.query(
                "MEAS:VOLT?"
            )
        )

    def read_current(self):

        return float(
            self.instrument.query(
                "MEAS:CURR?"
            )
        )