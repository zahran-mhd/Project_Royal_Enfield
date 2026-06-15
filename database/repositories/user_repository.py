# database/repositories/user_repository.py

class UserRepository:

    def __init__(self, db):

        self.db = db

    # ----------------------------------------
    # ADD USER
    # ----------------------------------------

    def add_user(
        self,
        username,
        password,
        role
    ):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            INSERT INTO Users
            (
                Username,
                Password,
                Role
            )
            VALUES (?, ?, ?)
            """,
            (
                username,
                password,
                role
            )
        )

        self.db.commit()

    # ----------------------------------------
    # GET USER
    # ----------------------------------------

    def get_user(self, username):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM Users
            WHERE Username = ?
            """,
            (username,)
        )

        return cursor.fetchone()

    # ----------------------------------------
    # AUTHENTICATE
    # ----------------------------------------

    def authenticate(
        self,
        username,
        password
    ):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM Users
            WHERE Username = ?
            AND Password = ?
            """,
            (
                username,
                password
            )
        )

        row = cursor.fetchone()

        return row

    # ----------------------------------------
    # UPDATE USER
    # ----------------------------------------

    def update_user(
        self,
        username,
        password,
        role
    ):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            UPDATE Users
            SET
                Password = ?,
                Role = ?
            WHERE Username = ?
            """,
            (
                password,
                role,
                username
            )
        )

        self.db.commit()

    # ----------------------------------------
    # DELETE USER
    # ----------------------------------------

    def delete_user(self, username):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            DELETE FROM Users
            WHERE Username = ?
            """,
            (username,)
        )

        self.db.commit()

    # ----------------------------------------
    # GET ALL USERS
    # ----------------------------------------

    def get_all_users(self):

        cursor = self.db.conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM Users
            ORDER BY Username
            """
        )

        return cursor.fetchall()