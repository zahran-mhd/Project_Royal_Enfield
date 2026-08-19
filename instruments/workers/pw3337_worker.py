import threading


class PW3337Worker(threading.Thread):

    def __init__(self, context, driver):

        super().__init__(daemon=True)

        self.context = context
        self.driver = driver

        self.stop_event = threading.Event()

        self.duts = self.get_connected_duts()


    def stop(self):

        self.stop_event.set()

    def run(self):
        while not self.stop_event.is_set():

            try:
                dut1, dut2 = self.duts
                read = self.driver.read()
                # print(read)

                # DUT A
                self.context.hardware_values[dut1] = {

                    "U1": read.get("U1"),
                    "I1": read.get("I1"),
                    "P1": read.get("P1"),
                    "U2": read.get("U2"),
                    "I2": read.get("I2"),
                    "P2": read.get("P2")
                }

                # DUT B
                self.context.hardware_values[dut2] = {
                    "U3": read.get("U3"),
                    "I3": read.get("I3"),
                    "P3": read.get("P3")

                    
                }

            except Exception as ex:

                print(f"PW3337 Error: {ex}")

            # print("Output : ",self.context.hardware_values)

            self.stop_event.wait(1)

    def get_connected_duts(self):

        configs = self.context.instrument_repository.get_all()

        for config in configs:

            if config.driver_class == "PW3337Driver" and config.address == self.driver.address:

                channel = config.channel_id

                if channel == 1:
                    return (1, 2)
                else:
                    return (3, 4)

        return ()

        # while not self.stop_event.is_set():

        #     try:

        #         read = (self.driver.read())

                
        #         # voltage = (
        #         #     self.driver.read_voltage()
        #         # )

        #         # current = (
        #         #     self.driver.read_current()
        #         # )

        #         # power = (
        #         #     self.driver.read_power()
        #         # )

        #         self.app.data_model.instrument_values[
        #             "PW3337"
        #         ] = {

        #             "Channel 1 Voltage": read.get('U1'),
        #             "Channel 2 Voltage": read.get('U2'),
        #             "Channel 3 Voltage": read.get('U3'),
        #             "Channel 1 Current": read.get('I1'),
        #             "Channel 2 Current": read.get('I2'),
        #             "Channel 3 Current": read.get('I3'),
        #             "Channel 1 Power": read.get('P1'),
        #             "Channel 2 Power": read.get('P2'),
        #             "Channel 3 Power": read.get('P3'),
        #             "Channel 1 Frequency": read.get('FREQU1'),
        #             "Channel 1 Power Factor": read.get('PF1')
        #         }

        #         # print(read)

        #     except Exception as ex:

        #         print(
        #             f"PW3337 Error: {ex}"
        #         )

        #     self.stop_event.wait(1)

        # self.driver.disconnect()