# models/app_state.py

from dataclasses import dataclass


@dataclass
class AppState:

    # -----------------------------
    # USER
    # -----------------------------

    current_user: str = ""

    current_role: str = ""

    logged_in: bool = False

    # -----------------------------
    # NAVIGATION
    # -----------------------------

    current_page: str = "test_settings"

    # -----------------------------
    # TEST STATUS
    # -----------------------------

    test_running: bool = False

    test_paused: bool = False

    emergency_stop: bool = False

    # -----------------------------
    # INSTRUMENT STATUS
    # -----------------------------

    instruments_connected: bool = False

    # -----------------------------
    # ALARM STATUS
    # -----------------------------

    alarm_active: bool = False

    alarm_message: str = ""

    # -----------------------------
    # APPLICATION STATUS
    # -----------------------------

    shutdown_requested: bool = False