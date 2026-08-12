import sqlite3
from pathlib import Path
from database.repositories.user_repository import UserRepository


class DatabaseManager:

    def __init__(self, db_path="data/application.db"):

        Path("data").mkdir(exist_ok=True)

        self.conn = sqlite3.connect(
            db_path,
            check_same_thread=False
        )

        self.conn.row_factory = sqlite3.Row

        self.create_tables()
        self.create_default_users()
        self.create_default_channels()
        # self.create_default_alarms()

    # --------------------------------------------------
    # CREATE TABLES
    # --------------------------------------------------

    def create_tables(self):

        cursor = self.conn.cursor()

        # ==========================================
        # USERS
        # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Users
        (
            Id INTEGER PRIMARY KEY AUTOINCREMENT,

            Username TEXT UNIQUE,

            Password TEXT,

            Role TEXT
        )
        """)


        # ==========================================
        # CHANNEL
        # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Channel
        (
            ChannelID INTEGER PRIMARY KEY,

              ChannelName TEXT UNIQUE

        )
        """)

        # ==========================================
        # INSTRUMENT CONFIGURATION
        # ==========================================
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Instruments
        (
            InstrumentID INTEGER PRIMARY KEY AUTOINCREMENT,
        
            InstrumentName TEXT NOT NULL,

            Address TEXT,

            InstrumentSNo TEXT,

            CalibrationDueDate TEXT,

            Status INTEGER,

            IsLocked INTEGER DEFAULT 0
        )
        """)

        # ==========================================
        # CHANNEL INSTRUMENT
        # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS ChannelInstrument
        (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,

            ChannelID INTEGER,

            InstrumentID INTEGER,

            IsShared INTEGER DEFAULT 0,

            FOREIGN KEY (ChannelID)
                REFERENCES Channel(ChannelID),

            FOREIGN KEY (InstrumentID)
                REFERENCES Instruments(InstrumentID)
        )
        """)

        # ==========================================
        # PARAMETER SETTINGS - DUT
        # ==========================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DUT (
            dut_id INTEGER PRIMARY KEY AUTOINCREMENT,
            dut_name TEXT NOT NULL UNIQUE,
            dut_bit_rate INTEGER NOT NULL
        )
        """)

        # ==========================================
        # PARAMETER SETTINGS - DUT DBC FILE
        # ==========================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS DUT_File (
        file_id INTEGER PRIMARY KEY AUTOINCREMENT,
        dut_id INTEGER NOT NULL,
        file_name TEXT,
        file_path TEXT NOT NULL,
        upload_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )   
        """)

        # ==========================================
        # PARAMETER SETTINGS - DUT ENDURANCE
        # ==========================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Endurance_Settings (
            dut_id INTEGER PRIMARY KEY,
            charge_time REAL,
            discharge_time REAL,
            rest_time1 REAL,
            rest_time2 REAL,
            ac_input_voltage REAL,
            ac_input_frequency REAL,
            dc_output_voltage REAL,
            dc_output_current REAL,
            char_dc_load_current REAL,
            dis_dc_load_current REAL,

            FOREIGN KEY (dut_id)
                REFERENCES DUT(dut_id)
        )
        """)

        # ==========================================
        # PARAMETER SETTINGS - LINE REGULATION
        # ==========================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Line_Common_Settings (
            dut_id INTEGER PRIMARY KEY,
            dwell_time INTEGER NOT NULL,
            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OBC_HV_DC_Input_Settings (
            input_setting_id INTEGER PRIMARY KEY AUTOINCREMENT,

            dut_id INTEGER NOT NULL,
            dc_load_current REAL NOT NULL,

            input_voltage REAL NOT NULL,
            input_frequency REAL NOT NULL,

            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OBC_HV_DC_Output_Settings (
            input_setting_id INTEGER NOT NULL,

            step_no INTEGER NOT NULL,
            hv_voltage REAL NOT NULL,
            hv_current REAL NOT NULL,

            PRIMARY KEY (input_setting_id, step_no),

            FOREIGN KEY (input_setting_id)
                REFERENCES OBC_HV_DC_Input_Settings(input_setting_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HPDC_HV_DC_Load_Settings (
            dut_id INTEGER NOT NULL,
            dc_load_current REAL NOT NULL,

            PRIMARY KEY (dut_id),

            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HPDC_HV_DC_Load_HV (
            dut_id INTEGER NOT NULL,
            step_no INTEGER NOT NULL,
            hv_voltage REAL NOT NULL,

            PRIMARY KEY (dut_id, step_no),

            FOREIGN KEY (dut_id) REFERENCES HPDC_HV_DC_Load_Settings(dut_id)
        )
        """)


        # ==========================================
        # PARAMETER SETTINGS - LOAD REGULATION
        # ==========================================
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HV_DC_Common_Settings (
            dut_id INTEGER PRIMARY KEY,

            dwell_time INTEGER NOT NULL,
            input_frequency REAL NOT NULL,
            input_voltage REAL NOT NULL,

            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS OBC_HV_DC_Current_Settings (
            dut_id INTEGER NOT NULL,
            hv_voltage REAL NOT NULL,
            step_no INTEGER NOT NULL,
            current_value REAL NOT NULL,
            PRIMARY KEY (dut_id,hv_voltage, step_no),
            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS HPDC_HV_DC_Current_Settings (
            dut_id INTEGER NOT NULL,
            hv_voltage REAL NOT NULL,
            step_no INTEGER NOT NULL,
            current_value REAL NOT NULL,
            PRIMARY KEY (dut_id,hv_voltage, step_no),
            
            FOREIGN KEY (dut_id) REFERENCES DUT(dut_id)
        )
        """)


        # # ==========================================
        # # TEST SETTINGS
        # # ==========================================

        cursor.execute("""
        CREATE TABLE IF NOT EXISTS Channel_Test_Settings (
            channel_id INTEGER PRIMARY KEY,

            dut_id INTEGER NOT NULL,

            use_dut_a INTEGER DEFAULT 0,
            use_dut_b INTEGER DEFAULT 0,

            test_type TEXT NOT NULL,

            test_name TEXT,

            dut_a_serial_no TEXT,
            dut_b_serial_no TEXT,

            no_of_cycles INTEGER,
            interval_seconds INTEGER,

            FOREIGN KEY (channel_id)
                REFERENCES Channels(channel_id),

            FOREIGN KEY (dut_id)
                REFERENCES DUT(dut_id)
        )
        """)

        # # ==========================================
        # # PARAMETER SETTINGS
        # # ==========================================

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS ThresholdSettings
        # (
        #     ParameterName TEXT PRIMARY KEY,

        #     MinValue REAL,

        #     MaxValue REAL,

        #     Unit TEXT
        # )
        # """)

        # # ==========================================
        # # TEST RESULTS
        # # ==========================================

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS TestResults
        # (
        #     Id INTEGER PRIMARY KEY AUTOINCREMENT,

        #     Timestamp TEXT,

        #     SerialNumber TEXT,

        #     Operator TEXT,

        #     TestName TEXT,

        #     MeasuredValue REAL,

        #     Unit TEXT,

        #     Verdict TEXT
        # )
        # """)

        # # ==========================================
        # # ALARM HISTORY
        # # ==========================================

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS AlarmHistory
        # (
        #     Id INTEGER PRIMARY KEY AUTOINCREMENT,

        #     Timestamp TEXT,

        #     AlarmName TEXT,

        #     AlarmValue REAL,

        #     AlarmLimit REAL
        # )
        # """)
        # ==========================================
        # ALARM SETTINGS
        # ==========================================

        cursor.execute("""

        CREATE TABLE IF NOT EXISTS AlarmSettings
        (
            AlarmID INTEGER PRIMARY KEY AUTOINCREMENT,

            AlarmName TEXT UNIQUE NOT NULL,

            IsEnabled INTEGER NOT NULL DEFAULT 1,

            MinValue REAL,

            MaxValue REAL,

            AlarmType TEXT NOT NULL
                CHECK (AlarmType IN ('Critical', 'Warning'))
        )
        """)

        # # ==========================================
        # # AUDIT LOG
        # # ==========================================

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS AuditLog
        # (
        #     Id INTEGER PRIMARY KEY AUTOINCREMENT,

        #     Timestamp TEXT,

        #     Username TEXT,

        #     Action TEXT
        # )
        # """)

        self.conn.commit()

    # --------------------------------------------------
    # COMMIT
    # --------------------------------------------------

    def commit(self):

        self.conn.commit()

    # --------------------------------------------------
    # CLOSE
    # --------------------------------------------------

    def close(self):

        self.conn.close()

    def create_default_users(self):

        cursor = self.conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO Users
            (
                Username,
                Password,
                Role
            )
            VALUES (?, ?, ?)
            """,
            [
                ("root", "root@123", "root"),
                ("admin", "admin", "admin"),
                ("operator", "operator", "operator")
            ]
        )

        self.conn.commit()
    
    def create_default_channels(self):

        cursor = self.conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO Channel
            (
                  ChannelID,
        ChannelName
            )
            VALUES (?, ?)
            """,
            [
                (1, "CHANNEL1"),
                ( 2, "CHANNEL2"),
              
                      
                
            ]
        )

        self.conn.commit()

    def create_default_alarms(self):

        cursor = self.conn.cursor()

        cursor.executemany(
            """
            INSERT OR IGNORE INTO AlarmSettings
        (AlarmName)
        VALUES(?)
            """,
            [
        ('Input Under Voltage'),

        ('Output Under Voltage'),

        ('Input Over Voltage'),

        ('Output Over Voltage'),

        ('OBC Over Current Protection'),

        ('OBC Short Current Protection'),

        ('HP DCDC Over Current Protection'),

        ('HP DCDC Short Current Protection')
            ]
        )
        self.conn.commit()