import pyvisa
import threading
import time


class DAQ970ADriver:

    def __init__(self, address):

        self.address = address

        self.rm = None
        self.instrument = None

        self.lock = threading.Lock()

        self.scan_channels = []

    # =========================================================
    # CONNECT
    # =========================================================

    def connect(self):

        self.rm = pyvisa.ResourceManager()

        resource = (
            f"TCPIP0::{self.address}::inst0::INSTR"
        )

        self.instrument = self.rm.open_resource(
            resource
        )

        # 60 sec initially for debugging
        self.instrument.timeout = 60000

        self.instrument.write_termination = "\n"
        self.instrument.read_termination = "\n"

        idn = self.instrument.query(
            "*IDN?"
        ).strip()

        print(
            f"DAQ970A [{self.address}] : {idn}"
        )

        return idn

    # =========================================================
    # DISCONNECT
    # =========================================================

    def disconnect(self):

        with self.lock:

            try:

                if self.instrument:

                    self.instrument.close()

            except Exception as ex:

                print(
                    f"DAQ970A disconnect error: {ex}"
                )

            finally:

                self.instrument = None

                if self.rm:

                    try:
                        self.rm.close()
                    except Exception:
                        pass

                    self.rm = None

    # =========================================================
    # WRITE
    # =========================================================

    def write(self, command):

        with self.lock:

            if not self.instrument:

                raise RuntimeError(
                    "DAQ970A is not connected"
                )

            self.instrument.write(
                command
            )

    # =========================================================
    # QUERY
    # =========================================================

    def query(self, command):

        with self.lock:

            if not self.instrument:

                raise RuntimeError(
                    "DAQ970A is not connected"
                )

            return self.instrument.query(
                command
            ).strip()

    # =========================================================
    # RESET
    # =========================================================

    def reset(self):

        self.write("*RST")

        # Give the instrument time to reset
        time.sleep(1)

    # =========================================================
    # CLEAR
    # =========================================================

    def clear(self):

        self.write("*CLS")

    # =========================================================
    # IDENTIFY MODULE
    # =========================================================

    def identify_module(self, slot):

        response = self.query(
            f"SYST:CTYP? {slot}"
        )

        return response.strip()

    # =========================================================
    # GET INSTALLED MODULES
    # =========================================================

    def get_modules(self):

        modules = {}

        for slot in range(1, 4):

            try:

                module = self.identify_module(
                    slot
                )

                modules[slot] = module

                print(
                    f"DAQ slot {slot}: {module}"
                )

            except Exception as ex:

                modules[slot] = None

                print(
                    f"Slot {slot} detection error: "
                    f"{ex}"
                )

        return modules

    # =========================================================
    # CONFIGURE DC VOLTAGE
    # =========================================================

    def configure_dc_voltage(
        self,
        channels
    ):

        channel_string = ",".join(
            str(ch)
            for ch in channels
        )

        self.write(
            f"CONF:VOLT:DC (@{channel_string})"
        )

    # =========================================================
    # CONFIGURE DC CURRENT
    # =========================================================

    def configure_dc_current(
        self,
        channels
    ):

        channel_string = ",".join(
            str(ch)
            for ch in channels
        )

        self.write(
            f"CONF:CURR:DC (@{channel_string})"
        )

    # =========================================================
    # CONFIGURE TEMPERATURE
    # =========================================================

    def configure_temperature(
        self,
        channels,
        thermocouple_type="K"
    ):

        if not channels:

            return

        channels = [
            str(ch)
            for ch in channels
        ]

        self.scan_channels = channels

        channel_string = ",".join(
            channels
        )

        # -----------------------------------------------
        # Configure all channels
        # -----------------------------------------------

        command = (
            f"CONF:TEMP TC,"
            f"{thermocouple_type},"
            f"(@{channel_string})"
        )

        print(
            "DAQ CONFIG:",
            command
        )

        self.write(command)

        # -----------------------------------------------
        # Configure scan list
        # -----------------------------------------------

        self.write(
            f"ROUT:SCAN (@{channel_string})"
        )

        print(
            "DAQ SCAN LIST:",
            channel_string
        )

    # =========================================================
    # CONFIGURE RESISTANCE
    # =========================================================

    def configure_resistance(
        self,
        channels
    ):

        channel_string = ",".join(
            str(ch)
            for ch in channels
        )

        self.write(
            f"CONF:RES (@{channel_string})"
        )

    # =========================================================
    # CONFIGURE CHANNEL
    # =========================================================

    def configure_channel(
        self,
        channel,
        measurement_type,
        thermocouple_type="K"
    ):

        channel = str(channel)

        measurement_type = (
            measurement_type.lower()
        )

        if measurement_type == "voltage":

            self.write(
                f"CONF:VOLT:DC (@{channel})"
            )

        elif measurement_type == "current":

            self.write(
                f"CONF:CURR:DC (@{channel})"
            )

        elif measurement_type == "temperature":

            self.write(
                f"CONF:TEMP TC,"
                f"{thermocouple_type},"
                f"(@{channel})"
            )

        elif measurement_type == "resistance":

            self.write(
                f"CONF:RES (@{channel})"
            )

        else:

            raise ValueError(
                f"Unsupported measurement type: "
                f"{measurement_type}"
            )

    # =========================================================
    # CONFIGURE MULTIPLE CHANNELS
    # =========================================================

    def configure_channels(
        self,
        channel_config
    ):

        for channel, config in (
            channel_config.items()
        ):

            measurement_type = config.get(
                "type"
            )

            tc = config.get(
                "tc",
                "K"
            )

            self.configure_channel(
                channel,
                measurement_type,
                tc
            )

    # =========================================================
    # READ SINGLE CHANNEL
    # =========================================================

    def read_channel(
        self,
        channel
    ):

        response = self.query(
            f"MEAS? (@{channel})"
        )

        try:

            return float(
                response.split(",")[0]
            )

        except Exception:

            return None

    # =========================================================
    # READ MULTIPLE CHANNELS
    # =========================================================

    def read(
        self,
        channels
    ):

        if not channels:

            return {}

        channels = [
            str(ch)
            for ch in channels
        ]

        # -------------------------------------------------
        # If requested channels differ from scan list,
        # configure scan list again.
        # -------------------------------------------------

        if channels != self.scan_channels:

            channel_string = ",".join(
                channels
            )

            self.write(
                f"ROUT:SCAN (@{channel_string})"
            )

            self.scan_channels = channels

        # -------------------------------------------------
        # Start scan
        # -------------------------------------------------

        self.write(
            "INIT"
        )

        # -------------------------------------------------
        # Wait for operation to complete
        # -------------------------------------------------

        self.query(
            "*OPC?"
        )

        # -------------------------------------------------
        # Fetch results
        # -------------------------------------------------

        response = self.query(
            "FETC?"
        )

        values = [
            x.strip()
            for x in response.split(",")
        ]

        result = {}

        for channel, value in zip(
            channels,
            values
        ):

            try:

                result[channel] = float(
                    value
                )

            except Exception:

                result[channel] = None

        return result

    # =========================================================
    # FETCH
    # =========================================================

    def fetch(
        self,
        channels=None
    ):

        if channels is None:

            channels = self.scan_channels

        response = self.query(
            "FETC?"
        )

        values = [
            x.strip()
            for x in response.split(",")
        ]

        result = {}

        for channel, value in zip(
            channels,
            values
        ):

            try:

                result[str(channel)] = float(
                    value
                )

            except Exception:

                result[str(channel)] = None

        return result

    # =========================================================
    # IDENTITY
    # =========================================================

    def get_idn(self):

        return self.query(
            "*IDN?"
        )

    # =========================================================
    # ERROR
    # =========================================================

    def get_error(self):

        return self.query(
            "SYST:ERR?"
        )