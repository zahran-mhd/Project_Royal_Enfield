from models.instrument_data import InstrumentData


class InstrumentRepository:

    def __init__(self, db):

        self.db = db

    # ------------------------------------------------
    # ADD INSTRUMENT
    # ------------------------------------------------

    def add(self, instrument: InstrumentData):

        cursor = self.db.conn.cursor()

        # Insert Instrument
        cursor.execute(
            """
            INSERT INTO Instruments
            (
                Sno,
                InstrumentName,
                Address,
                InstrumentSNo,
                CalibrationDueDate,
                Status,
                IsLocked
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            (
                instrument.sno,
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status,
                instrument.is_locked
            )
        )

        instrument_id = cursor.lastrowid

        # Create Channel Mapping

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

        self.db.commit()
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
                Sno=?,
                InstrumentName=?,
                Address=?,
                InstrumentSNo=?,
                CalibrationDueDate=?,
                Status=?,
                IsLocked=?
            WHERE InstrumentID=?
            """,
            (
                instrument.sno,
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                instrument.status,
                instrument.is_locked,
                instrument.instrument_id
            )
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

        self.db.commit()

    # ------------------------------------------------
    # DELETE INSTRUMENT
    # ------------------------------------------------

    def delete(self, instrument_id):

        cursor = self.db.conn.cursor()

        # Delete mapping first

        cursor.execute(
            """
            DELETE FROM ChannelInstrument
            WHERE InstrumentID=?
            """,
            (instrument_id,)
        )

        # Delete instrument

        cursor.execute(
            """
            DELETE FROM Instruments
            WHERE InstrumentID=?
            """,
            (instrument_id,)
        )

        self.db.commit()

    def get_all(self):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT

                I.InstrumentID,
                I.Sno,
                I.InstrumentName,
                I.Address,
                I.InstrumentSNo,
                I.CalibrationDueDate,
                I.Status,
                I.IsLocked,

                C.ChannelID,
                C.ChannelName,

                CI.IsShared

            FROM Instruments I

            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID

            LEFT JOIN Channel C
                ON CI.ChannelID = C.ChannelID

            ORDER BY I.Sno
            """
        )

        rows = cursor.fetchall()

        instruments = []

        for row in rows:

            instruments.append(
                InstrumentData(
                    instrument_id=row["InstrumentID"],
                    sno=row["Sno"],
                    instrument_name=row["InstrumentName"],
                    address=row["Address"],
                    instrument_sno=row["InstrumentSNo"],
                    calibration_due_date=row["CalibrationDueDate"],
                    status=row["Status"],
                    is_locked=row["IsLocked"],
                    channel_id=row["ChannelID"],
                    is_shared=row["IsShared"] if row["IsShared"] is not None else 0
                )
            )

        return instruments
    

    def get_by_id(self, instrument_id):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT

                I.InstrumentID,
                I.Sno,
                I.InstrumentName,
                I.Address,
                I.InstrumentSNo,
                I.CalibrationDueDate,
                I.Status,
                I.IsLocked,

                C.ChannelID,
                C.ChannelName,

                CI.IsShared

            FROM Instruments I

            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID

            LEFT JOIN Channel C
                ON CI.ChannelID = C.ChannelID

            WHERE I.InstrumentID = ?
            """,
            (instrument_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return InstrumentData(
            instrument_id=row["InstrumentID"],
            sno=row["Sno"],
            instrument_name=row["InstrumentName"],
            address=row["Address"],
            instrument_sno=row["InstrumentSNo"],
            calibration_due_date=row["CalibrationDueDate"],
            status=row["Status"],
            is_locked=row["IsLocked"],
            channel_id=row["ChannelID"],
            is_shared=row["IsShared"] if row["IsShared"] is not None else 0
        )
    
    def get_by_sno(self, sno):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM Instruments
            WHERE Sno = ?
            """,
            (sno,)
        )

        return cursor.fetchone()
    
    
    def get_next_sno(self):
        cursor = self.db.conn.cursor()

        cursor.execute(
            "SELECT COALESCE(MAX(Sno), 0) + 1 AS NextSno FROM Instruments"
        )

        return cursor.fetchone()["NextSno"]