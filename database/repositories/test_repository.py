class TestRepository:

    def __init__(self, db):

        self.db = db
    
    def save_settings(self,channel_id,values):
        cursor = self.db.conn.cursor()
        cursor.execute("""
        INSERT INTO Channel_Test_Settings
        (
            channel_id,
            dut_id,
            use_dut_a,
            use_dut_b,
            test_type,
            test_name,
            dut_a_serial_no,
            dut_b_serial_no,
            no_of_cycles,
            interval_seconds
        )
        VALUES
        (
            :channel_id,
            :dut_id,
            :use_dut_a,
            :use_dut_b,
            :test_type,
            :test_name,
            :dut_a_serial_no,
            :dut_b_serial_no,
            :no_of_cycles,
            :interval_seconds
        )

        ON CONFLICT(channel_id)
        DO UPDATE SET
            dut_id = excluded.dut_id,
            use_dut_a = excluded.use_dut_a,
            use_dut_b = excluded.use_dut_b,
            test_type = excluded.test_type,
            test_name = excluded.test_name,
            dut_a_serial_no = excluded.dut_a_serial_no,
            dut_b_serial_no = excluded.dut_b_serial_no,
            no_of_cycles = excluded.no_of_cycles,
            interval_seconds = excluded.interval_seconds
        """, values)
        print(values)



    def get_dbc_file(self, dut_id):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT file_path
            FROM DUT_File
            WHERE dut_id = ?
            ORDER BY upload_date DESC
            LIMIT 1
        """, (dut_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return row["file_path"]

    def get_interval_seconds(self, conn, channel_id):
        cursor = conn.cursor()

        cursor.execute("""
            SELECT interval_seconds
            FROM Channel_Test_Settings
            WHERE channel_id = ?
        """, (channel_id,))

        row = cursor.fetchone()

        if row:
            return row[0]      # or row["interval_seconds"] if row_factory is sqlite3.Row

        return None

    def save_channel_setting(self, conn, setting):

        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO Channel_Test_Settings
            (
                channel_id,
                dut_id,
                use_dut_a,
                use_dut_b,
                test_type,
                test_name,
                dut_a_serial_no,
                dut_b_serial_no,
                no_of_cycles,
                interval_seconds
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            setting["channel_id"],
            setting["dut_id"],
            setting["use_dut_a"],
            setting["use_dut_b"],
            setting["test_type"],
            setting["test_name"],
            setting["dut_a_serial_no"],
            setting["dut_b_serial_no"],
            setting["no_of_cycles"],
            setting["interval_seconds"]
        ))

        conn.commit()

    def get_channel_settings(self, channel_id):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT
                channel_id,
                dut_id,
                use_dut_a,
                use_dut_b,
                test_type,
                test_name,
                dut_a_serial_no,
                dut_b_serial_no,
                no_of_cycles,
                interval_seconds
            FROM Channel_Test_Settings
            WHERE channel_id = ?
        """, (channel_id,))

        row = cursor.fetchone()

        if row is None:
            return None

        return dict(row)