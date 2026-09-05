import tkinter as tk

from widgets.live_tabs import LiveTabs

from pages.live_monitoring.efficiency_trend import EfficiencyTrendFrame
from pages.live_monitoring.live_table import LiveTableFrame
from pages.live_monitoring.live_temperature import LiveTemperatureFrame

from controllers.live_monitoring_controller import LiveMonitoringController


class LiveMonitoringPage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(parent, bg="#eef2f7")

        self.context = context
        
        
        #create Controller
        
        self.controller = LiveMonitoringController(self,self.context)

        self.create_ui()

    def create_ui(self):

        # Title
        title = tk.Label(
            self,
            text="Endurance - Live Monitoring",
            font=("Bookman Antiqua", 16, "bold"),
            bg="#eef2f7"
        )
        title.pack(pady=10)

        self.tabs_widget = LiveTabs(
    self,
    callback=self.controller.show_tab
        )
        self.tabs_widget.pack(fill="x", padx=10)

        self.content_frame = tk.Frame(
            self,
            bg="white"
        )
        self.content_frame.pack(
            fill="both",
            expand=True,
            padx=10,
            pady=10
        )

        self.tabs = {
    "trend": EfficiencyTrendFrame(self.content_frame,self.context),
    "table": LiveTableFrame(self.content_frame, self.context),
    "temperature": LiveTemperatureFrame(self.content_frame,self.context)
}

        self.context.live_table = self.tabs["table"]
         # OPEN DEFAULT TAB HERE
        self.tabs_widget.select_tab("table")

   
    def start_live_plot(self, selected_duts):
        
        self.controller.start_live_plot(
            selected_duts
        )

    def reset(self, selected_duts):

        if not selected_duts:
            return

        first_dut = selected_duts[0]

        if first_dut in (1, 2):
            channel_id = 1
        else:
            channel_id = 2

        self.tabs["trend"].reset(channel_id)
        self.tabs["table"].reset(channel_id)
        self.tabs["temperature"].reset(channel_id)

    # def reset(self, selected_duts):

    #     self.tabs["trend"].reset(selected_duts)
    #     self.tabs["table"].reset(selected_duts)
    #     self.tabs["temperature"].reset(selected_duts)

