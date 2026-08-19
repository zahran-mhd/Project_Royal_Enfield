import pyvisa


class PW3337Driver:

    def __init__(self, address):

        self.address = address

        self.rm = None

        self.instrument = None

    def connect(self):

        self.rm = pyvisa.ResourceManager()
        print(self.address)
        RESOURCE = f"TCPIP0::{self.address}::3300::SOCKET"

        self.instrument = self.rm.open_resource(
            RESOURCE
        )

        self.instrument.timeout = 5000
        self.instrument.read_termination = "\n"
        self.instrument.write_termination = "\n"

        idn = self.instrument.query('*IDN?')
        print(idn)

        self.instrument.write(":MEAS:ITEM:UTHD:CH1 1")
        self.instrument.write(":MEAS:ITEM:UTHD:CH2 1")
        self.instrument.write(":MEAS:ITEM:UTHD:CH3 1")

        self.instrument.write(":MEAS:ITEM:ITHD:CH1 1")
        self.instrument.write(":MEAS:ITEM:ITHD:CH2 1")
        self.instrument.write(":MEAS:ITEM:ITHD:CH3 1")

    def disconnect(self):

        if self.instrument:

            self.instrument.close()

            self.instrument = None

    # def read_voltage(self):

    #     return float(
    #         self.instrument.query(
    #             ":NUMERIC:NORMAL:VALUE? 1"
    #         )
    #     )

    # def read_current(self):

    #     return float(
    #         self.instrument.query(
    #             ":NUMERIC:NORMAL:VALUE? 2"
    #         )
    #     )

    # def read_power(self):

    #     return float(
    #         self.instrument.query(
    #             ":NUMERIC:NORMAL:VALUE? 3"
    #         )
    #     )

    def read(self):
        response = self.instrument.query(":MEAS?").strip()

        data = {}

        for item in response.split(";"):

            item = item.strip()

            if not item:
                continue

            parts = item.split()

            if len(parts) != 2:
                continue

            key = parts[0]

            try:
                value = float(parts[1])
            except:
                value = None

            data[key] = value

        return data