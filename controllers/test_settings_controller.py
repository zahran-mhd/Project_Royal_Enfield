from tkinter import messagebox

class TestSettingsController():
    def __init__(self,context):
        self.context = context
        self.channel_selection = {}
    
    def on_dut_selected(self,channel_id,channel_name,selected_duts):
         # Store the selected DUTs for this channel
        self.channel_selection[channel_id] = {"channel_name": channel_name,"selected_duts":selected_duts}
        all_selected =[]
        all_channel_map = {}
        # Combine all selected DUTs from every channel
        for data in self.channel_selection.values():
            all_selected.extend(data["selected_duts"])
            all_channel_map[data["channel_name"]] = data["selected_duts"]

         # Save into AppContext
        self.context.selected_duts = all_selected
        self.context.selected_channels = all_channel_map

        print("Selected DUTs :", self.context.selected_duts)
        print("Selected Channels :", self.context.selected_channels)
        
    def start_test(self, card, values):

        # print(values)

        if not self.validate_settings(values):
            return

        card.disable_start_button()

        conn = self.context.database_manager.get_connection()

        self.context.test_repository.save_channel_setting(
            conn,
            values
        )

        self.context.test_controller.start_test(
            values["channel_id"],
            values
        )

        if values['test_type']=="Endurance":
            self.context.live_table.start_channel_refresh(
                values["channel_id"]
                )

        # self.context.can_manager.connect_channel(
        #             channel_id=channel_id,
        #             bitrate=bitrate
        #         )

        page = self.context.app_controller.pages[
            "Endurance-Live Monitoring"
        ]

        page.reset(values["selected_duts"])

        page.start_live_plot(values["selected_duts"])

        # page.start_live_plot(values["selected_duts"])
    
    def get_settings(self):
        
        selected_duts = [  
        dut
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        dut_a = self.dut_list[0]
        dut_b = self.dut_list[1]

        # Use the first selected DUT as dut_id
        dut_id = int(selected_duts[0].replace("DUT", "")) if selected_duts else None
        print(dut_id)
        return {
    "channel_id": self.channel_id,
    "dut_id": dut_id,

    "selected_duts": selected_duts,   # <-- Add this back
     "dut_a_name": dut_a,
    "dut_b_name": dut_b,

    "use_dut_a": 1 if dut_a in selected_duts else 0,
    "use_dut_b": 1 if dut_b in selected_duts else 0,

    "supplier": self.supplier_combo.get(),
    "test_type": self.selected_test.get(),
    "test_name": self.test_name.get(),

    "dut_a_serial_no": self.serial_entries[dut_a].get(),
    "dut_b_serial_no": self.serial_entries[dut_b].get(),
            
            
    "no_of_cycles": self.cycles_entry.get(),
    "interval_seconds": self.time_entry.get()
}
    def validate_settings(self, values):

        if not values["dut_type"]:
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

            if not serial.isdigit():
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

            if not serial.isdigit():
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
        if values['test_type'] == "Endurance":
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

    def get_all_duts(self):
            conn = self.context.database_manager.get_connection()
            return self.context.parameter_repository.get_all_duts(conn)

    # def on_dut_type_selected(self, channel_id, dut_name):

    #     dut = self.context.parameter_repository.get_by_name(dut_name)

    #     bitrate = dut["dut_bit_rate"]

    #     # self.context.can_manager.connect_channel(
    #     #     channel_id=channel_id,
    #     #     bitrate=bitrate
    #     # )

    def on_dut_type_selected(self, channel_id, dut_name):

        self.context.selected_dut_types[channel_id] = dut_name

    # def save_channel_settings(self, settings):

    #     for setting in settings:
    #         self.repository.save_channel_setting(
    #             self.db.conn,
    #             setting
    #         )