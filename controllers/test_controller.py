# controllers/test_controller.py

from datetime import datetime


class TestController:

    def __init__(self, context):

        self.context = context
        # self.controller = context.test_repository

    def start_test(self,channel_id,values):

        # Already running?
        if self.context.app_state.test_running:
            return

        # Update state

        self.context.app_state.test_running = True

        # Create test session

        self.context.test_session.start_time = (
            datetime.now()
        )

        self.context.test_session.status = "Running"

        
        self.context.test_repository.save_settings(channel_id,values)
        # self.run_test(channel_id)
        # Start instruments

        self.app.instrument_manager.start()

        print("Test Started")
    
    def stop_test(self):

        self.app.instrument_manager.stop()

        self.app.app_state.test_running = False

        self.app.test_session.status = "Completed"

        print("Test Stopped")