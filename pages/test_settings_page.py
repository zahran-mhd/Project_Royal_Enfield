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
         #Store DUT selections for each channel
        self.channel_selection = {}

        # Shared selected DUT list
        self.context.selected_duts = []
        
        
        self.channel_cards = {}   # Store ChannelCard objects
        
      

        self.create_ui()
      

    def create_ui(self):

        title = tk.Label(
            self,
            text="Test Settings",
            font=("Segoe UI", 18, "bold"),
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
                dut_callback=self.on_dut_selected,
                start_callback=self.start_test
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
            
   
    def on_dut_selected(self, channel_id, channel_name, selected_duts):

        self.channel_selection[channel_id] = selected_duts

        all_selected = []
        all_channel_map = {}

        for ch_id, duts in self.channel_selection.items():

            all_selected.extend(duts)

           
            ch_name = channel_name

            all_channel_map[ch_name] = duts

        self.context.selected_duts = all_selected
        self.context.selected_channels = all_channel_map
        
        dut = self.context.selected_duts[0]
        dut_no = int(dut.replace("DUT", ""))
        channel_id = (dut_no + 1) // 2

        print("Looking for:", channel_id, type(channel_id))
        print("Available keys:", self.channel_cards.keys())
    
    def start_test(self, card):

        values = card.get_settings()

        if not self.validate_settings(values):
            return
         # Disable only after validation succeeds
        card.disable_start_button()

        self.context.test_controller.start_test(
            values["channel_id"],
            values
        )

        page = self.context.app_controller.pages["Endurance-Live Monitoring"]
        page.start_live_plot(values["selected_duts"])
        
    def validate_settings(self, values):

        if not values["supplier"]:
            messagebox.showerror(
                "Validation Error",
                "Please select a DUT Type."
            )
            return False

        if not values["selected_duts"]:
            messagebox.showerror(
                "Validation Error",
                "Please select at least one DUT."
            )
            return False

        if not values["test_type"]:
            messagebox.showerror(
                "Validation Error",
                "Please select a Test Type."
            )
            return False

        if not values["test_name"].strip():
            messagebox.showerror(
                "Validation Error",
                "Please enter Test Name."
            )
            return False

                # Validate DUT A serial number
                # Validate DUT A serial number
        if values["use_dut_a"]:
            serial = values["dut_a_serial_no"].strip()

            if not serial:
                messagebox.showerror(
                    "Validation Error",
                    f"Please enter {values['dut_a_name']} Serial Number."
                )
                return False

            if not serial.isalnum():
                messagebox.showerror(
                    "Validation Error",
                    f"{values['dut_a_name']} Serial Number must contain only letters and numbers."
                )
                return False

            if len(serial) > 10:
                messagebox.showerror(
                    "Validation Error",
                    f"{values['dut_a_name']} Serial Number must not exceed 10 characters."
                )
                return False


        # Validate DUT B serial number
        if values["use_dut_b"]:
            serial = values["dut_b_serial_no"].strip()

            if not serial:
                messagebox.showerror(
                    "Validation Error",
                    f"Please enter {values['dut_b_name']} Serial Number."
                )
                return False

            if not serial.isalnum():
                messagebox.showerror(
                    "Validation Error",
                    f"{values['dut_b_name']} Serial Number must contain only letters and numbers."
                )
                return False

            if len(serial) > 10:
                messagebox.showerror(
                    "Validation Error",
                    f"{values['dut_b_name']} Serial Number must not exceed 10 characters."
                )
                return False
        # Validate cycles
        try:
            cycles = int(values["no_of_cycles"])

            if cycles <= 0:
                messagebox.showerror(
                    "Validation Error",
                    "Cycles must be greater than 0."
                )
                return False

        except (ValueError, TypeError):
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid positive integer for Cycles."
            )
            return False

        # Validate interval
        try:
            interval = float(values["interval_seconds"])
            if interval <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Validation Error",
                "Please enter a valid Interval."
            )
            return False

        return True