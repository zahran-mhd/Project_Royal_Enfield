import tkinter as tk

from core.app_context import AppContext

from database.database_manager import DatabaseManager

from database.repositories.user_repository import UserRepository
from database.repositories.instrument_repository import InstrumentRepository
from database.repositories.parameter_repository import ParameterRepository
from database.repositories.channel_repository import ChannelRepository
from database.repositories.test_repository import TestRepository

from controllers.login_controller import LoginController
from controllers.app_controller import AppController
from controllers.historical_trend_controller import HistoricalTrendController
from controllers.test_controller import TestController
from controllers.test_settings_controller import TestSettingsController
from controllers.parameter_settings_controller import ParameterSettingsController
from controllers.efficiency_trend_controller import EfficiencyTrendController
from instruments.workers.alarm_monitor import AlarmMonitor

from instruments.instrument_manager import InstrumentManager
from instruments.can_manager import CANManager
from instruments.dbc_decoder import DBCDecoder

from views.menu_window import MenuWindow
from views.home_window import HomeScreen


def main():

    # =====================================
    # ROOT WINDOW
    # =====================================

    root = tk.Tk()

    root.title("Royal Enfield Dashboard")
    root.geometry("1400x800")

    # =====================================
    # APP CONTEXT
    # =====================================

    context = AppContext()

    context.root = root

    # Important:
    # MenuWindow will be created only after login
    context.menu_window = None

    # =====================================
    # DATABASE
    # =====================================

    context.db = DatabaseManager()

    context.decoder = DBCDecoder()
    # =====================================
    # REPOSITORIES
    # =====================================

    context.user_repository = UserRepository(
        context.db
    )
 
    context.instrument_repository = InstrumentRepository(
        context.db
    )

    context.parameter_repository = ParameterRepository(
            context.db
        )

    context.channel_repository = ChannelRepository(
        context.db
    )

    context.test_repository = TestRepository(
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

    context.historical_trend_controller = (
        HistoricalTrendController(context)
    )


    context.instrument_manager = InstrumentManager(
        context
)
    context.instrument_manager.connect_all()
    
    context.can_manager = CANManager(
    context
    )

    context.test_controller = TestController(
        context
    )

    context.test_settings_controller = (
        TestSettingsController(context)
    )

    context.parameter_settings_controller = (
            ParameterSettingsController(context,context.db)
    )

    
    # context.efficiency_trend_controller = (
    #     EfficiencyTrendController(context)
    # )
    # =====================================
    # HOME SCREEN
    # =====================================

    context.home_screen = HomeScreen(
        root,
        context
    )

    context.home_screen.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )


    context.alarm_monitor = AlarmMonitor(context)
    context.alarm_monitor.start()
    # =====================================
    # CREATE MENU WINDOW FUNCTION
    # =====================================

    def create_menu_window():

        # If old MenuWindow exists,
        # destroy it first
        if context.menu_window is not None:

            context.menu_window.destroy()

            context.menu_window = None

        # Create completely fresh MenuWindow
        context.menu_window = MenuWindow(
            root,
            context
        )

        context.menu_window.place(
            relx=0,
            rely=0,
            relwidth=1,
            relheight=1
        )

        # Show MenuWindow
        context.menu_window.tkraise()

    # Make this function accessible
    # from HomeSidebar / other classes
    context.create_menu_window = create_menu_window

    # =====================================
    # SHOW HOME SCREEN FIRST
    # =====================================

    context.home_screen.tkraise()

    # =====================================
    # START APPLICATION
    # =====================================

    root.mainloop()


    def on_close():

        context.instrument_manager.disconnect_all()

        if context.can_manager:
            context.can_manager.disconnect_all()

        root.destroy()


    root.protocol(
        "WM_DELETE_WINDOW",
        on_close
    )




if __name__ == "__main__":

    main()