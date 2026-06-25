import tkinter as tk
from config_modules.instrument_config import InstrumentConfig
from config_modules.user_config import UserConfig


class ConfigurationPage(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#f5f5f5")
        
        self.context = context

        self.create_header()
        self.create_tabs()

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
            "bg": "#2563eb",
            "fg": "white",
            "activebackground": "#1d4ed8",
            "activeforeground": "white",
            "bd": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 8
        }

        channels = self.context.channel_repository.get_all_channels()
        self.channel_buttons=[]
        for channel in channels:
            channel_id =channel["ChannelID"]
            channel_name = channel["ChannelName"]
            btn = tk.Button(tab_frame,text=f"{channel_name} Configuration",
                            command=lambda cid=channel_id: self.show_instrument(cid),**btn_style)
            
            btn.pack(side="left",padx=10,pady=10)
            
            self.channel_buttons.append(btn)
        self.user_btn = tk.Button(
            tab_frame,
            text="User Management",
            command=self.show_user,
            **btn_style
        )
        self.user_btn.pack(
            side="left",
            padx=10,
            pady=10
        )
      
      

    def show_instrument(self, channel_id):

        # print("Selected Channel:", channel_id)

        self.instrument_page.set_channel(channel_id)

        self.user_page.pack_forget()
        self.instrument_page.pack(fill="both", expand=True)

        # Reset all buttons 
        for btn in self.channel_buttons:
            btn.config(bg="#2563eb")

        self.user_btn.config(bg="#2563eb")

        # Highlight selected button
        self.channel_buttons[channel_id - 1].config(bg="#16a34a")

    def show_user(self):

        self.instrument_page.pack_forget()
        self.user_page.pack(fill="both", expand=True)

        self.user_btn.config(bg="#16a34a")

        for btn in self.channel_buttons:
            btn.config(bg="#2563eb")