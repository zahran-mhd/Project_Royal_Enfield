class LiveTableController:

    def __init__(self, view, context):

        self.view = view
        self.context = context

        self.temperature_data = {}

        parameters = [
            "OBC_TEMP",
            "OBC_FET_TEMP",
            "HPDCDC_TEMP"
        ]

        self.temperature_data = {}

        for dut in range(1, 5):

            self.temperature_data[dut] = {
                "charging": {},
                "discharging": {}
            }

            for mode in ("charging", "discharging"):

                for parameter in parameters:

                    self.temperature_data[dut][mode][parameter] = {
                        "min": None,
                        "max": None
                    }
    def update_temperature(
            self,
            dut,
            mode,
            parameter,
            value
    ):

        value = float(value)

        data = self.temperature_data[dut][mode][parameter]

        if data["min"] is None or value < data["min"]:
            data["min"] = value

        if data["max"] is None or value > data["max"]:
            data["max"] = value

        self.update_statistics(dut)

    

    def update_statistics(self, dut):

        statistics = {}

        for mode in ("charging", "discharging"):

            highest = None
            lowest = None

            for parameter, values in self.temperature_data[dut][mode].items():

                if values["max"] is not None:

                    if highest is None or values["max"] > highest["value"]:

                        highest = {
                            "parameter": parameter,
                            "value": values["max"]
                        }

                if values["min"] is not None:

                    if lowest is None or values["min"] < lowest["value"]:

                        lowest = {
                            "parameter": parameter,
                            "value": values["min"]
                        }

            statistics[mode] = {
                "max": highest,
                "min": lowest
            }

        self.view.update_temperature_summary(
            dut,
            statistics
        )

    def reset(self, selected_duts):

        parameters = [
            "OBC_TEMP",
            "OBC_FET_TEMP",
            "HPDCDC_TEMP"
        ]

        for dut in selected_duts:

            self.temperature_data[dut] = {}

            for mode in ("charging", "discharging"):

                self.temperature_data[dut][mode] = {}

                for parameter in parameters:

                    self.temperature_data[dut][mode][parameter] = {
                        "min": None,
                        "max": None
                    }

        self.view.reset_display(selected_duts)