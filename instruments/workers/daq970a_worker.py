import threading


DAQ_TEMPERATURE_MAP = {

    "DUT1": {
        "T1": "101",
        "T2": "102",
        "T3": "103",
        "T4": "104",
        "T5": "105",
        "T6": "106",
        "T7": "107",
        "T8": "108",
        "T9": "109",
        "T10": "110",
    },

    "DUT2": {
        "T1": "111",
        "T2": "112",
        "T3": "113",
        "T4": "114",
        "T5": "115",
        "T6": "116",
        "T7": "117",
        "T8": "118",
        "T9": "119",
        "T10": "120",
    }

}


class DAQ970AWorker(threading.Thread):

    def __init__(
        self,
        context,
        driver,
        instrument_id,
        interval=1.0
    ):

        super().__init__(
            daemon=True
        )

        self.context = context
        self.driver = driver
        self.instrument_id = instrument_id
        self.interval = interval

        self.stop_event = threading.Event()

    # =====================================================
    # STOP
    # =====================================================

    def stop(self):

        self.stop_event.set()

    # =====================================================
    # GET CHANNELS
    # =====================================================

    def get_temperature_channels(self):

        channels = []

        for dut_config in (
            DAQ_TEMPERATURE_MAP.values()
        ):

            for channel in dut_config.values():

                if channel not in channels:

                    channels.append(channel)

        return channels

    # =====================================================
    # CONFIGURE
    # =====================================================

    def configure(self):

        channels = (
            self.get_temperature_channels()
        )

        print(
            "DAQ channels:",
            channels
        )

        self.driver.configure_temperature(
            channels,
            thermocouple_type="K"
        )

    # =====================================================
    # RUN
    # =====================================================

    def run(self):

        print(
            "======================================"
        )

        print(
            "DAQ970A WORKER STARTED"
        )

        print(
            "Instrument ID:",
            self.instrument_id
        )

        print(
            "Driver:",
            type(self.driver).__name__
        )

        print(
            "======================================"
        )

        # -------------------------------------------------
        # Configure
        # -------------------------------------------------

        try:

            self.configure()

            print(
                "DAQ configuration successful"
            )

        except Exception as ex:

            print(
                "DAQ configuration failed:",
                ex
            )

            import traceback
            traceback.print_exc()

            return

        # -------------------------------------------------
        # Read loop
        # -------------------------------------------------

        while not self.stop_event.is_set():

            try:

                channels = (
                    self.get_temperature_channels()
                )

                print(
                    "Reading DAQ:",
                    channels
                )

                values = self.driver.read(
                    channels
                )

                print(
                    "DAQ raw values:",
                    values
                )

                self.update_temperature_values(
                    values
                )

            except Exception as ex:

                print(
                    "DAQ read error:",
                    ex
                )

                import traceback
                traceback.print_exc()

            self.stop_event.wait(
                self.interval
            )

        print(
            "DAQ970A worker stopped"
        )

    # =====================================================
    # UPDATE DATA MODEL
    # =====================================================

    def update_temperature_values(
        self,
        values
    ):

        temperature_data = {}

        for dut, parameters in (
            DAQ_TEMPERATURE_MAP.items()
        ):

            temperature_data[dut] = {}

            for parameter, physical_channel in (
                parameters.items()
            ):

                value = values.get(
                    physical_channel
                )

                temperature_data[dut][
                    parameter
                ] = value

        # -------------------------------------------------
        # Data model
        # -------------------------------------------------

        if not hasattr(
            self.context.data_model,
            "instrument_values"
        ):

            self.context.data_model.instrument_values = {}

        self.context.data_model.instrument_values[
            self.instrument_id
        ] = temperature_data

        print(
            "DAQ DATA MODEL:"
        )

        print(
            self.context.data_model.instrument_values[
                self.instrument_id
            ]
        )