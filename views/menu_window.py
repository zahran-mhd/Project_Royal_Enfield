import tkinter as tk

from widgets.sidebar import Sidebar
from widgets.header import Header
from widgets.sub_header import SubHeader
from widgets.footer import Footer

from pages.test_settings_page import TestSettingsPage
from pages.configuration_page import ConfigurationPage
from pages.parameter_settings_page import ParameterSettingsPage
from pages.alarm_settings_page import AlarmSettingsPage
from pages.live_monitoring_page import LiveMonitoringPage
from pages.line_regulation_page import LineRegulationPage
from pages.load_regulation_page import LoadRegulationPage
from pages.historical_trend_page import HistoricalTrendPage
from pages.report_page import ReportsPage

from controllers.app_controller import AppController


class MenuWindow(tk.Frame):

    def __init__(self,parent,context):
        super().__init__(parent)

        
        self.configure(bg="white")
        self.context = context

        self.controller = context.app_controller

        # ================= Controller =================
        # self.controller = AppController()

        # ================= Header =================
        self.header = Header(self)
        self.header.pack(side="top", fill="x")

        # ================= Main Body =================
        body_frame = tk.Frame(self, bg="white")
        body_frame.pack(fill="both", expand=True)

        # ================= Sidebar =================
        self.sidebar = Sidebar(body_frame, self.controller)
        self.sidebar.pack(side="left", fill="y")
        
        self.controller.register_sidebar(self.sidebar)

        # ================= Right Section =================
        right_frame = tk.Frame(body_frame, bg="#f5f5f5")
        right_frame.pack(side="right", fill="both", expand=True)

        # ================= Sub Header =================
        self.sub_header = SubHeader(right_frame)
        self.sub_header.pack(side="top", fill="x")

        # ================= Footer =================
        self.footer = Footer(right_frame,self.context)
        self.footer.pack(side="bottom", fill="x")

        # ================= Content Area =================
        self.content = tk.Frame(right_frame, bg="#f5f5f5")
        self.content.pack(fill="both", expand=True)

        # ================= Pages =================

        test_settings_page = TestSettingsPage(self.content, self.context)
        configuration_page = ConfigurationPage(self.content,self.context)
        parameter_settings_page = ParameterSettingsPage(self.content)
        alarm_settings_page = AlarmSettingsPage(self.content)
        live_monitoring_page = LiveMonitoringPage(self.content,self.context)
        line_regulation_page = LineRegulationPage(self.content)
        load_regulation_page = LoadRegulationPage(self.content)
        historical_trend_page = HistoricalTrendPage(self.content, self.context)
        
        report_page = ReportsPage(self.content)

        self.controller.register_page(
    "Test Settings",
    test_settings_page
)

        self.controller.register_page(
            "Configuration",
            configuration_page
        )

        self.controller.register_page(
            "Parameter Settings",
            parameter_settings_page
        )

        self.controller.register_page(
            "Alarm Settings",
            alarm_settings_page
        )

        self.controller.register_page(
            "Endurance-Live Monitoring",
            live_monitoring_page
        )

        self.controller.register_page(
            "Line Regulation",
            line_regulation_page
        )

        self.controller.register_page(
            "Load Regulation",
            load_regulation_page
        )

        self.controller.register_page(
            "Historical Trend",
            historical_trend_page
        )

        self.controller.register_page(
            "Report",
            report_page
        )

        # ================= Place Pages =================

        for page in self.controller.pages.values():
            page.place(
                relx=0,
                rely=0,
                relwidth=1,
                relheight=1
            )
            
        
        # ================= Default Page =================

        self.controller.show_page("Test Settings")