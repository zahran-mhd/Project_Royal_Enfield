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
        
            Sno INTEGER UNIQUE NOT NULL,

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

        # # ==========================================
        # # TEST SETTINGS
        # # ==========================================

        # cursor.execute("""
        # CREATE TABLE IF NOT EXISTS TestSettings
        # (
        #     SettingName TEXT PRIMARY KEY,

        #     SettingValue TEXT
        # )
        # """)

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
                (2, "CHANNEL2")
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