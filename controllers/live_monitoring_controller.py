class LiveMonitoringController:
    def __init__(self,view,context):
        self.view = view
        self.context =context
    def show_tab(self,tab_name):
        for frame in self.view.tabs.values():
            frame.pack_forget()
            
        selected_tab = self.view.tabs.get(tab_name)
        
        if selected_tab:
            selected_tab.pack(fill='both',expand=True)
            
    def start_live_plot(self,selected_duts):
        self.view.tabs_widget.select_tab("trend")
        trend_frame = self.view.tabs.get("trend")
        if trend_frame:
            trend_frame.start_live_plot(selected_duts)