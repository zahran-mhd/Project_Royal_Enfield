from models.instrument_data import InstrumentData


class InstrumentRepository:

    def __init__(self, db):
        self.db = db

    # ------------------------------------------------
    # ADD INSTRUMENT
    # ------------------------------------------------

    def add(self, instrument: InstrumentData):

        cursor = self.db.conn.cursor()

        # Check if instrument already exists
        cursor.execute(
            """
            SELECT InstrumentID
            FROM Instruments
            WHERE InstrumentSNo=?
            """,
            (instrument.instrument_sno,)
        )

        row = cursor.fetchone()

        if row:
            instrument_id = row[0]
        else:
            cursor.execute(
                """
                INSERT INTO Instruments
                (
                    InstrumentName,
                    InstrumentTypeID,
                    Address,
                    InstrumentSNo,
                    CalibrationDueDate
                )
                VALUES
                (
                    ?, ?, ?, ?, ?
                )
                """,
                (
                    instrument.instrument_name,
                    instrument.instrument_type_id,
                    instrument.address,
                    instrument.instrument_sno,
                    instrument.calibration_due_date
                )
            )

            instrument_id = cursor.lastrowid

        # -----------------------------------
        # Channel mapping
        # -----------------------------------

        channel_ids = [instrument.channel_id]

        if instrument.is_shared:
            if instrument.channel_id == 1:
                channel_ids.append(2)
            elif instrument.channel_id == 2:
                channel_ids.append(1)

        for channel_id in set(channel_ids):

            cursor.execute(
                """
                SELECT 1
                FROM ChannelInstrument
                WHERE ChannelID=? AND InstrumentID=?
                """,
                (channel_id, instrument_id)
            )

            if cursor.fetchone() is None:
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
                        channel_id,
                        instrument_id,
                        instrument.is_shared
                    )
                )

        self.db.conn.commit()

        return instrument_id
    # def add(self, instrument: InstrumentData):

    #     cursor = self.db.conn.cursor()

    #     cursor.execute(
    #         """
    #         INSERT INTO Instruments
    #         (
    #             InstrumentName,
    #             Address,
    #             InstrumentSNo,
    #             CalibrationDueDate,
    #             Status,
    #             IsLocked
    #         )
    #         VALUES (?, ?, ?, ?, ?, ?)
    #         """,
    #         (
    #             instrument.instrument_name,
    #             instrument.address,
    #             instrument.instrument_sno,
    #             instrument.calibration_due_date,
    #             instrument.status,
    #             instrument.is_locked
    #         )
    #     )

    #     instrument_id = cursor.lastrowid

    #     # Channel mapping
    #     if instrument.channel_id is not None:
    #         cursor.execute(
    #             """
    #             INSERT INTO ChannelInstrument
    #             (
    #                 ChannelID,
    #                 InstrumentID,
    #                 IsShared
    #             )
    #             VALUES (?, ?, ?)
    #             """,
    #             (
    #                 instrument.channel_id,
    #                 instrument_id,
    #                 instrument.is_shared
    #             )
    #         )

    #     self.db.conn.commit()
    #     print(f"Inserted Instrument ID: {instrument_id}")

    #     return instrument_id

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
                IsLocked=?
            WHERE InstrumentID=?
            """,
            (
                instrument.instrument_name,
                instrument.address,
                instrument.instrument_sno,
                instrument.calibration_due_date,
                # instrument.status,
                instrument.is_locked,
                instrument.instrument_id
            )
        )

        cursor.execute(
            """
            DELETE FROM ChannelInstrument
            WHERE InstrumentID=?
            """,
            (instrument.instrument_id,)
        )

        channel_ids = [instrument.channel_id]

        if instrument.is_shared:
            if instrument.channel_id == 1:
                channel_ids.append(2)
            elif instrument.channel_id == 2:
                channel_ids.append(1)

        for channel_id in set(channel_ids):
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
                    channel_id,
                    instrument.instrument_id,
                    instrument.is_shared
                )
            )

        self.db.conn.commit()
    # def update(self, instrument: InstrumentData):

    #     cursor = self.db.conn.cursor()

    #     cursor.execute(
    #         """
    #         UPDATE Instruments
    #         SET
    #             InstrumentName=?,
    #             Address=?,
    #             InstrumentSNo=?,
    #             CalibrationDueDate=?,
    #             Status=?,
    #             IsLocked=?
    #         WHERE InstrumentID=?
    #         """,
    #         (
    #             instrument.instrument_name,
    #             instrument.address,
    #             instrument.instrument_sno,
    #             instrument.calibration_due_date,
    #             instrument.status,
    #             instrument.is_locked,
    #             instrument.instrument_id
    #         )
    #     )

    #     # Remove old mapping
    #     cursor.execute(
    #         """
    #         DELETE FROM ChannelInstrument
    #         WHERE InstrumentID=?
    #         """,
    #         (instrument.instrument_id,)
    #     )

    #     # Insert new mapping
    #     if instrument.channel_id is not None:
    #         cursor.execute(
    #             """
    #             INSERT INTO ChannelInstrument
    #             (
    #                 ChannelID,
    #                 InstrumentID,
    #                 IsShared
    #             )
    #             VALUES (?, ?, ?)
    #             """,
    #             (
    #                 instrument.channel_id,
    #                 instrument.instrument_id,
    #                 instrument.is_shared
    #             )
    #         )

    #     self.db.conn.commit()

    # ------------------------------------------------
    # DELETE INSTRUMENT
    # ------------------------------------------------
    # def delete(self, instrument_id):

    #     cursor = self.db.conn.cursor()

    #     try:
    #         cursor.execute(
    #             """
    #             DELETE FROM ChannelInstrument
    #             WHERE InstrumentID=?
    #             """,
    #             (instrument_id,)
    #         )

    #         cursor.execute(
    #             """
    #             DELETE FROM Instruments
    #             WHERE InstrumentID=?
    #             """,
    #             (instrument_id,)
    #         )

    #         self.db.conn.commit()

    #     except Exception as e:
    #         self.db.conn.rollback()
    #         print("Delete Error:", e)
    #         raise

    def delete(self, instrument_id, channel_id):

        cursor = self.db.conn.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM ChannelInstrument
                WHERE InstrumentID=?
                AND ChannelID=?
                """,
                (instrument_id, channel_id)
            )

            cursor.execute(
                """
                SELECT COUNT(*)
                FROM ChannelInstrument
                WHERE InstrumentID=?
                """,
                (instrument_id,)
            )

            count = cursor.fetchone()[0]

            if count == 0:
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
                I.ConnectionStatus,
                I.IsLocked,

                T.InstrumentTypeID,
                T.TypeName,
                T.DriverClass,
                T.WorkerClass,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I

            INNER JOIN InstrumentType T
                ON I.InstrumentTypeID = T.InstrumentTypeID

            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID
            """
        )

        rows = cursor.fetchall()

        return [

            InstrumentData(

                instrument_id=row["InstrumentID"],

                instrument_name=row["InstrumentName"],

                instrument_type_id=row["InstrumentTypeID"],

                instrument_type=row["TypeName"],

                driver_class=row["DriverClass"],

                worker_class=row["WorkerClass"],

                address=row["Address"],

                instrument_sno=row["InstrumentSNo"],

                calibration_due_date=row["CalibrationDueDate"],

                status=row["ConnectionStatus"],

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
                I.ConnectionStatus,
                I.IsLocked,

                T.InstrumentTypeID,
                T.TypeName,
                T.DriverClass,
                T.WorkerClass,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I

            INNER JOIN InstrumentType T
                ON I.InstrumentTypeID = T.InstrumentTypeID

            LEFT JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID

            WHERE I.InstrumentID=?
            """,
            (instrument_id,)
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return InstrumentData(

            instrument_id=row["InstrumentID"],

            instrument_name=row["InstrumentName"],

            instrument_type_id=row["InstrumentTypeID"],

            instrument_type=row["TypeName"],

            driver_class=row["DriverClass"],

            worker_class=row["WorkerClass"],

            address=row["Address"],

            instrument_sno=row["InstrumentSNo"],

            calibration_due_date=row["CalibrationDueDate"],

            status=row["ConnectionStatus"],

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
                I.ConnectionStatus,
                I.IsLocked,

                T.InstrumentTypeID,
                T.TypeName,
                T.DriverClass,
                T.WorkerClass,

                CI.ChannelID,
                CI.IsShared

            FROM Instruments I

            INNER JOIN InstrumentType T
                ON I.InstrumentTypeID = T.InstrumentTypeID

            INNER JOIN ChannelInstrument CI
                ON I.InstrumentID = CI.InstrumentID

            WHERE CI.ChannelID=?
            """,
            (channel_id,)
        )

        rows = cursor.fetchall()

        return [

            InstrumentData(

                instrument_id=row["InstrumentID"],

                instrument_name=row["InstrumentName"],

                instrument_type_id=row["InstrumentTypeID"],

                instrument_type=row["TypeName"],

                driver_class=row["DriverClass"],

                worker_class=row["WorkerClass"],

                address=row["Address"],

                instrument_sno=row["InstrumentSNo"],

                calibration_due_date=row["CalibrationDueDate"],

                status=row["ConnectionStatus"],

                is_locked=row["IsLocked"],

                channel_id=row["ChannelID"],

                is_shared=row["IsShared"] if row["IsShared"] else 0

            )

            for row in rows
        ]

    def update_connection_status(self, instrument_id, status):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            UPDATE Instruments
            SET ConnectionStatus=?
            WHERE InstrumentID=?
            """,
            (status, instrument_id)
        )

        self.db.conn.commit()

    def get_instrument_types(self):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT
                InstrumentTypeID,
                TypeName
            FROM InstrumentType
            ORDER BY TypeName
            """
        )

        return cursor.fetchall()

    def get_daq_channels(
        self,
        channel_id,
        instrument_id
    ):
        
        cursor = self.db.conn.cursor()

        query = """
            SELECT
                DAQChannel,
                Slot,
                ParameterName,
                MeasurementType,
                ThermocoupleType
            FROM DAQChannel
            WHERE ChannelID = ?
            AND InstrumentID = ?
            AND IsEnabled = 1
            ORDER BY Slot, DAQChannel
        """

        rows = cursor.execute(
            query,
            (
                channel_id,
                instrument_id
            )
        ).fetchall()

        return rows

    def get_daq_configuration(
        self,
        channel_id,
        instrument_id
    ):
        cursor = self.db.conn.cursor()
        query = """
            SELECT
                DAQChannelID,
                ChannelID,
                InstrumentID,
                Slot,
                DAQChannel,
                ParameterName,
                MeasurementType,
                ThermocoupleType
            FROM DAQChannel
            WHERE ChannelID = ?
            AND InstrumentID = ?
            AND IsEnabled = 1
            ORDER BY Slot, DAQChannel
        """

        rows = cursor.execute(
            query,
            (
                channel_id,
                instrument_id
            )
        ).fetchall()

        return [
            {
                "daq_channel_id": row["DAQChannelID"],
                "channel_id": row["ChannelID"],
                "instrument_id": row["InstrumentID"],
                "slot": row["Slot"],
                "daq_channel": str(row["DAQChannel"]),
                "parameter_name": row["ParameterName"],
                "measurement_type": row["MeasurementType"],
                "thermocouple_type": row["ThermocoupleType"]
            }
            for row in rows
        ]

    