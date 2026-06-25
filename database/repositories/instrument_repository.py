from models.instrument_data import InstrumentData


class InstrumentRepository:

    def __init__(self, db):
        self.db = db

    # ------------------------------------------------
    # ADD INSTRUMENT
    # ------------------------------------------------
    def add(self, instrument: InstrumentData):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            INSERT INTO Instruments
            (
                InstrumentName,
                Address,
                InstrumentSNo,
                CalibrationDueDate,
                Status,
                IsLocked
            )
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status,
                instrument.is_locked
            )
        )

        instrument_id = cursor.lastrowid

        # Channel mapping
        if instrument.channel_id is not None:
            cursor.execute(
                """
                INSERT INTO ChannelInstrument
                (
                    ChannelID,
                    InstrumentID,
                    IsShared
                )
                VALUES (?, ?, ?)
                """,
                (
                    instrument.channel_id,
                    instrument_id,
                    instrument.is_shared
                )
            )

        self.db.conn.commit()
        print(f"Inserted Instrument ID: {instrument_id}")

        return instrument_id

    # ------------------------------------------------
    # UPDATE INSTRUMENT
    # ------------------------------------------------
    def update(self, instrument: InstrumentData):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            UPDATE Instruments
            SET
                InstrumentName=?,
                Address=?,
                InstrumentSNo=?,
                CalibrationDueDate=?,
                Status=?,
                IsLocked=?
            WHERE InstrumentID=?
            """,
            (
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status,
                instrument.is_locked,
                instrument.instrument_id
            )
        )

        # Remove old mapping
        cursor.execute(
            """
            DELETE FROM ChannelInstrument
            WHERE InstrumentID=?
            """,
            (instrument.instrument_id,)
        )

        # Insert new mapping
        if instrument.channel_id is not None:
            cursor.execute(
                """
                INSERT INTO ChannelInstrument
                (
                    ChannelID,
                    InstrumentID,
                    IsShared
                )
                VALUES (?, ?, ?)
                """,
                (
                    instrument.channel_id,
                    instrument.instrument_id,
                    instrument.is_shared
                )
            )

        self.db.conn.commit()

    # ------------------------------------------------
    # DELETE INSTRUMENT
    # ------------------------------------------------
    def delete(self, instrument_id):

        cursor = self.db.conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM ChannelInstrument
                WHERE InstrumentID=?
                """,
                (instrument_id,)
            )

            cursor.execute(
                """
                DELETE FROM Instruments
                WHERE InstrumentID=?
                """,
                (instrument_id,)
            )

            self.db.conn.commit()

        except Exception as e:
            self.db.conn.rollback()
            print("Delete Error:", e)
            raise

    # ------------------------------------------------
    # GET ALL
    # ------------------------------------------------
    def get_all(self):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                I.InstrumentID,
                I.InstrumentName,
                I.Address,
                I.InstrumentSNo,
                I.CalibrationDueDate,
                I.Status,
                I.IsLocked,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I
            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID
            """
        )

        rows = cursor.fetchall()

        return [
            InstrumentData(
                instrument_id=row["InstrumentID"],
                instrument_name=row["InstrumentName"],
                address=row["Address"],
                instrument_sno=row["InstrumentSNo"],
                calibration_due_date=row["CalibrationDueDate"],
                status=row["Status"],
                is_locked=row["IsLocked"],
                channel_id=row["ChannelID"],
                is_shared=row["IsShared"] if row["IsShared"] else 0
            )
            for row in rows
        ]

    # ------------------------------------------------
    # GET BY ID
    # ------------------------------------------------
    def get_by_id(self, instrument_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                I.InstrumentID,
                I.InstrumentName,
                I.Address,
                I.InstrumentSNo,
                I.CalibrationDueDate,
                I.Status,
                I.IsLocked,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I
            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID
            WHERE I.InstrumentID = ?
            """,
            (instrument_id,)
        )

        row = cursor.fetchone()

        if not row:
            return None

        return InstrumentData(
            instrument_id=row["InstrumentID"],
            instrument_name=row["InstrumentName"],
            address=row["Address"],
            instrument_sno=row["InstrumentSNo"],
            calibration_due_date=row["CalibrationDueDate"],
            status=row["Status"],
            is_locked=row["IsLocked"],
            channel_id=row["ChannelID"],
            is_shared=row["IsShared"] if row["IsShared"] else 0
        )

    # ------------------------------------------------
    # GET BY CHANNEL
    # ------------------------------------------------
    def get_by_channel(self, channel_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                I.InstrumentID,
                I.InstrumentName,
                I.Address,
                I.InstrumentSNo,
                I.CalibrationDueDate,
                I.Status,
                I.IsLocked,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I
            INNER JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID
            WHERE CI.ChannelID = ?
            """,
            (channel_id,)
        )

        rows = cursor.fetchall()

        return [
            InstrumentData(
                instrument_id=row["InstrumentID"],
                instrument_name=row["InstrumentName"],
                address=row["Address"],
                instrument_sno=row["InstrumentSNo"],
                calibration_due_date=row["CalibrationDueDate"],
                status=row["Status"],
                is_locked=row["IsLocked"],
                channel_id=row["ChannelID"],
                is_shared=row["IsShared"] if row["IsShared"] else 0
            )
            for row in rows
        ]