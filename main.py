import tkinter as tk

from core.app_context import AppContext

from database.database_manager import DatabaseManager

from database.repositories.user_repository import UserRepository
from database.repositories.instrument_repository import InstrumentRepository
from database.repositories.channel_repository import ChannelRepository

from controllers.login_controller import LoginController
from controllers.app_controller import AppController

from views.menu_window import MenuWindow
from views.home_window import HomeScreen


def main():

    root = tk.Tk()

    root.title("Royal Enfield Dashboard")
    root.geometry("1400x800")

    # =====================================
    # APP CONTEXT
    # =====================================

    context = AppContext()
    context.root = root

    # =====================================
    # DATABASE
    # =====================================

    context.db = DatabaseManager()

    # =====================================
    # REPOSITORIES
    # =====================================

    context.user_repository = UserRepository(
        context.db
    )

    context.instrument_repository = InstrumentRepository(
        context.db
    )

    context.channel_repository = ChannelRepository(
        context.db
    )

    # =====================================
    # CONTROLLERS
    # =====================================

    context.login_controller = LoginController(
        context
    )

    context.app_controller = AppController(
        context
    )

    # =====================================
    # SCREENS
    # =====================================

    context.home_screen = HomeScreen(
        root,
        context
    )

    context.menu_window = MenuWindow(
        root,
        context
    )

    # Place both screens in same location
    context.home_screen.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    context.menu_window.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    # Show Home Screen first
    context.home_screen.tkraise()

    # =====================================
    # START APPLICATION
    # =====================================

    root.mainloop()


if __name__ == "__main__":
    main()