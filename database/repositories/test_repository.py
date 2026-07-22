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