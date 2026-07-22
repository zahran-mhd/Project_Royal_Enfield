import tkinter as tk
from config_modules.instrument_config import InstrumentConfig
from config_modules.user_config import UserConfig
from controllers.configuration_controller import ConfigurationController

class ConfigurationPage(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#f5f5f5")
        self.context = context
        self.controller = ConfigurationController(self, context)

        self.create_header()
        self.create_tabs()
        
        # self.channel_buttons = {}

    def create_header(self):
        tk.Label(
            self,
            text="Configuration",
            font=("Segoe UI", 18, "bold"),
            bg="#f5f5f5"
        ).pack(anchor="w", padx=30, pady=20)

    def create_tabs(self):

    # Header Tab Bar
        tab_frame = tk.Frame(
            self,
            # bg="#ffffff", 
            height=60,
            # bd=1,
            relief="solid"
        )
        tab_frame.pack(fill="x", padx=15, pady=(10, 0))

        # Content Area
        self.container = tk.Frame(
            self,
            bg="#eef2f7"
        )
        self.container.pack(
            fill="both",
            expand=True,
            padx=15,
            pady=15
        )

        # Pages
        self.instrument_page = InstrumentConfig(self.container,self.context)
        self.user_page = UserConfig(
    self.container,
    self.context
)

        self.instrument_page.pack(fill="both", expand=True)

        # Style
        btn_style = {
            "font": ("Segoe UI", 10, "bold"),
          
            "bg":"#dce3eb",
  
             "fg":"#2c3e50",
            "activebackground": "#2c3e50",
            "activeforeground": "#dce3eb",
            "bd": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 8
        }

        channels = self.context.channel_repository.get_all_channels()
        self.channel_buttons={}
        for channel in channels:
            channel_id =channel["ChannelID"]
            channel_name = channel["ChannelName"]
            btn = tk.Button(tab_frame,text=f"{channel_name} Configuration",
                            command=lambda cid=channel_id: self.controller.show_instrument(cid),**btn_style)
            
            btn.pack(side="left",padx=10,pady=10)
            
            self.channel_buttons[channel_id] = btn
        self.user_btn = tk.Button(
            tab_frame,
            text="User Management",
            command=self.controller.show_user,
            **btn_style
        )
        self.user_btn.pack(
            side="left",
            padx=10,
            pady=10
        )
      
    def hide_pages(self):
        self.instrument_page.pack_forget()
        self.user_page.pack_forget()
