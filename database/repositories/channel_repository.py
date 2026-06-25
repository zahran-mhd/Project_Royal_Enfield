class ChannelRepository:

    def __init__(self, db):
        self.db = db

    
    def get_all_channels(self):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT ChannelID, ChannelName
            FROM Channel
            ORDER BY ChannelID
        """)

        rows = cursor.fetchall()

        return [
            {
                "ChannelID": row[0],
                "ChannelName": row[1]
            }
            for row in rows
        ]

    def get_channel_id(self, channel_name):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            SELECT ChannelID
            FROM Channel
            WHERE ChannelName = ?
        """, (channel_name,))

        row = cursor.fetchone()

        if row:
            return row[0]

        return None

    def update_channel(self, channel_id, new_name):

        cursor = self.db.conn.cursor()

        cursor.execute("""
            UPDATE Channel
            SET ChannelName = ?
            WHERE ChannelID = ?
        """, (new_name, channel_id))

        self.db.conn.commit()