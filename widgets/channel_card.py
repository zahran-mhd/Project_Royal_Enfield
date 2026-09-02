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
        dut_type_callback=None,
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
        self.test_settings_controller = context.test_settings_controller

        self.channel_name = channel_name
        self.channel_id = channel_id
        self.dut_callback = dut_callback
        self.start_callback = start_callback
        self.dut_list = dut_list
        self.dut_type_callback = dut_type_callback

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

        rows = self.test_settings_controller.get_all_duts()
        self.dut_map = {row["dut_name"]: row["dut_id"] for row in rows}

        print("DUT DATABASE ROWS:", rows)
        print("DUT MAP:", self.dut_map)

        self.supplier_combo = ctk.CTkComboBox(
            self,
            values=list(self.dut_map.keys()),
            state="readonly",
            width=250,
            command=self.on_dut_type_changed
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

    # def on_start_clicked(self):

    #     if self.start_callback:

    #         self.start_callback(self)

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

    # def get_settings(self):

    #     # selected_duts = [
    #     #     dut
    #     #     for dut, var in self.dut_vars.items()
    #     #     if var.get()
    #     # ]

    #     selected_duts = [
    #         int(dut.replace("DUT", ""))
    #         for dut, var in self.dut_vars.items()
    #         if var.get()
    #     ]

    #     dut_a = self.dut_list[0]      # "DUT1"
    #     dut_b = self.dut_list[1]      # "DUT2"

    #     dut_a_no = int(dut_a.replace("DUT", ""))
    #     dut_b_no = int(dut_b.replace("DUT", ""))

    #     dut_id = selected_duts[0] if selected_duts else None

    #     return {
    #         "channel_id": self.channel_id,
    #         "dut_id": dut_id,
    #         "selected_duts": selected_duts,

    #         "dut_a_name": dut_a,
    #         "dut_b_name": dut_b,

    #         "use_dut_a": 1 if dut_a_no in selected_duts else 0,
    #         "use_dut_b": 1 if dut_b_no in selected_duts else 0,

    #         "dut_type": self.supplier_combo.get(),

    #         "test_type": self.selected_test.get(),

    #         "test_name": self.test_name.get(),

    #         "dut_a_serial_no": (
    #             self.serial_entries[dut_a].get()
    #         ),

    #         "dut_b_serial_no": (
    #             self.serial_entries[dut_b].get()
    #         ),

    #         "no_of_cycles": (
    #             self.cycles_entry.get()
    #         ),

    #         "interval_seconds": (
    #             self.time_entry.get()
    #         )
    #     }

    # def on_dut_type_changed(self, dut_type):

    #     dut_id = self.dut_map[dut_type]

    #     if self.dut_callback:
    #         self.dut_callback(
    #             channel_id=self.channel_id,
    #             channel_name=self.channel_name,
    #             dut_id=dut_id,
    #             dut_type=dut_type
    #         )

    # def get_settings(self):

    # # =====================================================
    # # SELECTED DUT NAMES
    # # =====================================================

    #     selected_duts = [
    #         dut
    #         for dut, var in self.dut_vars.items()
    #         if var.get()
    #     ]

    #     print("Selected DUT names:", selected_duts)

    #     # =====================================================
    #     # SELECTED DATABASE DUT IDs
    #     # =====================================================

    #     selected_dut_ids = [
    #         self.dut_map[dut]
    #         for dut in selected_duts
    #         if dut in self.dut_map
    #     ]

    #     print("Selected DUT DB IDs:", selected_dut_ids)

    #     # =====================================================
    #     # DUT A / DUT B
    #     # =====================================================

    #     dut_a = self.dut_list[0] if len(self.dut_list) > 0 else None
    #     dut_b = self.dut_list[1] if len(self.dut_list) > 1 else None

    #     # =====================================================
    #     # DUT A INFORMATION
    #     # =====================================================

    #     dut_a_id = (
    #         self.dut_map.get(dut_a)
    #         if dut_a
    #         else None
    #     )

    #     print("DUT_A_id: ",dut_a_id)

    #     use_dut_a = (
    #         1
    #         if dut_a in selected_duts
    #         else 0
    #     )

    #     # =====================================================
    #     # DUT B INFORMATION
    #     # =====================================================

    #     dut_b_id = (
    #         self.dut_map.get(dut_b)
    #         if dut_b
    #         else None
    #     )

    #     print("DUT_B_id: ",dut_b_id)

    #     use_dut_b = (
    #         1
    #         if dut_b in selected_duts
    #         else 0
    #     )

    #     # =====================================================
    #     # PRIMARY DUT ID
    #     # =====================================================

    #     dut_id = (
    #         selected_dut_ids[0]
    #         if selected_dut_ids
    #         else None
    #     )

    #     print("Primary DUT DB ID:", dut_id)

    #     # =====================================================
    #     # SERIAL NUMBERS
    #     # =====================================================

    #     dut_a_serial_no = ""

    #     if dut_a and dut_a in self.serial_entries:
    #         dut_a_serial_no = (
    #             self.serial_entries[dut_a].get().strip()
    #         )

    #     dut_b_serial_no = ""

    #     if dut_b and dut_b in self.serial_entries:
    #         dut_b_serial_no = (
    #             self.serial_entries[dut_b].get().strip()
    #         )

    #     # =====================================================
    #     # RETURN
    #     # =====================================================

    #     return {

    #         "channel_id": self.channel_id,

    #         # Actual database DUT ID
    #         "dut_id": dut_id,

    #         # All selected database IDs
    #         "selected_dut_ids": selected_dut_ids,

    #         # Selected DUT names
    #         "selected_duts": selected_duts,

    #         # ---------------------------------------------
    #         # DUT A
    #         # ---------------------------------------------

    #         "dut_a_name": dut_a,
    #         "dut_a_id": dut_a_id,
    #         "use_dut_a": use_dut_a,
    #         "dut_a_serial_no": dut_a_serial_no,

    #         # ---------------------------------------------
    #         # DUT B
    #         # ---------------------------------------------

    #         "dut_b_name": dut_b,
    #         "dut_b_id": dut_b_id,
    #         "use_dut_b": use_dut_b,
    #         "dut_b_serial_no": dut_b_serial_no,

    #         # ---------------------------------------------
    #         # TEST
    #         # ---------------------------------------------

    #         "dut_type": self.supplier_combo.get(),

    #         "test_type": self.selected_test.get(),

    #         "test_name": self.test_name.get().strip(),

    #         # ---------------------------------------------
    #         # ENDURANCE
    #         # ---------------------------------------------

    #         "no_of_cycles": self.cycles_entry.get(),

    #         "interval_seconds": self.time_entry.get()
    #     }
    

    def get_settings(self):

        # =====================================================
        # SELECTED PHYSICAL DUTS
        # =====================================================

        selected_duts = [
            dut
            # int(dut.replace("DUT", ""))
            for dut, var in self.dut_vars.items()
            if var.get()
        ]

        print("Selected DUT names:", selected_duts)

        # =====================================================
        # DUT TYPE
        # =====================================================

        dut_type = self.supplier_combo.get()

        # =====================================================
        # DATABASE DUT ID
        # =====================================================

        dut_id = self.dut_map.get(dut_type)

        print("Selected DUT Type:", dut_type)
        print("Selected DUT DB ID:", dut_id)

        # =====================================================
        # DUT A / DUT B
        # =====================================================

        dut_a = (
            self.dut_list[0]
            if len(self.dut_list) > 0
            else None
        )

        dut_b = (
            self.dut_list[1]
            if len(self.dut_list) > 1
            else None
        )

        # =====================================================
        # DUT A
        # =====================================================

        use_dut_a = (
            1
            if dut_a in selected_duts
            else 0
        )

        # =====================================================
        # DUT B
        # =====================================================

        use_dut_b = (
            1
            if dut_b in selected_duts
            else 0
        )

        # =====================================================
        # SERIAL NUMBERS
        # =====================================================

        dut_a_serial_no = ""

        if dut_a and dut_a in self.serial_entries:
            dut_a_serial_no = (
                self.serial_entries[dut_a]
                .get()
                .strip()
            )

        dut_b_serial_no = ""

        if dut_b and dut_b in self.serial_entries:
            dut_b_serial_no = (
                self.serial_entries[dut_b]
                .get()
                .strip()
            )

        # =====================================================
        # RETURN
        # =====================================================

        return {

            "channel_id": self.channel_id,

            # Database DUT type ID
            "dut_id": dut_id,

            # Physical DUTs selected on this channel
            "selected_duts": selected_duts,

            # Physical DUT names
            "dut_a_name": dut_a,
            "dut_b_name": dut_b,

            "use_dut_a": use_dut_a,
            "use_dut_b": use_dut_b,

            # DUT type
            "dut_type": dut_type,

            "test_type": self.selected_test.get(),

            "test_name": (
                self.test_name.get().strip()
            ),

            "dut_a_serial_no": dut_a_serial_no,

            "dut_b_serial_no": dut_b_serial_no,

            "no_of_cycles": (
                self.cycles_entry.get()
            ),

            "interval_seconds": (
                self.time_entry.get()
            )
        }
    
    def on_dut_type_changed(self, dut_name):

        if self.dut_type_callback:
            self.dut_type_callback(
                self.channel_id,
                dut_name
            )

    # def get_data(self):
    #     return {
    #         "channel_id": self.channel_id,
    #         "dut_id": self.selected_dut_id,      # Set when DUT is selected
    #         "use_dut_a": 1 if self.use_dut_a_var.get() else 0,
    #         "use_dut_b": 1 if self.use_dut_b_var.get() else 0,
    #         "test_type": self.test_type_combo.get(),
    #         "test_name": self.test_name_entry.get().strip(),
    #         "dut_a_serial_no": self.dut_a_serial_entry.get().strip(),
    #         "dut_b_serial_no": self.dut_b_serial_entry.get().strip(),
    #         "no_of_cycles": int(self.cycles_entry.get() or 0),
    #         "interval_seconds": int(self.interval_entry.get() or 0)
    #     }

    # def on_start_clicked(self):

    #     if self.start_callback:
    #         self.start_callback(self.get_settings())

    def on_start_clicked(self):

        if self.start_callback:
            self.start_callback(
                self,
                self.get_settings()
            )