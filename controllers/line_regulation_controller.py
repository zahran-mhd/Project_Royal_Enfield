import threading
import time


class LineRegulationController:

    def __init__(self, context):

        self.context = context
        # self.view = view

        self.running = False
        self.stop_requested = False

        self.current_step = 0
        self.total_steps = 0

        self.settings = None
        self.steps = []

    # ==================================================
    # LOAD SETTINGS
    # ==================================================

    def load_settings(self, dut_id):

        repository = self.context.test_repository

        # ----------------------------------------------
        # Common settings
        # ----------------------------------------------

        common = repository.get_line_common_settings(dut_id)

        if not common:
            raise ValueError(
                f"No Line Regulation common settings "
                f"found for DUT {dut_id}"
            )

        # ----------------------------------------------
        # Input settings
        # ----------------------------------------------

        input_setting = repository.get_obc_hv_dc_input_settings(dut_id)

        if not input_setting:
            raise ValueError(
                f"No OBC HV DC input settings "
                f"found for DUT {dut_id}"
            )

        input_setting_id = input_setting["input_setting_id"]

        # ----------------------------------------------
        # Output steps
        # ----------------------------------------------

        steps = repository.get_obc_hv_dc_output_settings(
            input_setting_id
        )

        if not steps:
            raise ValueError(
                f"No HV output steps found "
                f"for input setting {input_setting_id}"
            )

        self.settings = {
            "dut_id": dut_id,

            "dwell_time": common["dwell_time"],

            "dc_load_current": input_setting["dc_load_current"],
            "input_voltage": input_setting["input_voltage"],
            "input_frequency": input_setting["input_frequency"],
        }

        self.steps = steps
        self.total_steps = len(steps)

        return self.settings, self.steps

    # ==================================================
    # START TEST
    # ==================================================

    # def start_test(self, dut_id):

    #     if self.running:
    #         return

    #     self.stop_requested = False
    #     self.running = True

    #     try:

    #         self.load_settings(dut_id)

    #     except Exception as e:

    #         self.running = False

    #         self.view.show_error(
    #             "Line Regulation",
    #             str(e)
    #         )

    #         return

    #     # ----------------------------------------------
    #     # Update page with loaded settings
    #     # ----------------------------------------------

    #     self.view.update_test_settings(
    #         self.settings
    #     )

    #     # ----------------------------------------------
    #     # Run in background
    #     # ----------------------------------------------

    #     thread = threading.Thread(
    #         target=self._run_test,
    #         daemon=True
    #     )

    #     thread.start()


    def start_test(self, channel_id, values):

        if self.running:
            return

        self.running = True
        self.stop_requested = False

        threading.Thread(
            target=self._run_test,
            args=(channel_id, values),
            daemon=True
        ).start()

    # ==================================================
    # TEST SEQUENCE
    # ==================================================

    # def _run_test(self):

    #     try:

    #         for index, step in enumerate(self.steps):

    #             if self.stop_requested:
    #                 break

    #             self.current_step = index + 1

    #             # --------------------------------------
    #             # Step information
    #             # --------------------------------------

    #             hv_voltage = step["hv_voltage"]
    #             hv_current = step["hv_current"]

    #             ac_voltage = self.settings["input_voltage"]
    #             frequency = self.settings["input_frequency"]
    #             dwell_time = self.settings["dwell_time"]

    #             # --------------------------------------
    #             # Update UI
    #             # --------------------------------------

    #             self._update_step_ui(
    #                 step_no=self.current_step,
    #                 ac_voltage=ac_voltage,
    #                 frequency=frequency,
    #                 hv_voltage=hv_voltage,
    #                 hv_current=hv_current,
    #                 dwell_time=dwell_time
    #             )

    #             # --------------------------------------
    #             # Configure AC source
    #             # --------------------------------------

    #             self._set_ac_input(
    #                 voltage=ac_voltage,
    #                 frequency=frequency
    #             )

    #             # --------------------------------------
    #             # Configure HV load / source
    #             # --------------------------------------

    #             self._set_hv_output(
    #                 voltage=hv_voltage,
    #                 current=hv_current
    #             )

    #             # --------------------------------------
    #             # Wait / dwell
    #             # --------------------------------------

    #             self._dwell(dwell_time)

    #             # --------------------------------------
    #             # Read measurements
    #             # --------------------------------------

    #             if self.stop_requested:
    #                 break

    #             self._read_measurements()

    #         # ------------------------------------------
    #         # TEST COMPLETE
    #         # ------------------------------------------

    #         if not self.stop_requested:

    #             self.context.root.after(
    #                 0,
    #                 self.view.test_completed
    #             )

    #     except Exception as e:

    #         self.context.root.after(
    #             0,
    #             lambda e=e: self.view.test_failed(str(e))
    #         )

    #     finally:

    #         self.running = False

    def _run_test(self, channel_id, values):

        try:

            dut_id = values["dut_id"]

            # ==========================================
            # COMMON DWELL
            # ==========================================

            common = (
                self.context.parameter_repository
                .get_line_common_settings(dut_id)
            )

            if common is None:
                raise RuntimeError(
                    "Line Regulation common settings not found."
                )

            dwell_time = common["dwell_time"]

            # ==========================================
            # LOAD HV STEPS
            # ==========================================

            self.debug_line_settings(dut_id)

            hv_settings = (
                self.context.parameter_repository
                .get_obc_hv_dc_output_settings(dut_id)
            )

            if not hv_settings:
                raise RuntimeError(
                    "No HV DC output settings found."
                )

            # ==========================================
            # LOAD 3 AC SETTINGS
            # ==========================================

            ac_settings = (
                self.context.parameter_repository
                .get_obc_hv_dc_input_settings(dut_id)
            )

            if not ac_settings:
                raise RuntimeError(
                    "No AC input settings found."
                )

            print()
            print("====================================")
            print("LINE REGULATION TEST")
            print("====================================")

            print(
                "Dwell:",
                dwell_time,
                "sec"
            )

            print(
                "HV Steps:",
                len(hv_settings)
            )

            print(
                "AC Steps:",
                len(ac_settings)
            )

            # ==========================================
            # HV OUTER LOOP
            # ==========================================

            for hv_index, hv in enumerate(
                hv_settings
            ):

                if self.stop_requested:
                    break

                hv_step = hv_index + 1

                hv_voltage = hv["hv_voltage"]
                hv_current = hv["hv_current"]

                print()
                print(
                    "===================================="
                )

                print(
                    f"HV STEP {hv_step}/"
                    f"{len(hv_settings)}"
                )

                print(
                    f"HV Voltage = {hv_voltage} V"
                )

                print(
                    f"HV Current = {hv_current} A"
                )

                # ======================================
                # SET HV ONCE
                # ======================================

                self._set_hv_output(
                    voltage=hv_voltage,
                    current=hv_current
                )

                # ======================================
                # AC INNER LOOP
                # ======================================

                for ac_index, ac in enumerate(
                    ac_settings
                ):

                    if self.stop_requested:
                        break

                    ac_step = ac_index + 1

                    ac_voltage = ac["input_voltage"]
                    ac_frequency = ac["input_frequency"]

                    print()
                    print(
                        f"AC STEP {ac_step}/"
                        f"{len(ac_settings)}"
                    )

                    print(
                        f"AC Voltage = "
                        f"{ac_voltage} V"
                    )

                    print(
                        f"AC Frequency = "
                        f"{ac_frequency} Hz"
                    )

                    # ==================================
                    # SET AC
                    # ==================================

                    self._set_ac_input(
                        voltage=ac_voltage,
                        frequency=ac_frequency
                    )

                    # ==================================
                    # UPDATE GUI
                    # ==================================

                    self._update_page(
                        hv_step=hv_step,
                        total_hv_steps=len(hv_settings),

                        ac_step=ac_step,
                        total_ac_steps=len(ac_settings),

                        hv_voltage=hv_voltage,
                        hv_current=hv_current,

                        ac_voltage=ac_voltage,
                        ac_frequency=ac_frequency,

                        dwell_time=dwell_time
                    )

                    # ==================================
                    # DWELL
                    # ==================================

                    self._wait_dwell(
                        dwell_time
                    )

                    if self.stop_requested:
                        break

                    # ==================================
                    # MEASURE
                    # ==================================

                    self._measure(
                        channel_id=channel_id,

                        hv_voltage=hv_voltage,
                        hv_current=hv_current,

                        ac_voltage=ac_voltage,
                        ac_frequency=ac_frequency
                    )

            # ==========================================
            # COMPLETE
            # ==========================================

            if not self.stop_requested:

                self.context.root.after(
                    0,
                    self._test_completed
                )

        except Exception as e:

            print(
                "Line Regulation Error:",
                e
            )

            self.context.root.after(
                0,
                lambda e=e:
                self._test_failed(e)
            )

        finally:

            self.running = False


    def debug_line_settings(self, dut_id):

        cursor = self.context.db.conn.cursor()

        cursor.execute(
            "SELECT * FROM OBC_HV_DC_Input_Settings"
        )

        print("\n===== OBC_HV_DC_Input_Settings =====")

        for row in cursor.fetchall():
            print(dict(row))

        cursor.execute(
            "SELECT * FROM OBC_HV_DC_Output_Settings"
        )

        print("\n===== OBC_HV_DC_Output_Settings =====")

        for row in cursor.fetchall():
            print(dict(row))
    # ==================================================
    # UI UPDATE
    # ==================================================

    # def _update_step_ui(
    #     self,
    #     step_no,
    #     ac_voltage,
    #     frequency,
    #     hv_voltage,
    #     hv_current,
    #     dwell_time
    # ):

    #     self.context.root.after(
    #         0,
    #         lambda: self.view.update_active_step(
    #             step_no=step_no,
    #             total_steps=self.total_steps,
    #             ac_voltage=ac_voltage,
    #             frequency=frequency,
    #             hv_voltage=hv_voltage,
    #             hv_current=hv_current,
    #             dwell_time=dwell_time
    #         )
    #     )


    def _update_page(
        self,
        hv_step,
        total_hv_steps,
        ac_step,
        total_ac_steps,
        hv_voltage,
        hv_current,
        ac_voltage,
        ac_frequency,
        dwell_time
    ):

        def update():

            page = self.context.app_controller.pages.get(
                "Line Regulation"
            )

            if page is None:
                print(
                    "Line Regulation page not registered"
                )
                return

            page.update_active_step(
                hv_step=hv_step,
                total_hv_steps=total_hv_steps,

                ac_step=ac_step,
                total_ac_steps=total_ac_steps,

                hv_voltage=hv_voltage,
                hv_current=hv_current,

                ac_voltage=ac_voltage,
                ac_frequency=ac_frequency,

                dwell_time=dwell_time
            )

        self.context.root.after(
            0,
            update
        )
    # ==================================================
    # AC SOURCE
    # ==================================================

    def _set_ac_input(
        self,
        voltage,
        frequency
    ):

        print(
            f"AC SET -> "
            f"Voltage={voltage} V, "
            f"Frequency={frequency} Hz"
        )

        # ----------------------------------------------
        # Replace with your actual instrument
        # ----------------------------------------------

        # self.context.ac_source.set_voltage(voltage)
        # self.context.ac_source.set_frequency(frequency)
        # self.context.ac_source.output_on()

    # ==================================================
    # HV OUTPUT
    # ==================================================

    def _set_hv_output(
        self,
        voltage,
        current
    ):

        print(
            f"HV SET -> "
            f"Voltage={voltage} V, "
            f"Current={current} A"
        )

        # ----------------------------------------------
        # Replace with actual instrument
        # ----------------------------------------------

        # self.context.hv_source.set_voltage(voltage)
        # self.context.hv_source.set_current(current)
        # self.context.hv_source.output_on()

    # ==================================================
    # DWELL
    # ==================================================

    def _dwell(self, seconds):

        end_time = time.time() + seconds

        while time.time() < end_time:

            if self.stop_requested:
                return

            remaining = end_time - time.time()

            self.context.root.after(
                0,
                lambda remaining=remaining:
                    self.view.update_remaining_time(
                        max(0, remaining)
                    )
            )

            time.sleep(0.1)

    # ==================================================
    # MEASUREMENTS
    # ==================================================

    def _read_measurements(self):

        # ----------------------------------------------
        # Read CAN
        # ----------------------------------------------

        can_data = {}

        # Example:
        #
        # can_data = self.context.can_manager.get_values(...)

        # ----------------------------------------------
        # Read Power Analyzer
        # ----------------------------------------------

        analyzer_data = {}

        # Example:
        #
        # analyzer_data =
        #     self.context.power_analyzer.read()

        # ----------------------------------------------
        # Send values to GUI
        # ----------------------------------------------

        self.context.root.after(
            0,
            lambda: self.view.update_measurements(
                can_data,
                analyzer_data
            )
        )

    # ==================================================
    # STOP
    # ==================================================

    def stop_test(self):

        self.stop_requested = True

        # ----------------------------------------------
        # Hardware safe state
        # ----------------------------------------------

        try:
            self._stop_hardware()
        except Exception as e:
            print("Hardware stop error:", e)

    # ==================================================
    # HARDWARE STOP
    # ==================================================

    def _stop_hardware(self):

        print("Stopping Line Regulation hardware")

        # self.context.ac_source.output_off()
        # self.context.hv_source.output_off()

    # ==================================================
    # STATUS
    # ==================================================

    def is_running(self):

        return self.running