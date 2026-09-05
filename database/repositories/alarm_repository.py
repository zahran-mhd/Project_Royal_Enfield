class AlarmRepository:

    def __init__(self, conn):
        self.conn = conn

    def get_all_alarms(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                AlarmID,
                AlarmName,
                IsEnabled
            FROM AlarmSettings
            ORDER BY AlarmID
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "alarm_id": row["AlarmID"],
                "alarm_name": row["AlarmName"],
                "is_enabled": bool(row["IsEnabled"])
            }
            for row in rows
        ]

    def update_alarm_settings(self, alarm_settings):

        cursor = self.conn.cursor()

        cursor.executemany(
            """
            UPDATE AlarmSettings
            SET IsEnabled = ?
            WHERE AlarmID = ?
            """,
            [
                (
                    1 if alarm["is_enabled"] else 0,
                    alarm["alarm_id"]
                )
                for alarm in alarm_settings
            ]
        )

        self.conn.commit()

    def get_enabled_alarms(self):

        cursor = self.conn.cursor()

        cursor.execute(
            """
            SELECT
                AlarmID,
                AlarmName
            FROM AlarmSettings
            WHERE IsEnabled = 1
            ORDER BY AlarmID
            """
        )

        rows = cursor.fetchall()

        return [
            {
                "alarm_id": row["AlarmID"],
                "alarm_name": row["AlarmName"]
            }
            for row in rows
        ]