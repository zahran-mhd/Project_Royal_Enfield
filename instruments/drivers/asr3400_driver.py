import pyvisa
import time

class ASR3400Driver:

    def __init__(self, address):

        self.address = address
        print("ASR address : ", address)

        self.rm = None

        self.instrument = None

        

    def connect(self):

        self.rm = pyvisa.ResourceManager()

        self.instrument = self.rm.open_resource(
            f"TCPIP0::{self.address}::2268::SOCKET"
        )

        self.instrument.timeout = 5000
        self.instrument.write_termination = "\n"
        self.instrument.read_termination = "\n"

        self.instrument.clear()

        print("ASR address:", self.address)
        print("IDN:", self.instrument.query("*IDN?").strip())

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

    def initial_setting(self,voltage,frequency):
        # ------------------------------------
        # Set voltage
        # ------------------------------------

        print("\nSetting voltage to 230 V...")

        self.instrument.write(f":VOLT {voltage}")

        print(
            "Voltage:",
            self.instrument.query(":VOLT?").strip()
        )

        print(
            "Error:",
            self.instrument.query(":SYST:ERR?").strip()
        )


        # ------------------------------------
        # Set frequency
        # ------------------------------------

        print("\nSetting frequency to 50 Hz...")

        self.instrument.write(f":FREQ {frequency}")

        print(
            "Frequency:",
            self.instrument.query(":FREQ?").strip()
        )

        print(
            "Error:",
            self.instrument.query(":SYST:ERR?").strip()
        )


        # ------------------------------------
        # Output ON
        # ------------------------------------

        print("\nTurning output ON...")

        self.instrument.write(":OUTP ON")
        time.sleep(2)

        print("Output:", self.instrument.query(":OUTP?"))
        print("Set frequency:", self.instrument.query(":FREQ?"))
        print("Measured voltage:", self.instrument.query(":MEAS:VOLT?"))
        print("Measured current:", self.instrument.query(":MEAS:CURR?"))
        print("Measured frequency:", self.instrument.query(":MEAS:FREQ?"))
        time.sleep(2)

    def off(self):
        self.instrument.write(":OUTP OFF")
        time.sleep(0.2)
    