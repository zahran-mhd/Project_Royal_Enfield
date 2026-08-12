import customtkinter as ctk


class ChannelCard(ctk.CTkFrame):

    def __init__(
        self,
        context,
        parent,
        title,
        channel_name,
        dut_list,
        channel_id=None,
        dut_callback=None,
        start_callback=None
    ):

        super().__init__(
            parent,
            fg_color="white",
            corner_radius=8,
            border_width=1,
            border_color="#d9d9d9"
        )

        self.context = context
        self.test_controller = context.test_controller

        self.channel_name = channel_name
        self.channel_id = channel_id
        self.dut_callback = dut_callback
        self.start_callback = start_callback
        self.dut_list = dut_list

        self.create_widgets()

    # =====================================================
    # CREATE UI
    # =====================================================

    def create_widgets(self):

        duts = self.dut_list
        row = 0

        # =================================================
        # TITLE
        # =================================================

        self.title_label = ctk.CTkLabel(
            self,
            text=self.channel_name,
            font=("Bookman Antiqua", 15, "bold"),
            text_color="#1f2937"
        )

        self.title_label.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="w",
            padx=15,
            pady=(15, 10)
        )

        row += 1

        # =================================================
        # DUT TYPE
        # =================================================

        ctk.CTkLabel(
            self,
            text="Type of DUT",
             font=("Bookman Antiqua", 15, "bold"),
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        self.supplier_combo = ctk.CTkComboBox(
            self,
            values=[
                "Supplier A",
                "Supplier B",
                "Supplier C"
            ],
            state="readonly",
            width=250
        )

        self.supplier_combo.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 15),
            pady=5
        )

        row += 1

        # =================================================
        # DUT SELECTION
        # =================================================

        ctk.CTkLabel(
            self,
            text="Select DUT",
             font=("Bookman Antiqua", 15, "bold"),
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            padx=15,
            pady=5
        )

        dut_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )
        

        dut_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="w",
            padx=(10, 15)
        )

        self.dut_vars = {}

        for dut in duts:

            var = ctk.BooleanVar(value=False)

            self.dut_vars[dut] = var

            ctk.CTkCheckBox(
                dut_frame,
                text=dut,
                variable=var,
                command=self.on_checkbox_changed,
                cursor="hand2"
            ).pack(
                side="left",
                padx=10
            )

        row += 1

        # =================================================
        # SEPARATOR
        # =================================================

        self.create_separator(row)

        row += 1

        # =================================================
        # TEST TYPE
        # =================================================

        ctk.CTkLabel(
            self,
            text="Test Type",
             font=("Bookman Antiqua", 15, "bold"),
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            padx=15,
            pady=5
        )

        test_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        test_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="w",
            padx=(10, 15)
        )

        self.selected_test = ctk.StringVar(value="")

        tests = [
            "Endurance",
            "Line Regulation",
            "Load Regulation"
        ]

        for test in tests:

            ctk.CTkRadioButton(
                test_frame,
                text=test,
                variable=self.selected_test,
                value=test,
                cursor="hand2"
            ).pack(
                anchor="w",
                pady=2
            )

        row += 1

        # =================================================
        # SEPARATOR
        # =================================================

        self.create_separator(row)

        row += 1

        # =================================================
        # TEST NAME
        # =================================================

        ctk.CTkLabel(
            self,
            text="Test Name",
             font=("Bookman Antiqua", 15, "bold"),
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        self.test_name = ctk.CTkEntry(
            self,
            placeholder_text="Enter test name"
        )

        self.test_name.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 15),
            pady=5
        )

        row += 1

        # =================================================
        # SERIAL NUMBERS
        # =================================================

        ctk.CTkLabel(
            self,
             font=("Bookman Antiqua", 15, "bold"),
            text="Serial Numbers",
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="nw",
            padx=15,
            pady=5
        )

        serial_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        serial_frame.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 15),
            pady=5
        )

        self.serial_entries = {}

        for col, dut in enumerate(duts):

            ctk.CTkLabel(
                serial_frame,
                text=f"{dut} SN",
                font=("Segoe UI", 10),
                text_color="#4b5563"
            ).grid(
                row=0,
                column=col,
                sticky="w",
                padx=5
            )

            entry = ctk.CTkEntry(
                serial_frame,
                placeholder_text=f"{dut} serial number"
            )

            entry.grid(
                row=1,
                column=col,
                sticky="ew",
                padx=5,
                pady=(3, 0)
            )

            self.serial_entries[dut] = entry

            serial_frame.columnconfigure(
                col,
                weight=1
            )

        row += 1

        # =================================================
        # CYCLES
        # =================================================

        ctk.CTkLabel(
            self,
             font=("Bookman Antiqua", 15, "bold"),
            text="Cycles",
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        self.cycles_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter number of cycles"
        )

        self.cycles_entry.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 15),
            pady=5
        )

        row += 1

        # =================================================
        # TIME INTERVAL
        # =================================================

        ctk.CTkLabel(
            self,
            text="Interval (sec)",
             font=("Bookman Antiqua", 15, "bold"),
            text_color="#374151"
        ).grid(
            row=row,
            column=0,
            sticky="w",
            padx=15,
            pady=5
        )

        self.time_entry = ctk.CTkEntry(
            self,
            placeholder_text="Enter interval in seconds"
        )

        self.time_entry.grid(
            row=row,
            column=1,
            columnspan=2,
            sticky="ew",
            padx=(10, 15),
            pady=5
        )

        row += 1

        # =================================================
        # START BUTTON
        # =================================================

        self.start_btn = ctk.CTkButton(
            self,
            text="Start Test",
             font=("Segoe UI", 15, "bold"),
            fg_color="#16a34a",
            hover_color="#15803d",
            cursor="hand2",
            command=self.on_start_clicked
        )

        self.start_btn.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=15,
            pady=(15, 15)
        )

        # =================================================
        # GRID CONFIGURATION
        # =================================================

        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)

    # =====================================================
    # SEPARATOR
    # =====================================================

    def create_separator(self, row):

        separator = ctk.CTkFrame(
            self,
            height=1,
            fg_color="#d1d5db"
        )

        separator.grid(
            row=row,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=15,
            pady=10
        )

    # =====================================================
    # DUT CHECKBOX CALLBACK
    # =====================================================

    def on_checkbox_changed(self):

        selected = [
            dut
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        print("ChannelCard:", selected)

        if self.dut_callback:

            self.dut_callback(
                self.channel_id,
                self.channel_name,
                selected
            )

    # =====================================================
    # START TEST
    # =====================================================

    def on_start_clicked(self):

        if self.start_callback:

            self.start_callback(self)

    # =====================================================
    # DISABLE START BUTTON
    # =====================================================

    def disable_start_button(self):

        self.start_btn.configure(
            state="disabled"
        )

    # =====================================================
    # ENABLE START BUTTON
    # =====================================================

    def enable_start_button(self):

        self.start_btn.configure(
            state="normal"
        )
    # def reset_selection(self):

    #     # Reset DUT checkboxes
    #     for var in self.dut_vars.values():
    #         var.set(False)

    #     # Reset supplier
    #     self.supplier_combo.set("")

    #     # Reset test type
    #     self.selected_test.set("")

    #     # Clear test name
    #     self.test_name.delete(0, "end")

    #     # Clear serial numbers
    #     for entry in self.serial_entries.values():
    #         entry.delete(0, "end")

    #     # Clear cycles
    #     self.cycles_entry.delete(0, "end")

    #     # Clear interval
    #     self.time_entry.delete(0, "end")

    #     # Enable start button again
    #     self.enable_start_button()
    # =====================================================
    # GET SETTINGS
    # =====================================================

    def get_settings(self):

        selected_duts = [
            dut
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        dut_a = self.dut_list[0]
        dut_b = self.dut_list[1]

        # First selected DUT
        dut_id = (
            int(selected_duts[0].replace("DUT", ""))
            if selected_duts
            else None
        )

        print(dut_id)

        return {

            "channel_id": self.channel_id,

            "dut_id": dut_id,

            "selected_duts": selected_duts,

            "dut_a_name": dut_a,

            "dut_b_name": dut_b,

            "use_dut_a": (
                1
                if dut_a in selected_duts
                else 0
            ),

            "use_dut_b": (
                1
                if dut_b in selected_duts
                else 0
            ),

            "supplier": self.supplier_combo.get(),

            "test_type": self.selected_test.get(),

            "test_name": self.test_name.get(),

            "dut_a_serial_no": (
                self.serial_entries[dut_a].get()
            ),

            "dut_b_serial_no": (
                self.serial_entries[dut_b].get()
            ),

            "no_of_cycles": (
                self.cycles_entry.get()
            ),

            "interval_seconds": (
                self.time_entry.get()
            )
        }