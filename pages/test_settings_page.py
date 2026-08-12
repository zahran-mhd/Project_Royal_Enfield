import tkinter as tk

from widgets.channel_card import ChannelCard
from tkinter import messagebox

class TestSettingsPage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(
            parent,
            bg="#f5f5f5"
        )

        self.context = context
        
        self.channel_cards = {}   # Store ChannelCard objects
        
      

        self.create_ui()
      

    def create_ui(self):

        title = tk.Label(
            self,
            text="Test Settings",
            font=("Segoe UI", 15, "bold"),
            bg="#f5f5f5"
        )
        title.pack(pady=15)

        content = tk.Frame(
            self,
            bg="#f5f5f5"
        )
        content.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        channels = self.context.channel_repository.get_all_channels()

        for col, channel in enumerate(channels):

            channel_id = channel["ChannelID"]
            channel_name = channel["ChannelName"]

            card = ChannelCard(self.context,
                content,
                title=channel_name,
                channel_name=channel_name,
                dut_list = [
    f"DUT{2 * int(channel_id) - 1}",
    f"DUT{2 * int(channel_id)}"
],
                channel_id=channel_id,
                dut_callback=self.context.test_settings_controller.on_dut_selected,
                 start_callback=self.context.test_settings_controller.start_test
            )
            self.channel_cards[channel_name] = card    # <-- Save reference
            card.grid(
                row=0,
                column=col,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            content.columnconfigure(col, weight=1)
   