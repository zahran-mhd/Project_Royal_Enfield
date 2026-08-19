import os
import csv
from datetime import datetime
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter


class EnduranceDataLogger:

    # ==========================================================
    # PARAMETERS TO LOG
    # ==========================================================

    COMMON_PARAMETERS = [

        # OBC
        "OBC Input Voltage",
        "OBC Input Current",
        "OBC Output Voltage",
        "OBC Output Current",
        "OBC_Input_Power",
        "OBC_Output_Power",
        "OBC Efficiency",

        # HPDCDC
        "HPDCDC Input Voltage",
        "HPDCDC Input Current",
        "HPDCDC Output Voltage",
        "HPDCDC Output Current",
        "HPDCDC_Input_Power",
        "HPDCDC_Output_Power",
        "HPDCDC_Efficiency",

        # Temperature
        "OBC_TEMP",
        "OBC_FET_TEMP",
        "HPDCDC_TEMP",
    ]

    # ==========================================================
    # INITIALIZATION
    # ==========================================================

    def __init__(self, base_folder="CSV_Logs", report_folder="Report"):

        self.base_folder = base_folder
        self.report_folder = report_folder

        # Current test run
        self.test_folder_name = None
        self.test_name = None

        # CSV
        self.csv_files = {}
        self.csv_writers = {}

        # Excel
        self.excel_files = {}
        self.excel_rows = {}

        # Start time for each DUT/cycle
        self.cycle_start_time = {}

    # ==========================================================
    # SANITIZE FILE/FOLDER NAME
    # ==========================================================

    def sanitize_name(self, name):

        if name is None:
            name = "Unknown_Test"

        invalid = '<>:"/\\|?*'

        for char in invalid:
            name = name.replace(char, "_")

        return name.strip()

    # ==========================================================
    # START TEST
    # ==========================================================

    def start_test(self, test_name):

        self.test_name = self.sanitize_name(test_name)

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        self.test_folder_name = (
            f"{self.test_name}_{timestamp}"
        )

        # ------------------------------------------------------
        # CSV ROOT
        # ------------------------------------------------------

        csv_root = os.path.join(
            self.base_folder,
            self.test_folder_name
        )

        os.makedirs(
            csv_root,
            exist_ok=True
        )

        # ------------------------------------------------------
        # EXCEL ROOT
        # ------------------------------------------------------

        excel_root = os.path.join(
            self.report_folder,
            "Endurance",
            self.test_folder_name
        )

        os.makedirs(
            excel_root,
            exist_ok=True
        )

        print(
            f"Data logging started:\n"
            f"CSV    : {csv_root}\n"
            f"Report : {excel_root}"
        )

    # ==========================================================
    # START CYCLE
    # ==========================================================

    def start_cycle(
        self,
        test_name,
        dut_no,
        cycle_no,
        serial_number="",
        user_name="",
        temperature_type="",
        initial_temperature="",
        source_type=""
    ):

        # If start_test() was not called
        if self.test_folder_name is None:

            self.start_test(test_name)

        # ------------------------------------------------------
        # DUT FOLDER - CSV
        # ------------------------------------------------------

        dut_csv_folder = os.path.join(
            self.base_folder,
            self.test_folder_name,
            f"DUT{dut_no}"
        )

        os.makedirs(
            dut_csv_folder,
            exist_ok=True
        )

        csv_path = os.path.join(
            dut_csv_folder,
            f"Cycle_{cycle_no}.csv"
        )

        # ------------------------------------------------------
        # DUT FOLDER - EXCEL
        # ------------------------------------------------------

        dut_excel_folder = os.path.join(
            self.report_folder,
            "Endurance",
            self.test_folder_name,
            f"DUT{dut_no}"
        )

        os.makedirs(
            dut_excel_folder,
            exist_ok=True
        )

        excel_path = os.path.join(
            dut_excel_folder,
            f"Cycle_{cycle_no}.xlsx"
        )

        # ------------------------------------------------------
        # START TIME
        # ------------------------------------------------------

        start_time = datetime.now()

        self.cycle_start_time[
            (dut_no, cycle_no)
        ] = start_time

        # ======================================================
        # CSV
        # ======================================================

        csv_file = open(
            csv_path,
            "w",
            newline="",
            encoding="utf-8"
        )

        headers = [
            "Timestamp",
            "Time_sec",
            "Mode"
        ]

        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"CAN_{parameter}"
            )

        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"HW_{parameter}"
            )

        writer = csv.DictWriter(
            csv_file,
            fieldnames=headers
        )

        writer.writeheader()

        key = (
            dut_no,
            cycle_no
        )

        self.csv_files[key] = csv_file
        self.csv_writers[key] = writer

        # ======================================================
        # EXCEL
        # ======================================================

        workbook = Workbook()

        worksheet = workbook.active

        worksheet.title = f"Cycle {cycle_no}"

        # ------------------------------------------------------
        # Store Excel information
        # ------------------------------------------------------

        self.excel_files[key] = {
            "workbook": workbook,
            "worksheet": worksheet,
            "path": excel_path,
            "charging_rows": [],
            "discharging_rows": [],
            "charging_start_row": None,
            "discharging_start_row": None,
            "charging_header_row": None,
            "discharging_header_row": None,
            "charging_average_row": None,
            "discharging_average_row": None,
        }

        self._create_excel_header(
            key=key,
            serial_number=serial_number,
            dut_no=dut_no,
            start_time=start_time,
            user_name=user_name,
            temperature_type=temperature_type,
            initial_temperature=initial_temperature,
            source_type=source_type
        )

        workbook.save(excel_path)

        print(
            f"CSV started   : {csv_path}"
        )

        print(
            f"Excel started : {excel_path}"
        )

    # ==========================================================
    # EXCEL HEADER
    # ==========================================================

    def _create_excel_header(
        self,
        key,
        serial_number,
        dut_no,
        start_time,
        user_name,
        temperature_type,
        initial_temperature,
        source_type
    ):

        info = self.excel_files[key]

        ws = info["worksheet"]

        # ------------------------------------------------------
        # TITLE
        # ------------------------------------------------------

        ws["A1"] = "Endurance Test Report"

        ws["A1"].font = Font(
            bold=True,
            size=16
        )

        ws.merge_cells(
            start_row=1,
            start_column=1,
            end_row=1,
            end_column=6
        )

        # ------------------------------------------------------
        # INFORMATION
        # ------------------------------------------------------

        headers = [
            "Serial Number",
            "DUT Slot",
            "Start Time",
            "User Name",
            "Temperature Type",
            "Initial Temperature(°C)",
            "Source Type"
        ]

        values = [
            serial_number,
            f"DUT{dut_no}",
            start_time.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            user_name,
            temperature_type,
            initial_temperature,
            source_type
        ]

        # Header row
        for column, value in enumerate(
            headers,
            start=1
        ):

            cell = ws.cell(
                row=3,
                column=column
            )

            cell.value = value
            cell.font = Font(
                bold=True
            )

        # Values row
        for column, value in enumerate(
            values,
            start=1
        ):

            ws.cell(
                row=4,
                column=column
            ).value = value

        # ------------------------------------------------------
        # Formatting
        # ------------------------------------------------------

        for row in ws.iter_rows(
            min_row=3,
            max_row=4,
            min_col=1,
            max_col=len(headers)
        ):

            for cell in row:

                cell.alignment = Alignment(
                    horizontal="center",
                    vertical="center"
                )

        # ------------------------------------------------------
        # Start Charging section
        # ------------------------------------------------------

        row = 6

        ws.cell(
            row=row,
            column=1
        ).value = "OBC Charging"

        ws.cell(
            row=row,
            column=1
        ).font = Font(
            bold=True,
            size=14
        )

        info["charging_start_row"] = row

        row += 1

        headers = self._get_data_headers()

        info["charging_header_row"] = row

        self._write_data_headers(
            ws,
            row,
            headers
        )

    # ==========================================================
    # DATA HEADERS
    # ==========================================================

    def _get_data_headers(self):

        headers = [
            "Timestamp",
            "Time_sec",
            "Mode"
        ]

        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"CAN_{parameter}"
            )

        for parameter in self.COMMON_PARAMETERS:

            headers.append(
                f"HW_{parameter}"
            )

        return headers

    # ==========================================================
    # WRITE DATA HEADERS
    # ==========================================================

    def _write_data_headers(
        self,
        worksheet,
        row,
        headers
    ):

        for column, header in enumerate(
            headers,
            start=1
        ):

            cell = worksheet.cell(
                row=row,
                column=column
            )

            cell.value = header

            cell.font = Font(
                bold=True
            )

            cell.alignment = Alignment(
                horizontal="center"
            )

    # ==========================================================
    # LOG DATA
    # ==========================================================

    def log_data(
        self,
        dut_no,
        cycle_no,
        mode,
        can_values,
        hardware_values,
        timestamp=None,
        time_sec=None
    ):

        key = (
            dut_no,
            cycle_no
        )

        # ------------------------------------------------------
        # Validate
        # ------------------------------------------------------

        if key not in self.csv_writers:

            print(
                f"Logger not started for "
                f"DUT{dut_no} Cycle {cycle_no}"
            )

            return

        # ------------------------------------------------------
        # Timestamp
        # ------------------------------------------------------

        if timestamp is None:

            timestamp = datetime.now()

        if isinstance(timestamp, datetime):

            timestamp_text = timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            )

        else:

            timestamp_text = str(timestamp)

        # ------------------------------------------------------
        # Time seconds
        # ------------------------------------------------------

        if time_sec is None:

            start = self.cycle_start_time.get(
                key,
                timestamp
            )

            if isinstance(start, datetime) and isinstance(timestamp, datetime):

                time_sec = (
                    timestamp - start
                ).total_seconds()

            else:

                time_sec = 0

        # ======================================================
        # BUILD ROW
        # ======================================================

        row = {
            "Timestamp": timestamp_text,
            "Time_sec": round(
                float(time_sec),
                2
            ),
            "Mode": mode
        }

        # ------------------------------------------------------
        # CAN
        # ------------------------------------------------------

        for parameter in self.COMMON_PARAMETERS:

            value = can_values.get(
                parameter,
                ""
            )

            row[
                f"CAN_{parameter}"
            ] = value

        # ------------------------------------------------------
        # HARDWARE
        # ------------------------------------------------------

        for parameter in self.COMMON_PARAMETERS:

            value = hardware_values.get(
                parameter,
                ""
            )

            row[
                f"HW_{parameter}"
            ] = value

        # ======================================================
        # CSV
        # ======================================================

        writer = self.csv_writers[key]

        writer.writerow(row)

        self.csv_files[key].flush()

        # ======================================================
        # EXCEL
        # ======================================================

        info = self.excel_files[key]

        ws = info["worksheet"]

        # ------------------------------------------------------
        # Determine section
        # ------------------------------------------------------

        mode_lower = str(
            mode
        ).lower()

        if mode_lower in (
            "charge",
            "charging"
        ):

            section = "charging"

        elif mode_lower in (
            "discharge",
            "discharging"
        ):

            section = "discharging"

        else:

            # REST is not stored in either section
            return

        # ------------------------------------------------------
        # Create DCDC section when first needed
        # ------------------------------------------------------

        if (
            section == "discharging"
            and info["discharging_header_row"] is None
        ):

            self._create_discharging_section(
                key
            )

        # ------------------------------------------------------
        # Determine row
        # ------------------------------------------------------

        if section == "charging":

            header_row = info[
                "charging_header_row"
            ]

            data_rows = info[
                "charging_rows"
            ]

        else:

            header_row = info[
                "discharging_header_row"
            ]

            data_rows = info[
                "discharging_rows"
            ]

        row_number = (
            header_row +
            1 +
            len(data_rows)
        )

        # ------------------------------------------------------
        # Write Excel row
        # ------------------------------------------------------

        values = []

        for header in self._get_data_headers():

            values.append(
                row.get(
                    header,
                    ""
                )
            )

        for column, value in enumerate(
            values,
            start=1
        ):

            ws.cell(
                row=row_number,
                column=column
            ).value = value

        data_rows.append(
            row_number
        )

        # ------------------------------------------------------
        # Auto width
        # ------------------------------------------------------

        self._adjust_column_widths(
            ws
        )

        # Save
        info["workbook"].save(
            info["path"]
        )

    # ==========================================================
    # CREATE DISCHARGING SECTION
    # ==========================================================

    def _create_discharging_section(
        self,
        key
    ):

        info = self.excel_files[key]

        ws = info["worksheet"]

        # ------------------------------------------------------
        # Find next available row
        # ------------------------------------------------------

        max_row = ws.max_row

        row = max_row + 3

        # ------------------------------------------------------
        # Heading
        # ------------------------------------------------------

        ws.cell(
            row=row,
            column=1
        ).value = "DCDC Discharging"

        ws.cell(
            row=row,
            column=1
        ).font = Font(
            bold=True,
            size=14
        )

        info["discharging_start_row"] = row

        row += 1

        # ------------------------------------------------------
        # Column headers
        # ------------------------------------------------------

        info["discharging_header_row"] = row

        self._write_data_headers(
            ws,
            row,
            self._get_data_headers()
        )

    # ==========================================================
    # FINISH CYCLE
    # ==========================================================

    def finish_cycle(
        self,
        dut_no,
        cycle_no
    ):

        key = (
            dut_no,
            cycle_no
        )

        # ======================================================
        # CSV
        # ======================================================

        if key in self.csv_files:

            try:

                self.csv_files[key].flush()
                self.csv_files[key].close()

            except Exception as e:

                print(
                    f"CSV close error: {e}"
                )

            del self.csv_files[key]
            del self.csv_writers[key]

            print(
                f"CSV closed: "
                f"DUT{dut_no}, "
                f"Cycle {cycle_no}"
            )

        # ======================================================
        # EXCEL
        # ======================================================

        if key in self.excel_files:

            info = self.excel_files[key]

            ws = info["worksheet"]

            # --------------------------------------------------
            # Charging average
            # --------------------------------------------------

            if info["charging_rows"]:

                self._write_average_row(
                    ws,
                    info["charging_rows"],
                    "charging"
                )

            # --------------------------------------------------
            # Discharging average
            # --------------------------------------------------

            if info["discharging_rows"]:

                self._write_average_row(
                    ws,
                    info["discharging_rows"],
                    "discharging"
                )

            # --------------------------------------------------
            # Formatting
            # --------------------------------------------------

            self._format_excel(
                ws
            )

            # --------------------------------------------------
            # Save
            # --------------------------------------------------

            info["workbook"].save(
                info["path"]
            )

            print(
                f"Excel closed: "
                f"DUT{dut_no}, "
                f"Cycle {cycle_no}"
            )

            del self.excel_files[key]

        # ------------------------------------------------------
        # Remove start time
        # ------------------------------------------------------

        self.cycle_start_time.pop(
            key,
            None
        )

    # ==========================================================
    # WRITE AVERAGE
    # ==========================================================

    def _write_average_row(
        self,
        worksheet,
        data_rows,
        section
    ):

        if not data_rows:
            return

        average_row = (
            max(data_rows) + 1
        )

        worksheet.cell(
            row=average_row,
            column=1
        ).value = "Average"

        worksheet.cell(
            row=average_row,
            column=1
        ).font = Font(
            bold=True
        )

        # ------------------------------------------------------
        # Average numeric columns
        # ------------------------------------------------------

        headers = self._get_data_headers()

        for column, header in enumerate(
            headers,
            start=1
        ):

            # Skip non-numeric
            if header in (
                "Timestamp",
                "Mode"
            ):
                continue

            values = []

            for row in data_rows:

                value = worksheet.cell(
                    row=row,
                    column=column
                ).value

                try:

                    if value is not None and value != "":

                        values.append(
                            float(value)
                        )

                except (
                    ValueError,
                    TypeError
                ):

                    pass

            if values:

                average = (
                    sum(values) /
                    len(values)
                )

                worksheet.cell(
                    row=average_row,
                    column=column
                ).value = round(
                    average,
                    4
                )

        # ------------------------------------------------------
        # Save average row reference
        # ------------------------------------------------------

        if section == "charging":

            # Nothing else required

            pass

        elif section == "discharging":

            pass

    # ==========================================================
    # FORMAT EXCEL
    # ==========================================================

    def _format_excel(
        self,
        worksheet
    ):

        thin_border = Border(
            left=Side(style="thin"),
            right=Side(style="thin"),
            top=Side(style="thin"),
            bottom=Side(style="thin")
        )

        # ------------------------------------------------------
        # Format all used cells
        # ------------------------------------------------------

        for row in worksheet.iter_rows():

            for cell in row:

                cell.alignment = Alignment(
                    vertical="center",
                    horizontal="center"
                )

        # ------------------------------------------------------
        # Borders
        # ------------------------------------------------------

        for row in worksheet.iter_rows():

            for cell in row:

                if cell.value is not None:

                    cell.border = thin_border

        # ------------------------------------------------------
        # Header rows
        # ------------------------------------------------------

        for row in range(
            1,
            worksheet.max_row + 1
        ):

            value = worksheet.cell(
                row=row,
                column=1
            ).value

            if value in (
                "OBC Charging",
                "DCDC Discharging"
            ):

                worksheet.cell(
                    row=row,
                    column=1
                ).font = Font(
                    bold=True,
                    size=14
                )

        # ------------------------------------------------------
        # Freeze panes
        # ------------------------------------------------------

        worksheet.freeze_panes = "A8"

    # ==========================================================
    # COLUMN WIDTH
    # ==========================================================

    def _adjust_column_widths(
        self,
        worksheet
    ):

        for column_cells in worksheet.columns:

            max_length = 0

            column_letter = get_column_letter(
                column_cells[0].column
            )

            for cell in column_cells:

                try:

                    length = len(
                        str(cell.value)
                    )

                    if length > max_length:

                        max_length = length

                except Exception:

                    pass

            worksheet.column_dimensions[
                column_letter
            ].width = min(
                max(max_length + 2, 12),
                30
            )

    # ==========================================================
    # CLOSE ALL
    # ==========================================================

    def close_all(self):

        # Close CSV files

        for key, file in list(
            self.csv_files.items()
        ):

            try:
                file.flush()
                file.close()
            except Exception:
                pass

        self.csv_files.clear()
        self.csv_writers.clear()

        # Save Excel files

        for key, info in list(
            self.excel_files.items()
        ):

            try:

                self._format_excel(
                    info["worksheet"]
                )

                info["workbook"].save(
                    info["path"]
                )

            except Exception as e:

                print(
                    f"Excel close error: {e}"
                )

        self.excel_files.clear()

        print(
            "All data loggers closed."
        )