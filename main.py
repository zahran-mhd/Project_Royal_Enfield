import tkinter as tk

from core.app_context import AppContext

from database.database_manager import DatabaseManager

from database.repositories.user_repository import UserRepository
from database.repositories.instrument_repository import InstrumentRepository

from controllers.login_controller import LoginController
from controllers.app_controller import AppController

from views.home_window import HomeScreen


def main():

    root = tk.Tk()

    root.title("Royal Enfield Dashboard")

    root.geometry("1400x800")

    # =====================================
    # APP CONTEXT
    # =====================================

    app = AppContext()

    app.root = root

    # =====================================
    # DATABASE
    # =====================================

    app.db = DatabaseManager()

    # =====================================
    # REPOSITORIES
    # =====================================

    app.user_repository = UserRepository(
        app.db
    )

    app.instrument_repository = InstrumentRepository(
        app.db
    )

    # =====================================
    # CONTROLLERS
    # =====================================

    app.login_controller = LoginController(
        app
    )

    app.app_controller = AppController(
        app
    )

    # =====================================
    # HOME SCREEN
    # =====================================

    app.home_screen = HomeScreen(
        root,
        app
    )

    app.home_screen.pack(
        fill="both",
        expand=True
    )

    root.mainloop()


if __name__ == "__main__":
    main()