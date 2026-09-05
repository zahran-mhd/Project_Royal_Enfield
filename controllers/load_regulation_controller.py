import threading
import time


# ==========================================================
# LOAD REGULATION DUT -> PCAN PORT
# ==========================================================

LOAD_DUT_TO_CAN_PORT = {
    1: "PCAN_USBBUS1",
    2: "PCAN_USBBUS2",
    3: "PCAN_USBBUS3",
    4: "PCAN_USBBUS4",
}

# ==========================================================
# LOAD REGULATION - CAN PARAMETER MAP
# ==========================================================

LOAD_CAN_PARAMETER_MAP = {

    # AC input
    "Chrgr_Input_AC_Vlt":
        "Input AC Voltage",

    "Chrgr_Input_AC_Curr":
        "Input AC Current",

    # OBC DC output
    "Chrgr_Output_DC_Vlt":
        "Output OBC Voltage",

    "Chrgr_Output_DC_Curr":
        "Output OBC Current",

}


# ==========================================================
# LOAD REGULATION - HARDWARE / POWER ANALYZER MAP
# ==========================================================

LOAD_HARDWARE_PARAMETER_MAP = {

    # AC input
    "U1":
        "Input AC Voltage",

    "I1":
        "Input AC Current",

    "P1":
        "Input Power",

    # OBC DC output
    "U2":
        "Output OBC Voltage",

    "I2":
        "Output OBC Current",

    "P2":
        "Output Power",

}



class LoadRegulationController:

    LOAD_POINTS = [
        ("No Load", 0),
        ("25", 25),
        ("50", 50),
        ("75", 75),
        ("100", 100),
    ]

    def __init__(self, context):

        self.context = context

        self.running = False
        self.stop_requested = False

        self.current_hv_step = 0
        self.current_load_step = 0

        self.total_hv_steps = 0
        self.total_load_steps = 5

        self.settings = None
        self.steps = []

    # ==================================================
    # LOAD SETTINGS
    # ==================================================

    def load_settings(self, dut_id):

        repository = self.context.parameter_repository

        # --------------------------------------------------
        # COMMON SETTINGS
        # --------------------------------------------------

        common = repository.get_load_common(
            self.context.db.conn,
            dut_id
        )

        if not common:

            raise ValueError(
                f"No Load Regulation common settings "
                f"found for DUT {dut_id}"
            )

        # --------------------------------------------------
        # OBC CURRENT SETTINGS
        # --------------------------------------------------

        steps = repository.get_obc_current_settings(
            self.context.db.conn,
            dut_id
        )

        if not steps:

            raise ValueError(
                f"No OBC Load Regulation current settings "
                f"found for DUT {dut_id}"
            )

        # --------------------------------------------------
        # SETTINGS
        # --------------------------------------------------

        self.settings = {

            "dut_id": dut_id,

            "dwell_time":
                common["dwell_time"],

            "input_voltage":
                common["input_voltage"],

            "input_frequency":
                common["input_frequency"]

        }

        self.steps = steps

        return self.settings, self.steps

    # ==================================================
    # START TEST
    # ==================================================

    def start_test(self, channel_id, values):

        if self.running:

            print(
                "Load Regulation test is already running."
            )

            return

        self.running = True
        self.stop_requested = False

        self.current_hv_step = 0
        self.current_load_step = 0

        thread = threading.Thread(
            target=self._run_test,
            args=(channel_id, values),
            daemon=True
        )

        thread.start()

    # ==================================================
    # TEST SEQUENCE
    # ==================================================

    def _run_test(
        self,
        channel_id,
        values
    ):

        try:

            dut_id = values["dut_id"]

            # ==========================================
            # LOAD SETTINGS
            # ==========================================

            settings, hv_settings = (
                self.load_settings(dut_id)
            )

            dwell_time = float(
                settings["dwell_time"]
            )

            input_voltage = float(
                settings["input_voltage"]
            )

            input_frequency = float(
                settings["input_frequency"]
            )

            self.total_hv_steps = len(
                hv_settings
            )

            # ==========================================
            # DEBUG
            # ==========================================

            self.debug_load_settings(
                dut_id
            )

            # ==========================================
            # START MESSAGE
            # ==========================================

            print()
            print("=" * 40)
            print("LOAD REGULATION TEST")
            print("=" * 40)

            print(
                "DUT:",
                dut_id
            )

            print(
                "Input Voltage:",
                input_voltage,
                "V"
            )

            print(
                "Input Frequency:",
                input_frequency,
                "Hz"
            )

            print(
                "Dwell:",
                dwell_time,
                "sec"
            )

            print(
                "HV Steps:",
                self.total_hv_steps
            )

            print(
                "Load Steps:",
                self.total_load_steps
            )

            # ==========================================
            # SET AC INPUT
            # ==========================================

            self._set_ac_input(
                input_voltage,
                input_frequency
            )

            # ==========================================
            # HV OUTER LOOP
            # ==========================================

            for hv_index, hv_setting in enumerate(
                hv_settings,
                start=1
            ):

                if self.stop_requested:
                    break

                self.current_hv_step = hv_index

                hv_voltage = float(
                    hv_setting["hv_voltage"]
                )

                step_no = hv_setting["step_no"]

                # ======================================
                # CLEAR OLD MEASUREMENTS
                # ======================================

                self._clear_measurement_tables()

                print()
                print("=" * 40)
                print(
                    f"HV STEP "
                    f"{hv_index}/{self.total_hv_steps}"
                )

                print(
                    f"Step No     = {step_no}"
                )

                print(
                    f"HV Voltage  = {hv_voltage} V"
                )

                # ======================================
                # HV VOLTAGE
                # ======================================

                # For Load Regulation the HV voltage
                # stays fixed while the current changes.

                # ======================================
                # LOAD LOOP
                # ======================================

                for load_index, (
                    load_name,
                    load_percent
                ) in enumerate(
                    self.LOAD_POINTS,
                    start=1
                ):

                    if self.stop_requested:
                        break

                    self.current_load_step = load_index

                    # ==================================
                    # GET CURRENT FROM DB
                    # ==================================

                    hv_current = hv_setting[
                        "loads"
                    ].get(
                        load_name
                    )

                    if hv_current is None:

                        raise ValueError(
                            f"Current not found for "
                            f"HV={hv_voltage} V, "
                            f"Load={load_percent}%"
                        )

                    hv_current = float(
                        hv_current
                    )

                    # ==================================
                    # PRINT
                    # ==================================

                    print()
                    print(
                        f"LOAD STEP "
                        f"{load_index}/5"
                    )

                    print(
                        f"HV Voltage = "
                        f"{hv_voltage} V"
                    )

                    print(
                        f"HV Load = "
                        f"{load_percent}%"
                    )

                    print(
                        f"HV Current = "
                        f"{hv_current} A"
                    )

                    # ==================================
                    # SET HV OUTPUT
                    # ==================================

                    self._set_hv_output(
                        voltage=hv_voltage,
                        current=hv_current
                    )

                    # ==================================
                    # UPDATE GUI
                    # ==================================

                    self._update_page(
                        hv_step=hv_index,
                        total_hv_steps=self.total_hv_steps,

                        load_step=load_index,
                        total_load_steps=5,

                        hv_voltage=hv_voltage,
                        hv_current=hv_current,

                        load_percent=load_percent,

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

                    # self._measure(
                    #     channel_id=channel_id,

                    #     hv_step=hv_index,
                    #     load_step=load_index,

                    #     hv_voltage=hv_voltage,
                    #     hv_current=hv_current,

                    #     load_percent=load_percent
                    # )

            
                    self._measure(
                        channel_id=channel_id,
                        dut_id=dut_id,
                        hv_step=hv_index,
                        load_step=load_index,
                        hv_voltage=hv_voltage,
                        hv_current=hv_current,
                        load_percent=load_percent
                    )
                


            # ==========================================
            # COMPLETE / STOP
            # ==========================================

            if self.stop_requested:

                self.context.root.after(
                    0,
                    self._test_stopped
                )

            else:

                self.context.root.after(
                    0,
                    self._test_completed
                )

        except Exception as e:

            print()
            print("=" * 40)
            print("LOAD REGULATION ERROR")
            print("=" * 40)

            print(e)

            self.context.root.after(
                0,
                lambda error=e:
                    self._test_failed(error)
            )

        finally:

            self.running = False

    # ==================================================
    # DEBUG SETTINGS
    # ==================================================

    def debug_load_settings(
        self,
        dut_id
    ):

        cursor = self.context.db.conn.cursor()

        # --------------------------------------------------
        # COMMON
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM HV_DC_Common_Settings
            WHERE dut_id = ?
            """,
            (dut_id,)
        )

        print(
            "\n===== HV_DC_Common_Settings ====="
        )

        for row in cursor.fetchall():

            print(
                dict(row)
            )

        # --------------------------------------------------
        # OBC
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM OBC_HV_DC_Current_Settings
            WHERE dut_id = ?
            ORDER BY hv_voltage, step_no, load_percent
            """,
            (dut_id,)
        )

        print(
            "\n===== OBC_HV_DC_Current_Settings ====="
        )

        for row in cursor.fetchall():

            print(
                dict(row)
            )

        # --------------------------------------------------
        # HPDC
        # --------------------------------------------------

        cursor.execute(
            """
            SELECT *
            FROM HPDC_HV_DC_Current_Settings
            WHERE dut_id = ?
            ORDER BY hv_voltage, step_no, load_percent
            """,
            (dut_id,)
        )

        print(
            "\n===== HPDC_HV_DC_Current_Settings ====="
        )

        for row in cursor.fetchall():

            print(
                dict(row)
            )

    # ==================================================
    # UI UPDATE
    # ==================================================

    def _update_page(
        self,
        hv_step,
        total_hv_steps,

        load_step,
        total_load_steps,

        hv_voltage,
        hv_current,

        load_percent,

        dwell_time
    ):

        def update():

            page = (
                self.context
                .app_controller
                .pages
                .get("Load Regulation")
            )

            if page is None:

                print(
                    "Load Regulation page "
                    "not registered"
                )

                return

            # ------------------------------------------
            # HV SUBTITLE
            # ------------------------------------------

            page.can_sub_title.config(
                text=(
                    f"HV Step "
                    f"{hv_step}/{total_hv_steps}"
                    f"   |   "
                    f"HV Voltage: "
                    f"{hv_voltage:.1f} Vdc"
                    f"   |   "
                    f"HV Current: "
                    f"{hv_current:.2f} A"
                    f"   |   "
                    f"Load: "
                    f"{load_percent}%"
                )
            )

            page.analyzer_sub_title.config(
                text=(
                    f"HV Step "
                    f"{hv_step}/{total_hv_steps}"
                    f"   |   "
                    f"HV Voltage: "
                    f"{hv_voltage:.1f} Vdc"
                    f"   |   "
                    f"HV Current: "
                    f"{hv_current:.2f} A"
                    f"   |   "
                    f"Load: "
                    f"{load_percent}%"
                )
            )

            # ------------------------------------------
            # UPDATE ACTIVE ROW
            # ------------------------------------------

            page.update_active_row(
                load_step=load_step,
                load_percent=load_percent,
                hv_voltage=hv_voltage,
                hv_current=hv_current
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
        # Actual instrument
        # ----------------------------------------------

        # self.context.ac_source.set_voltage(
        #     voltage
        # )
        #
        # self.context.ac_source.set_frequency(
        #     frequency
        # )
        #
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
        # Actual instrument
        # ----------------------------------------------

        # self.context.hv_source.set_voltage(
        #     voltage
        # )
        #
        # self.context.hv_source.set_current(
        #     current
        # )
        #
        # self.context.hv_source.output_on()

    # ==================================================
    # DWELL
    # ==================================================

    def _wait_dwell(
        self,
        seconds
    ):

        seconds = float(
            seconds
        )

        end_time = (
            time.time() + seconds
        )

        while time.time() < end_time:

            if self.stop_requested:
                return

            remaining = max(
                0,
                end_time - time.time()
            )

            print(
                f"\rDwell remaining: "
                f"{remaining:.1f} sec",
                end=""
            )

            time.sleep(
                0.1
            )

        print()

    # ==================================================
    # MEASURE
    # ==================================================

    # def _measure(
    #     self,
    #     channel_id,

    #     hv_step,
    #     load_step,

    #     hv_voltage,
    #     hv_current,

    #     load_percent
    # ):

    #     print(
    #         "MEASURE -> "
    #         f"HV Step={hv_step}, "
    #         f"Load Step={load_step}, "
    #         f"HV={hv_voltage} V, "
    #         f"Current={hv_current} A, "
    #         f"Load={load_percent}%"
    #     )

    #     # ==============================================
    #     # CAN
    #     # ==============================================

    #     can_data = {}

    #     # Example:
    #     #
    #     # can_data = (
    #     #     self.context.can_manager
    #     #     .get_values(channel_id)
    #     # )

    #     # ==============================================
    #     # POWER ANALYZER
    #     # ==============================================

    #     analyzer_data = {}

    #     # Example:
    #     #
    #     # analyzer_data = (
    #     #     self.context.power_analyzer
    #     #     .read()
    #     # )

    #     # ==============================================
    #     # UPDATE GUI
    #     # ==============================================

    #     def update():

    #         page = (
    #             self.context
    #             .app_controller
    #             .pages
    #             .get("Load Regulation")
    #         )

    #         if page is None:
    #             return

    #         page.update_can_row(
    #             load_step=load_step,
    #             can_data=can_data
    #         )

    #         page.update_power_analyzer_row(
    #             load_step=load_step,
    #             analyzer_data=analyzer_data
    #         )

    #     self.context.root.after(
    #         0,
    #         update
    #     )


    
    def _measure(
        self,
        channel_id,
        dut_id,
        hv_step,
        load_step,
        hv_voltage,
        hv_current,
        load_percent
    ):
        """
        Capture Load Regulation measurement for one explicit DUT.

        This function is independent of LiveTableFrame.

        dut_id:
            Explicit DUT being tested.

        CAN source:
            context.can_values

        Hardware source:
            context.hardware_values
        """

        print(
            "\n========================================"
        )
        print("LOAD REGULATION MEASUREMENT")
        print("========================================")

        print(
            f"DUT          = {dut_id}"
        )

        print(
            f"Channel      = {channel_id}"
        )

        print(
            f"HV Step      = {hv_step}"
        )

        print(
            f"Load Step    = {load_step}"
        )

        print(
            f"HV Voltage   = {hv_voltage} V"
        )

        print(
            f"HV Current   = {hv_current} A"
        )

        print(
            f"Load         = {load_percent}%"
        )

        # ==========================================================
        # CAN DATA
        # ==========================================================

        # can_data = {}

        # # ----------------------------------------------------------
        # # Get CAN data specifically for this DUT
        # # ----------------------------------------------------------

        # dut_can_data = self.context.can_values.get(
        #     dut_id,
        #     {}
        # )

        # print(
        #     f"Raw CAN data for DUT{dut_id}: "
        #     f"{dut_can_data}"
        # )

        
        # # ==========================================================
        # # GET CAN DATA FOR EXPLICIT DUT
        # # ==========================================================

        # can_data = {}

        # can_port = LOAD_DUT_TO_CAN_PORT.get(
        #     dut_id
        # )

        # if can_port is None:

        #     print(
        #         f"No CAN port configured for DUT{dut_id}"
        #     )

        # else:

        #     for group, ports in (
        #         self.context.can_values.items()
        #     ):

        #         signals = ports.get(
        #             can_port
        #         )

        #         if not signals:
        #             continue

        #         for signal, value in signals.items():

        #             parameter = LOAD_CAN_PARAMETER_MAP.get(
        #                 signal
        #             )

        #             if parameter is None:
        #                 continue

        #             try:

        #                 can_data[parameter] = float(
        #                     value
        #                 )

        #             except (
        #                 TypeError,
        #                 ValueError
        #             ):

        #                 continue



        # # ----------------------------------------------------------
        # # Convert CAN signal names
        # # ----------------------------------------------------------

        # for signal, value in dut_can_data.items():

        #     parameter = LOAD_CAN_PARAMETER_MAP.get(
        #         signal
        #     )

        #     if parameter is None:
        #         continue

        #     try:

        #         can_data[parameter] = float(value)

        #     except (
        #         TypeError,
        #         ValueError
        #     ):

        #         continue


        # ==========================================================
        # CAN DATA
        # ==========================================================

        can_data = {}

        # ----------------------------------------------------------
        # Get CAN port for explicit DUT
        # ----------------------------------------------------------

        can_port = LOAD_DUT_TO_CAN_PORT.get(dut_id)

        if can_port is None:

            print(
                f"No CAN port configured for DUT{dut_id}"
            )

        else:

            # ------------------------------------------------------
            # Get data for this test channel
            # ------------------------------------------------------

            channel_data = self.context.can_values.get(
                channel_id,
                {}
            )

            # ------------------------------------------------------
            # Get data from this DUT's CAN port
            # ------------------------------------------------------

            dut_can_data = channel_data.get(
                can_port,
                {}
            )

            print(
                f"Raw CAN data for DUT{dut_id} "
                f"({can_port}): {dut_can_data}"
            )

            # ------------------------------------------------------
            # Convert CAN signal names
            # ------------------------------------------------------

            for signal, value in dut_can_data.items():

                parameter = LOAD_CAN_PARAMETER_MAP.get(
                    signal
                )

                if parameter is None:
                    continue

                try:

                    can_data[parameter] = float(value)

                except (
                    TypeError,
                    ValueError
                ):

                    continue

        # ==========================================================
        # CAN POWER CALCULATION
        # ==========================================================

        can_input_voltage = can_data.get(
            "Input AC Voltage",
            0.0
        )

        can_input_current = can_data.get(
            "Input AC Current",
            0.0
        )

        can_output_voltage = can_data.get(
            "Output OBC Voltage",
            0.0
        )

        can_output_current = can_data.get(
            "Output OBC Current",
            0.0
        )

        # ----------------------------------------------------------
        # Input Power
        # ----------------------------------------------------------

        can_input_power = (
            can_input_voltage *
            can_input_current *
            0.99
        )

        # ----------------------------------------------------------
        # Output Power
        # ----------------------------------------------------------

        can_output_power = (
            can_output_voltage *
            can_output_current
        )

        # ----------------------------------------------------------
        # Efficiency
        # ----------------------------------------------------------

        if can_input_power > 0:

            can_efficiency = (
                can_output_power /
                can_input_power
            ) * 100.0

        else:

            can_efficiency = 0.0

        can_data["Input Power"] = (
            can_input_power
        )

        can_data["Output Power"] = (
            can_output_power
        )

        can_data["Efficiency"] = (
            can_efficiency
        )

        # ==========================================================
        # LOAD REGULATION
        # ==========================================================

        # Load regulation will be calculated after the no-load
        # output voltage is available.
        #
        # For now, keep it empty until the controller has a
        # reference/no-load voltage.

        can_data["Load Regulation"] = None

        print(
            f"CAN DATA DUT{dut_id}:"
        )

        for parameter, value in can_data.items():

            print(
                f"    {parameter}: {value}"
            )

        # ==========================================================
        # HARDWARE / POWER ANALYZER DATA
        # ==========================================================

        analyzer_data = {}

        dut_hardware_data = (
            self.context.hardware_values.get(
                dut_id,
                {}
            )
        )

        print(
            f"Raw Hardware data for DUT{dut_id}: "
            f"{dut_hardware_data}"
        )

        # ----------------------------------------------------------
        # Convert hardware signal names
        # ----------------------------------------------------------

        for signal, value in dut_hardware_data.items():

            parameter = LOAD_HARDWARE_PARAMETER_MAP.get(
                signal
            )

            if parameter is None:
                continue

            try:

                analyzer_data[parameter] = float(
                    value
                )

            except (
                TypeError,
                ValueError
            ):

                continue

        # ==========================================================
        # POWER ANALYZER POWER
        # ==========================================================

        analyzer_input_voltage = analyzer_data.get(
            "Input AC Voltage",
            0.0
        )

        analyzer_input_current = analyzer_data.get(
            "Input AC Current",
            0.0
        )

        analyzer_output_voltage = analyzer_data.get(
            "Output OBC Voltage",
            0.0
        )

        analyzer_output_current = analyzer_data.get(
            "Output OBC Current",
            0.0
        )

        # ----------------------------------------------------------
        # Input Power
        #
        # If P1 is already supplied by the analyzer, use it.
        # Otherwise calculate V x I.
        # ----------------------------------------------------------

        if "Input Power" not in analyzer_data:

            analyzer_input_power = (
                analyzer_input_voltage *
                analyzer_input_current
            )

            analyzer_data["Input Power"] = (
                analyzer_input_power
            )

        else:

            analyzer_input_power = (
                analyzer_data["Input Power"]
            )

        # ----------------------------------------------------------
        # Output Power
        #
        # If P2 is supplied, use it.
        # Otherwise calculate V x I.
        # ----------------------------------------------------------

        if "Output Power" not in analyzer_data:

            analyzer_output_power = (
                analyzer_output_voltage *
                analyzer_output_current
            )

            analyzer_data["Output Power"] = (
                analyzer_output_power
            )

        else:

            analyzer_output_power = (
                analyzer_data["Output Power"]
            )

        # ----------------------------------------------------------
        # Efficiency
        # ----------------------------------------------------------

        if analyzer_input_power > 0:

            analyzer_efficiency = (
                analyzer_output_power /
                analyzer_input_power
            ) * 100.0

        else:

            analyzer_efficiency = 0.0

        analyzer_data["Efficiency"] = (
            analyzer_efficiency
        )

        # ==========================================================
        # LOAD REGULATION
        # ==========================================================

        analyzer_data["Load Regulation"] = None

        print(
            f"POWER ANALYZER DATA DUT{dut_id}:"
        )

        for parameter, value in analyzer_data.items():

            print(
                f"    {parameter}: {value}"
            )

        # ==========================================================
        # UPDATE LOAD REGULATION PAGE
        # ==========================================================

        page = (
            self.context.app_controller.pages.get(
                "Load Regulation"
            )
        )

        if page is None:

            print(
                "Load Regulation page not found."
            )

            return

        # ==========================================================
        # TKINTER MAIN THREAD
        # ==========================================================

        def update():

            try:

                if not page.winfo_exists():
                    return

                # --------------------------------------------------
                # CAN TABLE
                # --------------------------------------------------

                page.update_can_row(
                    load_step=load_step,
                    can_data=can_data
                )

                # --------------------------------------------------
                # POWER ANALYZER TABLE
                # --------------------------------------------------

                page.update_power_analyzer_row(
                    load_step=load_step,
                    analyzer_data=analyzer_data
                )

            except Exception as e:

                print(
                    "Load Regulation measurement "
                    f"UI error: {e}"
                )

        self.context.root.after(
            0,
            update
        )

    # ==================================================
    # CLEAR TABLES
    # ==================================================

    def _clear_measurement_tables(
        self
    ):

        def clear():

            page = (
                self.context
                .app_controller
                .pages
                .get("Load Regulation")
            )

            if page is None:

                print(
                    "Load Regulation page "
                    "not found"
                )

                return

            page.clear_measurement_tables()

        self.context.root.after(
            0,
            clear
        )

    # ==================================================
    # TEST COMPLETED
    # ==================================================

    def _test_completed(
        self
    ):

        print()
        print("=" * 40)
        print("LOAD REGULATION TEST COMPLETED")
        print("=" * 40)

        try:

            page = (
                self.context
                .app_controller
                .pages
                .get("Load Regulation")
            )

            if page is not None:

                page.test_completed()

        except Exception as e:

            print(
                "Completion UI error:",
                e
            )

    # ==================================================
    # TEST FAILED
    # ==================================================

    def _test_failed(
        self,
        error
    ):

        print()
        print("=" * 40)
        print("LOAD REGULATION TEST FAILED")
        print("=" * 40)

        print(
            error
        )

        try:

            page = (
                self.context
                .app_controller
                .pages
                .get("Load Regulation")
            )

            if page is not None:

                page.test_failed(
                    str(error)
                )

        except Exception as e:

            print(
                "Failure UI error:",
                e
            )

    # ==================================================
    # TEST STOPPED
    # ==================================================

    def _test_stopped(
        self
    ):

        print()
        print("=" * 40)
        print("LOAD REGULATION TEST STOPPED")
        print("=" * 40)

        try:

            page = (
                self.context
                .app_controller
                .pages
                .get("Load Regulation")
            )

            if page is not None:

                page.test_stopped()

        except Exception as e:

            print(
                "Stop UI error:",
                e
            )

    # ==================================================
    # STOP
    # ==================================================

    def stop_test(
        self
    ):

        print(
            "Stop requested for "
            "Load Regulation"
        )

        self.stop_requested = True

        try:

            self._stop_hardware()

        except Exception as e:

            print(
                "Hardware stop error:",
                e
            )

    # ==================================================
    # HARDWARE STOP
    # ==================================================

    def _stop_hardware(
        self
    ):

        print(
            "Stopping Load Regulation hardware"
        )

        # self.context.ac_source.output_off()
        # self.context.hv_source.output_off()

    # ==================================================
    # STATUS
    # ==================================================

    def is_running(
        self
    ):

        return self.running