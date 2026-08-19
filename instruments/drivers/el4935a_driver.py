import pyvisa
import time

class EL4935ADriver:

    def __init__(self, address):

        self.address = address

        self.rm = None

        self.instrument = None

    def connect(self):

        self.rm = pyvisa.ResourceManager()
        RESOURCE = f"TCPIP0::{self.address}::inst0::INSTR"

        self.instrument = self.rm.open_resource(
            RESOURCE
        )

        self.instrument.timeout = 5000

        idn = self.instrument.query('*IDN?')
        print(idn)

        # self.instrument.read_termination = "\n"
        # self.instrument.write_termination = "\n"

    def disconnect(self):

        if self.instrument:

            self.instrument.close()

            self.instrument = None

    def read_voltage(self):
        temp_values = self.instrument.query_ascii_values(':MEASure:SCALar:VOLTage:DC?')
        dc = temp_values[0]

        return float(
            dc
        )

    def read_current(self):
        temp_values = self.instrument.query_ascii_values(':MEASure:SCALar:CURRent:DC?')
        dc1 = temp_values[0]
        return float(
            dc1
        )

    def initial_setting(self,settings):

        if settings:
            # voltage = settings["dc_output_voltage"]
            current = settings["dis_dc_load_current"]
            # load_current = settings["char_dc_load_current"]

            print(current)
        self.instrument.write(':OUTPut:STATe %d' % (0))

        self.instrument.write(f':SOURce:CURRent:LEVel:IMMediate:AMPLitude {current}')
        time.sleep(0.2)
        self.instrument.write(':OUTPut:STATe %d' % (1))

    
    def off(self):
        self.instrument.write(':OUTPut:STATe %d' % (0))
        time.sleep(0.2)
