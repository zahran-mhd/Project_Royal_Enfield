from pymodbus.client import ModbusTcpClient


class Adam6052Driver:

    def __init__(
        self,
        ip_address,
        port=502,
        timeout=2
    ):
        self.ip_address = ip_address
        self.port = port
        self.timeout = timeout

        self.client = None

    # ==========================================================
    # CONNECTION
    # ==========================================================

    def connect(self):

        if self.client is not None:
            return True

        self.client = ModbusTcpClient(
            host=self.ip_address,
            port=self.port,
            timeout=self.timeout
        )

        connected = self.client.connect()

        if connected:

            print(
                f"ADAM-6052 connected: "
                f"{self.ip_address}:{self.port}"
            )

            return True

        self.client = None

        raise ConnectionError(
            f"Failed to connect to ADAM-6052 "
            f"{self.ip_address}:{self.port}"
        )

    def disconnect(self):

        if self.client:

            self.client.close()

            print(
                f"ADAM-6052 disconnected: "
                f"{self.ip_address}"
            )

            self.client = None

    # ==========================================================
    # CONNECTION CHECK
    # ==========================================================

    def _check_connection(self):

        if self.client is None:
            raise RuntimeError(
                "ADAM-6052 is not connected"
            )

    # ==========================================================
    # DIGITAL INPUT
    # ==========================================================

    def read_input(
        self,
        input_port
    ):

        """
        Read one digital input.

        input_port:
            0 -> DI0
            1 -> DI1
            2 -> DI2
            ...
        """

        self._check_connection()

        if not 0 <= input_port <= 11:
            raise ValueError(
                "ADAM-6052 input port must be 0-11"
            )

        result = self.client.read_discrete_inputs(
            address=input_port,
            count=1
        )

        if result.isError():
            raise RuntimeError(
                f"Failed to read DI{input_port}: "
                f"{result}"
            )

        return bool(result.bits[0])

    # ==========================================================
    # READ ALL DIGITAL INPUTS
    # ==========================================================

    def read_all_inputs(self):

        self._check_connection()

        result = self.client.read_discrete_inputs(
            address=0,
            count=12
        )

        if result.isError():
            raise RuntimeError(
                f"Failed to read ADAM inputs: "
                f"{result}"
            )

        return {
            port: bool(result.bits[port])
            for port in range(12)
        }

    # ==========================================================
    # DIGITAL OUTPUT
    # ==========================================================

    def write_output(
        self,
        output_port,
        value
    ):

        """
        Write one digital output.

        output_port:
            0 -> DO0
            1 -> DO1
            ...
            7 -> DO7

        value:
            0 / False -> OFF
            1 / True  -> ON
        """

        self._check_connection()

        if not 0 <= output_port <= 7:
            raise ValueError(
                "ADAM-6052 output port must be 0-7"
            )

        value = bool(value)

        result = self.client.write_coil(
            address=output_port+16,
            value=value
        )

        if result.isError():
            raise RuntimeError(
                f"Failed to write DO{output_port}: "
                f"{result}"
            )

        return True

    # ==========================================================
    # READ OUTPUT
    # ==========================================================

    def read_output(
        self,
        output_port
    ):

        self._check_connection()

        if not 0 <= output_port <= 7:
            raise ValueError(
                "ADAM-6052 output port must be 0-7"
            )

        result = self.client.read_coils(
            address=output_port,
            count=1
        )

        if result.isError():
            raise RuntimeError(
                f"Failed to read DO{output_port}: "
                f"{result}"
            )

        return bool(result.bits[0])

    # ==========================================================
    # READ ALL OUTPUTS
    # ==========================================================

    def read_all_outputs(self):

        self._check_connection()

        result = self.client.read_coils(
            address=0,
            count=8
        )

        if result.isError():
            raise RuntimeError(
                f"Failed to read ADAM outputs: "
                f"{result}"
            )

        return {
            port: bool(result.bits[port])
            for port in range(8)
        }

    # ==========================================================
    # WRITE MULTIPLE OUTPUTS
    # ==========================================================

    def write_outputs(
        self,
        outputs
    ):

        """
        Example:

        {
            0: True,
            1: False,
            2: True
        }
        """

        for port, value in outputs.items():

            self.write_output(
                port,
                value
            )

    # ==========================================================
    # TURN ALL OUTPUTS OFF
    # ==========================================================

    def all_outputs_off(self):

        for port in range(8):

            self.write_output(
                port,
                False
            )

    # ==========================================================
    # TEST-SPECIFIC FUNCTIONS
    # ==========================================================

    # def set_charge_mode(
    #     self,
    #     charge_output=0,
    #     discharge_output=1
    # ):

    #     self.write_output(
    #         charge_output,
    #         True
    #     )

    #     self.write_output(
    #         discharge_output,
    #         False
    #     )

    def set_charge_mode(self):

        outputs = {
            0: True,
            1: False,
            2: True,
            3: True,
            4: False,
            5: True,
            6: True,
            7: False
        }

        self.write_outputs(outputs)

    def set_discharge_mode(self):
    
            outputs = {
                0: True,
                1: False,
                2: True,
                3: True,
                4: False,
                5: True,
                6: True,
                7: False
            }
    
            self.write_outputs(outputs)

    # def set_discharge_mode(
    #     self,
    #     charge_output=0,
    #     discharge_output=1
    # ):

    #     self.write_output(
    #         charge_output,
    #         False
    #     )

    #     self.write_output(
    #         discharge_output,
    #         True
    #     )

    def output_off(
        self,
        charge_output=0,
        discharge_output=1
    ):

        self.write_output(
            charge_output,
            False
        )

        self.write_output(
            discharge_output,
            False
        )