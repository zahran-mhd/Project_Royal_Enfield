import tkinter as tk

from core.app_context import AppContext

from database.database_manager import DatabaseManager


from database.repositories.user_repository import UserRepository
from database.repositories.instrument_repository import InstrumentRepository

from controllers.login_controller import LoginController
from controllers.app_controller import AppController
from controllers.historical_trend_controller import HistoricalTrendController
from instruments.instrument_manager import InstrumentManager

from views.home_window import HomeScreen
from views.menu_window import MenuWindow


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
    
    app.historical_trend_controller = HistoricalTrendController(app)
   
    app.instrument_manager = InstrumentManager(
    app
)

    # =====================================
    # HOME SCREEN
    # =====================================

    # app.home_screen = HomeScreen(
    #     root,
    #     app
    # )
    # app.home_screen = HomeScreen(
    #     root,
    #     app
    # )

    # app.home_screen.pack(
    #     fill="both",
    #     expand=True
    # )

    app.home_screen = HomeScreen(root, app)

    app.menu_window = MenuWindow(root, app)

    app.home_screen.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    app.menu_window.place(
        relx=0,
        rely=0,
        relwidth=1,
        relheight=1
    )

    app.home_screen.tkraise()

    root.mainloop()


if __name__ == "__main__":
    main()