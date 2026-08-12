import tkinter as tk

from config_modules.instrument_config import InstrumentConfig
from config_modules.user_config import UserConfig
from controllers.configuration_controller import ConfigurationController


class ConfigurationPage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(
            parent,
            bg="#f5f5f5"
        )

        self.context = context
        self.controller = ConfigurationController(self, context)

        self.channel_buttons = {}

        self.create_header()
        self.create_tabs()

    # --------------------------------------------------
    # Header
    # --------------------------------------------------

    def create_header(self):

        title = tk.Label(
            self,
            text="Configuration",
            font=("Bookman Antiqua", 15, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=15)

    # --------------------------------------------------
    # Tabs
    # --------------------------------------------------

    def create_tabs(self):

        tab_frame = tk.Frame(
            self,
            height=60,
            # relief="solid",
            # bd=1,
            bg="white"
        )
        tab_frame.pack(
            fill="x",
            padx=15,
            pady=(10, 0)
        )

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
        self.instrument_page = InstrumentConfig(
            self.container,
            self.context
        )

        self.user_page = UserConfig(
            self.container,
            self.context
        )

        button_style = {
            "font": ("Bookman Antiqua", 15, "bold"),
            "bg": "#dce3eb",
            "fg": "#2c3e50",
            "bd": 0,
            "cursor": "hand2",
            "padx": 20,
            "pady": 8
        }

        channels = self.context.channel_repository.get_all_channels()

        first_channel = None

        for index, channel in enumerate(channels):

            channel_id = channel["ChannelID"]
            channel_name = channel["ChannelName"]

            if index == 0:
                first_channel = channel_id

            btn = tk.Button(
                tab_frame,
                text=f"{channel_name} Configuration",
                command=lambda cid=channel_id: self.controller.show_instrument(cid),
                **button_style
            )

            btn.pack(
                side="left",
                padx=10,
                pady=10
            )

            self.channel_buttons[channel_id] = btn

        self.user_btn = tk.Button(
            tab_frame,
            text="User Management",
            command=self.controller.show_user,
            **button_style
        )

        self.user_btn.pack(
            side="left",
            padx=10,
            pady=10
        )

        # Show first channel automatically
        if first_channel is not None:
            self.controller.show_instrument(first_channel)

    # --------------------------------------------------
    # Hide Pages
    # --------------------------------------------------

    def hide_pages(self):

        self.instrument_page.pack_forget()
        self.user_page.pack_forget()