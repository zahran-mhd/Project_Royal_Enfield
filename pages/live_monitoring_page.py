import tkinter as tk

from widgets.live_tabs import LiveTabs

from pages.live_monitoring.efficiency_trend import EfficiencyTrendFrame
from pages.live_monitoring.live_table import LiveTableFrame
from pages.live_monitoring.live_temperature import LiveTemperatureFrame


class LiveMonitoringPage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(parent, bg="#eef2f7")

        self.context = context

        self.create_ui()

    def create_ui(self):

        # Title
        title = tk.Label(
            self,
            text="Endurance - Live Monitoring",
            font=("Segoe UI", 16, "bold"),
            bg="#eef2f7"
        )
        title.pack(pady=10)

        self.tabs_widget = LiveTabs(
    self,
    callback=self.show_tab
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
        # OPEN DEFAULT TAB HERE
        self.tabs_widget.select_tab("trend")

    def show_tab(self, tab_name):

        for frame in self.tabs.values():
            frame.pack_forget()

        self.tabs[tab_name].pack(fill="both", expand=True)

        # print(f"{tab_name} tab loaded")
        
    def start_live_plot(self, selected_duts):

        # Switch to the Trend tab
        self.tabs_widget.select_tab("trend")

        # Start the plot in the EfficiencyTrendFrame
        self.tabs["trend"].start_live_plot(selected_duts)
