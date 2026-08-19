class ParameterRepository:

    def __init__(self, db):
        self.db = db

    def get_all_duts(self, conn):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT dut_id, dut_name
            FROM DUT
            ORDER BY dut_id
        """)

        return cursor.fetchall()


    def get_by_name(self, dut_name):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                dut_id,
                dut_name,
                dut_bit_rate
            FROM DUT
            WHERE dut_name = ?
            """,
            (dut_name,)
        )

        return cursor.fetchone()

    def get_dut_settings(self, conn, dut_id):
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT *
                FROM DUT
                WHERE dut_id=?
            """, (dut_id,))
    
            return cursor.fetchone()

    def get_endurance_settings(self, conn, dut_id):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Endurance_Settings
            WHERE dut_id=?
        """, (dut_id,))

        return cursor.fetchone()

    def get_line_common(self, conn, dut_id):
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT *
                FROM Line_Common_Settings
                WHERE dut_id=?
            """, (dut_id,))
    
            return cursor.fetchone()


    def get_obc_line_settings(self, conn, dut_id):

        cursor = conn.cursor()

        # ==========================================
        # GET AC SETTINGS
        # ==========================================

        cursor.execute(
            """
            SELECT
                input_setting_id,
                dc_load_current,
                input_voltage,
                input_frequency
            FROM OBC_HV_DC_Input_Settings
            WHERE dut_id = ?
            ORDER BY input_setting_id
            """,
            (dut_id,)
        )

        input_rows = cursor.fetchall()

        # ==========================================
        # GET HV SETTINGS
        # ==========================================

        cursor.execute(
            """
            SELECT
                step_no,
                hv_voltage,
                hv_current
            FROM OBC_HV_DC_Output_Settings
            WHERE dut_id = ?
            ORDER BY step_no
            """,
            (dut_id,)
        )

        output_rows = cursor.fetchall()

        # ==========================================
        # BUILD OLD UI FORMAT
        # ==========================================

        outputs = []

        for row in output_rows:

            outputs.append({
                "step_no": row["step_no"],
                "hv_voltage": row["hv_voltage"],
                "hv_current": row["hv_current"]
            })

        result = []

        for row in input_rows:

            result.append({
                "dc_load_current":
                    row["dc_load_current"],

                "input_voltage":
                    row["input_voltage"],

                "input_frequency":
                    row["input_frequency"],

                # Same HV steps for every AC condition
                "outputs": [
                    output.copy()
                    for output in outputs
                ]
            })

        return result



    # def get_obc_line_settings(self, conn, dut_id):

    #     cursor = conn.cursor()

    #     # ==========================================
    #     # COMMON DWELL
    #     # ==========================================

    #     cursor.execute(
    #         """
    #         SELECT
    #             dwell_time
    #         FROM Line_Common_Settings
    #         WHERE dut_id = ?
    #         """,
    #         (dut_id,)
    #     )

    #     common_row = cursor.fetchone()

    #     dwell_time = (
    #         common_row["dwell_time"]
    #         if common_row
    #         else None
    #     )

    #     # ==========================================
    #     # AC INPUT SETTINGS
    #     # ==========================================

    #     cursor.execute(
    #         """
    #         SELECT
    #             input_setting_id,
    #             step_no,
    #             dc_load_current,
    #             input_voltage,
    #             input_frequency
    #         FROM OBC_HV_DC_Input_Settings
    #         WHERE dut_id = ?
    #         ORDER BY step_no
    #         """,
    #         (dut_id,)
    #     )

    #     input_rows = cursor.fetchall()

    #     # ==========================================
    #     # HV OUTPUT SETTINGS
    #     # ==========================================

    #     cursor.execute(
    #         """
    #         SELECT
    #             step_no,
    #             hv_voltage,
    #             hv_current
    #         FROM OBC_HV_DC_Output_Settings
    #         WHERE dut_id = ?
    #         ORDER BY step_no
    #         """,
    #         (dut_id,)
    #     )

    #     output_rows = cursor.fetchall()

    #     # ==========================================
    #     # BUILD RESULT
    #     # ==========================================

    #     result = {

    #         "dwell_time": dwell_time,

    #         "inputs": [],

    #         "outputs": []
    #     }

    #     # ------------------------------------------
    #     # AC INPUTS
    #     # ------------------------------------------

    #     for row in input_rows:

    #         result["inputs"].append({

    #             "input_setting_id":
    #                 row["input_setting_id"],

    #             "step_no":
    #                 row["step_no"],

    #             "dc_load_current":
    #                 row["dc_load_current"],

    #             "input_voltage":
    #                 row["input_voltage"],

    #             "input_frequency":
    #                 row["input_frequency"]
    #         })

    #     # ------------------------------------------
    #     # HV OUTPUTS
    #     # ------------------------------------------

    #     for row in output_rows:

    #         result["outputs"].append({

    #             "step_no":
    #                 row["step_no"],

    #             "hv_voltage":
    #                 row["hv_voltage"],

    #             "hv_current":
    #                 row["hv_current"]
    #         })

    #     return result

    # def get_obc_line_settings(self, conn, dut_id):

    #     cursor = conn.cursor()

    #     cursor.execute("""
    #         SELECT
    #             i.input_setting_id,
    #             i.dc_load_current,
    #             i.input_voltage,
    #             i.input_frequency,

    #             o.step_no,
    #             o.hv_voltage,
    #             o.hv_current

    #         FROM OBC_HV_DC_Input_Settings i

    #         LEFT JOIN OBC_HV_DC_Output_Settings o
    #             ON i.input_setting_id = o.input_setting_id

    #         WHERE i.dut_id = ?

    #         ORDER BY
    #             i.input_setting_id,
    #             o.step_no
    #     """, (dut_id,))

    #     rows = cursor.fetchall()

    #     result = []
    #     inputs = {}

    #     for row in rows:

    #         input_id = row["input_setting_id"]

    #         if input_id not in inputs:

    #             inputs[input_id] = {
    #                 "dc_load_current": row["dc_load_current"],
    #                 "input_voltage": row["input_voltage"],
    #                 "input_frequency": row["input_frequency"],
    #                 "outputs": []
    #             }

    #             result.append(inputs[input_id])

    #         inputs[input_id]["outputs"].append({

    #             "step_no": row["step_no"],
    #             "hv_voltage": row["hv_voltage"],
    #             "hv_current": row["hv_current"]

    #         })

    #     return result

    # def get_hpdc_line_current(self, conn, dut_id):
    #     cursor = conn.cursor()

    #     cursor.execute("""
    #         SELECT *
    #         FROM HPDC_HV_DC_Load_Settings
    #         WHERE dut_id=?
    #     """, (dut_id,))

    #     return cursor.fetchone()

    # def get_hpdc_line_setting(self, conn, dut_id):
    #     cursor = conn.cursor()

    #     cursor.execute("""
    #         SELECT *
    #         FROM HPDC_HV_DC_Load_HV
    #         WHERE dut_id=?
    #     """, (dut_id,))

    #     return cursor.fetchone()

    def get_hpdc_line_setting(self, conn, dut_id):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                s.dc_load_current,
                h.step_no,
                h.hv_voltage
            FROM HPDC_HV_DC_Load_Settings s
            JOIN HPDC_HV_DC_Load_HV h
                ON s.dut_id = h.dut_id
            WHERE s.dut_id = ?
            ORDER BY h.step_no
        """, (dut_id,))

        rows = cursor.fetchall()

        if not rows:
            return None

        print(rows[0]["dc_load_current"])
        print(rows[1])
        result = {
            "dc_load_current": rows[0]["dc_load_current"],
            "hv_steps": []
        }

        for row in rows:
            result["hv_steps"].append({
                "step_no": row["step_no"],
                "hv_voltage": row["hv_voltage"]
            })

        print(result)

        return result

    def get_load_common(self, conn, dut_id):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM HV_DC_Common_Settings
            WHERE dut_id=?
        """, (dut_id,))

        return cursor.fetchone()

    def get_obc_current_settings(self, conn, dut_id):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                hv_voltage,
                step_no,
                load_percent,
                current_value
            FROM OBC_HV_DC_Current_Settings
            WHERE dut_id = ?
            ORDER BY step_no, load_percent
        """, (dut_id,))

        rows = cursor.fetchall()

        if not rows:
            return []

        load_map = {
            0: "No Load",
            25: "25",
            50: "50",
            75: "75",
            100: "100"
        }

        result = []
        steps = {}

        for row in rows:

            step_no = row["step_no"]

            if step_no not in steps:

                steps[step_no] = {
                    "step_no": step_no,
                    "hv_voltage": row["hv_voltage"],
                    "loads": {}
                }

                result.append(steps[step_no])

            steps[step_no]["loads"][
                load_map[row["load_percent"]]
            ] = row["current_value"]

        return result

    def get_hpdc_current_settings(self, conn, dut_id):
    
            cursor = conn.cursor()
    
            cursor.execute("""
                SELECT
                    hv_voltage,
                    step_no,
                    load_percent,
                    current_value
                FROM HPDC_HV_DC_Current_Settings
                WHERE dut_id = ?
                ORDER BY step_no, load_percent
            """, (dut_id,))
    
            rows = cursor.fetchall()
    
            if not rows:
                return []
    
            load_map = {
                0: "No Load",
                25: "25",
                50: "50",
                75: "75",
                100: "100"
            }
    
            result = []
            steps = {}
    
            for row in rows:
    
                step_no = row["step_no"]
    
                if step_no not in steps:
    
                    steps[step_no] = {
                        "step_no": step_no,
                        "hv_voltage": row["hv_voltage"],
                        "loads": {}
                    }
    
                    result.append(steps[step_no])
    
                steps[step_no]["loads"][
                    load_map[row["load_percent"]]
                ] = row["current_value"]
    
            return result
    

    # def get_obc_input_settings(self, conn, dut_id):

    #     cursor = conn.cursor()

    #     cursor.execute("""
    #         SELECT
    #             input_setting_id,
    #             dc_load_current,
    #             input_voltage,
    #             input_frequency
    #         FROM OBC_HV_DC_Input_Settings
    #         WHERE dut_id = ?
    #         ORDER BY input_setting_id
    #     """, (dut_id,))

    #     return cursor.fetchall()

    # def get_obc_output_settings(self, conn, dut_id):
    
    #         cursor = conn.cursor()
    
    #         cursor.execute("""
    #             SELECT
    #                 input_setting_id,
    #                 dc_load_current,
    #                 hv_voltage,
    #                 hv_current
    #             FROM OBC_HV_DC_Output_Settings
    #             WHERE dut_id = ?
    #             ORDER BY input_setting_id
    #         """, (dut_id,))
    
    #         return cursor.fetchall()

    def add_dut(self, conn, values):
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO DUT (dut_name, dut_bit_rate)
            VALUES (?, ?)
        """, values)

    def edit_dut(self, conn, values):
            dut_id=values[0]
            dut_name=values[1]
            dut_bit_rate=values[2]

            print(dut_id,dut_name,dut_bit_rate)
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE DUT
                SET
                    dut_name = ?,
                    dut_bit_rate = ?
                WHERE dut_id = ?
            """, (
                dut_name,
                dut_bit_rate,
                dut_id
            ))

    def delete_duts(self, conn, dut_ids):

        cursor = conn.cursor()

        cursor.executemany(
            "DELETE FROM DUT WHERE dut_id=?",
            [(dut_id,) for dut_id in dut_ids]
        )

        conn.commit()
    

        # conn.commit()

    def save_endurance_settings(self, conn, data):

        cursor = conn.cursor()

        common = data["endurance"]
        print(common)
        print(data["dut_id"])
        print(type(data["dut_id"]))
        cursor.execute("""
        INSERT INTO Endurance_Settings (
                dut_id,
                charge_time,
                discharge_time,
                rest_time1,
                rest_time2,
                ac_input_voltage,
                ac_input_frequency,
                dc_output_voltage,
                dc_output_current,
                char_dc_load_current,
                dis_dc_load_current
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)

        ON CONFLICT(dut_id)
        DO UPDATE SET
                charge_time=excluded.charge_time,
                discharge_time=excluded.discharge_time,
                rest_time1=excluded.rest_time1,
                rest_time2=excluded.rest_time2,
                ac_input_voltage=excluded.ac_input_voltage,
                ac_input_frequency=excluded.ac_input_frequency,
                dc_output_voltage=excluded.dc_output_voltage,
                dc_output_current=excluded.dc_output_current,
                char_dc_load_current=excluded.char_dc_load_current,
                dis_dc_load_current=excluded.dis_dc_load_current
        """,

        (
            data["dut_id"],
            common["charge_time"],
            common["discharge_time"],
            common["rest_time1"],
            common["rest_time2"],
            common["ac_input_voltage"],
            common["ac_input_frequency"],
            common["dc_output_voltage"],
            common["dc_output_current"],
            common["char_dc_load_current"],
            common["dis_dc_load_current"]
        ))


    def save_line_common_settings(self, conn, data):

        cursor = conn.cursor()

        common = data["line_common"]

        cursor.execute("""
        INSERT INTO Line_Common_Settings
        VALUES (?,?)

        ON CONFLICT(dut_id)
        DO UPDATE SET
        dwell_time=excluded.dwell_time
        """,

        (
            data["dut_id"],
            common["line_dwell_time"]
        ))


    def save_obc_input(self, conn, data):

        cursor = conn.cursor()

        dut_id = data["dut_id"]

        # ==========================================
        # DELETE OLD HV SETTINGS
        # ==========================================

        cursor.execute(
            """
            DELETE FROM OBC_HV_DC_Output_Settings
            WHERE dut_id = ?
            """,
            (dut_id,)
        )

        # ==========================================
        # DELETE OLD AC SETTINGS
        # ==========================================

        cursor.execute(
            """
            DELETE FROM OBC_HV_DC_Input_Settings
            WHERE dut_id = ?
            """,
            (dut_id,)
        )

        # ==========================================
        # SAVE AC SETTINGS
        # ==========================================

        for index, item in enumerate(
            data["obc_line_inputs"],
            start=1
        ):

            cursor.execute(
                """
                INSERT INTO OBC_HV_DC_Input_Settings
                (
                    dut_id,
                    step_no,
                    dc_load_current,
                    input_voltage,
                    input_frequency
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    dut_id,
                    index,
                    item["dc_load_current"],
                    item["input_voltage"],
                    item["input_frequency"]
                )
            )

        # ==========================================
        # SAVE HV SETTINGS ONLY ONCE
        # ==========================================

        if data["obc_line_inputs"]:

            first_input = data["obc_line_inputs"][0]

            for output in first_input["outputs"]:

                cursor.execute(
                    """
                    INSERT INTO OBC_HV_DC_Output_Settings
                    (
                        dut_id,
                        step_no,
                        hv_voltage,
                        hv_current
                    )
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        dut_id,
                        output["step_no"],
                        output["hv_voltage"],
                        output["hv_current"]
                    )
                )

    # def save_obc_input(self, conn, data):

    #     cursor = conn.cursor()

    #     # cursor.execute(
    #     #     "DELETE FROM OBC_HV_DC_Input_Settings WHERE dut_id=?",
    #     #     (data["dut_id"],)
    #     # )

    #     cursor.execute("""
    #         DELETE FROM OBC_HV_DC_Output_Settings
    #         WHERE input_setting_id IN
    #         (
    #             SELECT input_setting_id
    #             FROM OBC_HV_DC_Input_Settings
    #             WHERE dut_id=?
    #         )
    #         """, (data["dut_id"],))

    #     cursor.execute("""
    #         DELETE FROM OBC_HV_DC_Input_Settings
    #         WHERE dut_id=?
    #         """, (data["dut_id"],))

    #     for item in data["obc_line_inputs"]:

    #         cursor.execute("""

    #         INSERT INTO OBC_HV_DC_Input_Settings
    #         (
    #             dut_id,
    #             dc_load_current,
    #             input_voltage,
    #             input_frequency
    #         )

    #         VALUES(?,?,?,?)

    #         """,

    #         (

    #             data["dut_id"],
    #             item["dc_load_current"],
    #             item["input_voltage"],
    #             item["input_frequency"]

    #         ))

    #         input_setting_id = cursor.lastrowid

    #         for output in item["outputs"]:

    #             cursor.execute("""

    #             INSERT INTO OBC_HV_DC_Output_Settings

    #             VALUES(?,?,?,?)

    #             """,

    #             (

    #                 input_setting_id,
    #                 output["step_no"],
    #                 output["hv_voltage"],
    #                 output["hv_current"]

    #             ))


    def save_hpdc_input(self, conn, data):

        cursor = conn.cursor()

        hpdc = data["hpdc_line"]

        # Delete child rows first
        cursor.execute("""
            DELETE FROM HPDC_HV_DC_Load_HV
            WHERE dut_id=?
        """, (data["dut_id"],))

        # Delete parent row
        cursor.execute("""
            DELETE FROM HPDC_HV_DC_Load_Settings
            WHERE dut_id=?
        """, (data["dut_id"],))

        # Insert parent
        cursor.execute("""
            INSERT INTO HPDC_HV_DC_Load_Settings
            (
                dut_id,
                dc_load_current
            )
            VALUES (?, ?)
        """, (
            data["dut_id"],
            hpdc["dc_load_current"]
        ))

        # Insert child rows
        for step in hpdc["hv_steps"]:

            cursor.execute("""
                INSERT INTO HPDC_HV_DC_Load_HV
                (
                    dut_id,
                    step_no,
                    hv_voltage
                )
                VALUES (?, ?, ?)
            """, (
                data["dut_id"],
                step["step_no"],
                step["hv_voltage"]
            ))

    def save_load_common_settings(self, conn, data):
    
            cursor = conn.cursor()
    
            common = data["load_common"]
    
            cursor.execute("""
            INSERT INTO HV_DC_Common_Settings
            VALUES (?,?,?,?)
    
            ON CONFLICT(dut_id)
            DO UPDATE SET
            dwell_time=excluded.dwell_time,
            input_frequency=excluded.input_frequency,
            input_voltage=excluded.input_voltage
            """,
    
            (
                data["dut_id"],
                common["load_dwell_time"],
                common["load_input_frequency"],
                common["load_input_voltage"]
            ))

    def save_obc_current_settings(self, conn, data):

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM OBC_HV_DC_Current_Settings
            WHERE dut_id=?
        """, (data["dut_id"],))

        load_map = {
            "No Load": 0,
            "25": 25,
            "50": 50,
            "75": 75,
            "100": 100
        }

        for step in data["obc_load_regulation"]:
            print(step)
            for load_name, current in step["loads"].items():
                print(data["dut_id"],
                                    step["hv_voltage"],
                                    step["step_no"],
                                    load_map[load_name],
                                    current)

                cursor.execute("""
                    INSERT INTO OBC_HV_DC_Current_Settings
                    (
                        dut_id,
                        hv_voltage,
                        step_no,
                        load_percent,
                        current_value
                    )
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    data["dut_id"],
                    step["hv_voltage"],
                    step["step_no"],
                    load_map[load_name],
                    current
                ))

    def save_hpdc_current_settings(self, conn, data):
    
            cursor = conn.cursor()
    
            cursor.execute("""
                DELETE FROM HPDC_HV_DC_Current_Settings
                WHERE dut_id=?
            """, (data["dut_id"],))
    
            load_map = {
                "No Load": 0,
                "25": 25,
                "50": 50,
                "75": 75,
                "100": 100
            }
    
            for step in data["hpdc_load_regulation"]:
                print(step)
    
                for load_name, current in step["loads"].items():
                    print(data["dut_id"],
                                        step["hv_voltage"],
                                        step["step_no"],
                                        load_map[load_name],
                                        current)
    
                    cursor.execute("""
                        INSERT INTO HPDC_HV_DC_Current_Settings
                        (
                            dut_id,
                            hv_voltage,
                            step_no,
                            load_percent,
                            current_value
                        )
                        VALUES (?, ?, ?, ?, ?)
                    """, (
                        data["dut_id"],
                        step["hv_voltage"],
                        step["step_no"],
                        load_map[load_name],
                        current
                    ))

    def save_dbc_file(self, conn, dut_id, file_name, file_path):

        cursor = conn.cursor()

        cursor.execute(
            "DELETE FROM DUT_File WHERE dut_id=?",
            (dut_id,)
        )

        cursor.execute("""
            INSERT INTO DUT_File
            (
                dut_id,
                file_name,
                file_path
            )
            VALUES (?, ?, ?)
        """, (
            dut_id,
            file_name,
            file_path
        ))

        conn.commit()

    def remove_dbc_file(self, conn, dut_id):

        cursor = conn.cursor()

        cursor.execute("""
            DELETE FROM DUT_File
            WHERE dut_id=?
        """, (dut_id,))

        conn.commit()

    def get_dbc_file(self, conn, dut_id):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                file_name,
                file_path
            FROM DUT_File
            WHERE dut_id=?
        """, (dut_id,))

        return cursor.fetchone()


    def get_rp_initial_settings(self, dut_id):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT
                dc_output_voltage,
                dc_output_current
            FROM Endurance_Settings
            WHERE dut_id = ?
        """, (dut_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "dc_output_voltage": row["dc_output_voltage"],
            "dc_output_current": row["dc_output_current"]
            # "char_dc_load_current": row["char_dc_load_current"]
        }


    def get_el4935a_initial_settings(self, dut_id):
    
            cursor = self.db.conn.cursor()
    
            cursor.execute("""
                SELECT
                    dis_dc_load_current
                FROM Endurance_Settings
                WHERE dut_id = ?
            """, (dut_id,))
    
            row = cursor.fetchone()
    
            if row is None:
                return None
    
            return {
                "dis_dc_load_current": row["dis_dc_load_current"]
            }


    def get_el34143a_initial_settings(self, dut_id):
    
            cursor = self.db.conn.cursor()
    
            cursor.execute("""
                SELECT
                    char_dc_load_current
                FROM Endurance_Settings
                WHERE dut_id = ?
            """, (dut_id,))
    
            row = cursor.fetchone()
    
            if row is None:
                return None
    
            return {
                "char_dc_load_current": row["char_dc_load_current"]
            }

    def get_endurance_settings(self, conn, dut_name):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT E.*
            FROM Endurance_Settings E
            INNER JOIN DUT D
                ON E.dut_id = D.dut_id
            WHERE D.dut_name = ?
        """, (dut_name,))

        row = cursor.fetchone()
        print(row)
        return dict(row) if row else None

    def get_endurance_settingsbyid(self,conn, dut_id):

        cursor = conn.cursor()

        cursor.execute("""
            SELECT *
            FROM Endurance_Settings
            WHERE dut_id = ?
        """, (dut_id,))

        row = cursor.fetchone()

        return dict(row) if row else None

    def get_line_common_settings(self, dut_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                dut_id,
                dwell_time
            FROM Line_Common_Settings
            WHERE dut_id = ?
            """,
            (dut_id,)
        )

        return cursor.fetchone()

    # def get_obc_hv_dc_input_settings(self, dut_id):

    #     cursor = self.db.conn.cursor()

    #     cursor.execute(
    #         """
    #         SELECT
    #             input_setting_id,
    #             dut_id,
    #             dc_load_current,
    #             input_voltage,
    #             input_frequency
    #         FROM OBC_HV_DC_Input_Settings
    #         WHERE dut_id = ?
    #         ORDER BY input_setting_id
    #         LIMIT 1
    #         """,
    #         (dut_id,)
    #     )

    #     return cursor.fetchone()

    def get_obc_hv_dc_input_settings(self, dut_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                input_setting_id,
                dut_id,
                step_no,
                dc_load_current,
                input_voltage,
                input_frequency
            FROM OBC_HV_DC_Input_Settings
            WHERE dut_id = ?
            ORDER BY step_no
            """,
            (dut_id,)
        )

        return cursor.fetchall()

    # def get_obc_hv_dc_output_settings(
    #     self,
    #     input_setting_id
    # ):

    #     cursor = self.db.conn.cursor()

    #     cursor.execute(
    #         """
    #         SELECT
    #             input_setting_id,
    #             step_no,
    #             hv_voltage,
    #             hv_current
    #         FROM OBC_HV_DC_Output_Settings
    #         WHERE input_setting_id = ?
    #         ORDER BY step_no
    #         """,
    #         (input_setting_id,)
    #     )

    #     return cursor.fetchall()
    

    def get_obc_hv_dc_output_settings(self, dut_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                dut_id,
                step_no,
                hv_voltage,
                hv_current
            FROM OBC_HV_DC_Output_Settings
            WHERE dut_id = ?
            ORDER BY step_no
            """,
            (dut_id,)
        )

        return cursor.fetchall()
    