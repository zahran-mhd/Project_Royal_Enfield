import tkinter as tk

from core.app_context import AppContext

from database.database_manager import DatabaseManager

from database.repositories.user_repository import UserRepository
from database.repositories.instrument_repository import InstrumentRepository
from database.repositories.channel_repository import ChannelRepository
from database.repositories.test_repository import TestRepository

from controllers.login_controller import LoginController
from controllers.app_controller import AppController
from controllers.historical_trend_controller import HistoricalTrendController
from controllers.test_controller import TestController
from instruments.instrument_manager import InstrumentManager

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

    context.test_repository= TestRepository(context.db)

    # =====================================
    # CONTROLLERS
    # =====================================

    context.login_controller = LoginController(
        context
    )

    context.app_controller = AppController(
        context
    )
    context.historical_trend_controller = HistoricalTrendController(context)

    context.instrument_manager = InstrumentManager(
    context
)
    context.test_controller=TestController(context)
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
    
    # context.menu_window.tkraise()

    # =====================================
    # START APPLICATION
    # =====================================

    root.mainloop()


if __name__ == "__main__":
    main()