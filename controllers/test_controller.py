# controllers/test_controller.py

from datetime import datetime


class TestController:

    def __init__(self, app):

        self.app = app

    def start_test(self):

        # Already running?
        if self.app.app_state.test_running:
            return

        # Update state

        self.app.app_state.test_running = True

        # Create test session

        self.app.test_session.start_time = (
            datetime.now()
        )

        self.app.test_session.status = "Running"

        # Start instruments

        self.app.instrument_manager.start()

        print("Test Started")
    
    def stop_test(self):

        self.app.instrument_manager.stop()

        self.app.app_state.test_running = False

        self.app.test_session.status = "Completed"

        print("Test Stopped")