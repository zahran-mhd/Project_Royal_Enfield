import csv
import os
import re
from datetime import datetime


class CSVLogger:

    # These are the common parameters that can come
    # from both CAN and hardware.
    COMMON_PARAMETERS = [
        "OBC Input Voltage",
        "OBC Input Current",
        "OBC Output Voltage",
        "OBC Output Current",
        "OBC_Input_Power",
        "OBC_Output_Power",
        "OBC Efficiency",

        "HPDCDC Input Voltage",
        "HPDCDC Input Current",
        "HPDCDC Output Voltage",
        "HPDCDC Output Current",
        "HPDCDC_Input_Power",
        "HPDCDC_Output_Power",
        "HPDCDC_Efficiency",

        "OBC_TEMP",
        "OBC_FET_TEMP",
        "HPDCDC_TEMP",
    ]

    def __init__(self, base_folder="CSV_Logs"):

        self.base_folder = base_folder

        self.files = {}
        self.writers = {}

    # ==========================================================
    # SANITIZE FILE/FOLDER NAME
    # ==========================================================

    def sanitize_name(self, name):

        name = str(name)

        return re.sub(
            r'[<>:"/\\|?*]',
            "_",
            name
        )

    def start_test(self, test_name):

        test_name = self.sanitize_name(test_name)

        # Generate timestamp ONCE for this test
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

        self.test_folder = os.path.join(
            self.base_folder,
            f"{test_name}_{timestamp}"
        )

        os.makedirs(
            self.test_folder,
            exist_ok=True
        )

        print(
            f"CSV test folder created: {self.test_folder}"
        )

    # ==========================================================
    # CREATE CSV
    # ==========================================================

    def start_cycle(self, dut_no, cycle_no):

        dut_folder = os.path.join(
            self.test_folder,
            f"DUT{dut_no}"
        )

        os.makedirs(dut_folder, exist_ok=True)

        file_path = os.path.join(
            dut_folder,
            f"Cycle_{cycle_no}.csv"
        )

        file = open(
            file_path,
            "w",
            newline="",
            encoding="utf-8"
        )

        # ======================================================
        # CSV COLUMNS
        # ======================================================

        headers = [
            "Timestamp",
            "Time_sec",
            "Mode"
        ]

        # CAN columns
        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"CAN_{parameter}"
            )

        # Hardware columns
        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"HW_{parameter}"
            )

        writer = csv.DictWriter(
            file,
            fieldnames=headers
        )

        writer.writeheader()

        key = (
            dut_no,
            cycle_no
        )

        self.files[key] = file
        self.writers[key] = writer

        print(
            f"CSV started: {file_path}"
        )

    # def start_cycle(
    #     self,
    #     test_name,
    #     dut_no,
    #     cycle_no
    # ):

    #     test_name = self.sanitize_name(
    #         test_name
    #     )

    #     dut_folder = os.path.join(
    #         self.base_folder,
    #         test_name,
    #         f"DUT{dut_no}"
    #     )

    #     os.makedirs(
    #         dut_folder,
    #         exist_ok=True
    #     )

    #     file_path = os.path.join(
    #         dut_folder,
    #         f"Cycle_{cycle_no}.csv"
    #     )

    #     file = open(
    #         file_path,
    #         "w",
    #         newline="",
    #         encoding="utf-8"
    #     )

    #     # ======================================================
    #     # CSV COLUMNS
    #     # ======================================================

    #     headers = [
    #         "Timestamp",
    #         "Time_sec",
    #         "Mode"
    #     ]

    #     # CAN columns
    #     for parameter in self.COMMON_PARAMETERS:

    #         headers.append(
    #             f"CAN_{parameter}"
    #         )

    #     # Hardware columns
    #     for parameter in self.COMMON_PARAMETERS:

    #         headers.append(
    #             f"HW_{parameter}"
    #         )

    #     writer = csv.DictWriter(
    #         file,
    #         fieldnames=headers
    #     )

    #     writer.writeheader()

    #     key = (
    #         dut_no,
    #         cycle_no
    #     )

    #     self.files[key] = file
    #     self.writers[key] = writer

    #     print(
    #         f"CSV started: {file_path}"
    #     )

    # ==========================================================
    # WRITE ONE SECOND OF DATA
    # ==========================================================

    def write_row(
        self,
        dut_no,
        cycle_no,
        elapsed_seconds,
        mode,
        can_values,
        hardware_values
    ):

        # print("\n========== CSV LOG ==========")
        # print("DUT       :", dut_no)
        # print("Cycle     :", cycle_no)
        # print("Mode      :", mode)
        # print("CAN       :", can_values)
        # print("HARDWARE  :", hardware_values)
        # print("=============================\n")

        key = (
            dut_no,
            cycle_no
        )

        writer = self.writers.get(
            key
        )

        if writer is None:
            return

        row = {
            "Timestamp":
                datetime.now().strftime(
                    "%Y-%m-%d %H:%M:%S"
                ),

            "Time_sec":
                elapsed_seconds,

            "Mode":
                mode
        }

        # ======================================================
        # CAN VALUES
        # ======================================================

        for parameter in self.COMMON_PARAMETERS:

            value = can_values.get(
                parameter,
                ""
            )

            row[
                f"CAN_{parameter}"
            ] = value

        # ======================================================
        # HARDWARE VALUES
        # ======================================================

        for parameter in self.COMMON_PARAMETERS:

            value = hardware_values.get(
                parameter,
                ""
            )

            row[
                f"HW_{parameter}"
            ] = value

        writer.writerow(row)

        # Immediately write to disk
        self.files[key].flush()

    # ==========================================================
    # CLOSE ONE CYCLE
    # ==========================================================

    def close_cycle(
        self,
        dut_no,
        cycle_no
    ):

        key = (
            dut_no,
            cycle_no
        )

        file = self.files.pop(
            key,
            None
        )

        self.writers.pop(
            key,
            None
        )

        if file:

            file.flush()
            file.close()

            print(
                f"CSV closed: DUT{dut_no}, "
                f"cycle{cycle_no}"
            )

    # ==========================================================
    # CLOSE EVERYTHING
    # ==========================================================

    def close_all(self):

        for file in self.files.values():

            try:
                file.flush()
                file.close()

            except Exception:
                pass

        self.files.clear()
        self.writers.clear()