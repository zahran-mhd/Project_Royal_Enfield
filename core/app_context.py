# core/app_context.py

from models.data_model import DataModel
from models.app_state import AppState
from models.test_session import TestSession
from instruments.dbc_decoder import DBCDecoder
from pages.live_monitoring.live_table import LiveTableFrame
from services.data_logger import EnduranceDataLogger
class AppContext:

    def __init__(self):
        
        self.current_user = None
        
        self.selected_duts = []
        
      

        # ==================================
        # RUNTIME MODELS
        # ==================================

        self.data_model = DataModel()

        self.app_state = AppState()

        self.test_session = TestSession()
        
        self.dbc_decoder = DBCDecoder()


        # ==================================
        # CONFIGURATION MODELS
        # ==================================

        self.instrument_config = None

        self.user_config = None

        self.test_settings = None

        self.threshold_settings = None

        # ==================================
        # DATABASE
        # ==================================

        self.db = None

        # ==================================
        # REPOSITORIES
        # ==================================

        self.user_repository = None

        self.instrument_repository = None

        self.settings_repo = None

        self.threshold_repo = None

        self.result_repo = None

        self.parameter_repository = None

        # ==================================
        # SERVICES
        # ==================================

        self.logger = None

        self.alarm_service = None

        self.report_service = None

        self.csv_service = None

        # ==================================
        # INSTRUMENTS
        # ==================================

        self.asr3400 = None

        self.rp5935a = None

        self.el34243a = None

        self.el4913a = None

        self.pw3337 = None

        self.daq970a = None

        # ==================================
        # INSTRUMENT MANAGER
        # ==================================

        self.instrument_manager = None

        # ==================================
        # CONTROLLERS
        # ==================================

        self.login_controller = None

        self.settings_controller = None

        self.test_controller = None

        self.graph_controller = None

        self.historical_trend_controller = None

        # ==================================
        # GUI REFERENCES (OPTIONAL)
        # ==================================

        self.root = None

        self.main_window = None

        self.graph_window = None

        self.settings_window = None


        self.selected_dut_types = {}

        self.can_values = {}

        self.can_values = {
            1: {      # Channel 1
                "PCAN_USBBUS1": {},
                "PCAN_USBBUS2": {}
            },
            2: {      # Channel 2
                "PCAN_USBBUS3": {},
                "PCAN_USBBUS4": {}
            }
        }

        self.hardware_values = {
            1: {},
            2: {},
            3: {},
            4: {}
            }
        self.data_logger = EnduranceDataLogger(
            base_folder="CSV_Logs",
            report_folder="Report"
        )