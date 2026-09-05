# import tkinter as tk
# from tkinter import ttk


# class AlarmSettingsWidget(tk.Frame):

#     def __init__(self, parent):
#         super().__init__(parent, bg="#EEF2F7")

#         # TABLE CARD
#         table_frame = tk.Frame(
#             self,
#             bg="white"
#         )
#         table_frame.pack(
#             fill="x",
#             pady=(0, 10)
#         )

#         # Column Sizes
#         table_frame.grid_columnconfigure(0, weight=1, minsize=100)
#         table_frame.grid_columnconfigure(1, weight=3, minsize=320)
#         # table_frame.grid_columnconfigure(2, weight=2, minsize=180)
#         # table_frame.grid_columnconfigure(3, weight=2, minsize=180)
#         # table_frame.grid_columnconfigure(4, weight=2, minsize=180)

#         # HEADERS
#         headers = ["Enable", "Name"]

#         #  # HEADERS
#         #         headers = ["Enable", "Name", "Min", "Max", "Type"]

#         for col, header in enumerate(headers):
#             tk.Label(
#                 table_frame,
#                 text=header,
#                 font=("Bookman Antiqua", 18, "bold"),
#                 bg="#1976F3",
#                 fg="white",
#                 pady=10
#             ).grid(
#                 row=0,
#                 column=col,
#                 sticky="nsew",
#                 padx=1,
#                 pady=(0, 2)
#             )

#         alarms = [
#             "Input Under Voltage",
#             "Output Under Voltage",
#             "Input Over Voltage",
#             "Output Over Voltage",
#             "OBC Over Current Protection",
#             "OBC Short Current Protection",
#             "HP DCDC Over Current Protection",
#             "HP DCDC Short Current Protection",
#             "CAN Communication Failure"
#         ]

#         self.alarm_rows = []

#         # DATA ROWS
#         for row, alarm_name in enumerate(alarms, start=1):

#             enable_var = tk.BooleanVar()

#             checkbox = tk.Checkbutton(
#                 table_frame,
#                 variable=enable_var,
#                 bg="white",
#                 activebackground="white",
#                 bd=0,
#                 highlightthickness=0,
#                 cursor="hand2"
#             )

#             checkbox.grid(
#                 row=row,
#                 column=0,
#                 padx=20,
#                 pady=8
#             )

#             tk.Label(
#                 table_frame,
#                 text=alarm_name,
#                 bg="white",
#                 fg="#1E3A5F",
#                 font=("Bookman Antiqua", 16),
#                 anchor="w"
#             ).grid(
#                 row=row,
#                 column=1,
#                 sticky="w",
#                 padx=(20, 10),
#                 pady=8
#             )

#             # min_entry = ttk.Entry(
#             #     table_frame,
#             #     font=("Bookman Antiqua", 10)
#             # )

#             # min_entry.grid(
#             #     row=row,
#             #     column=2,
#             #     sticky="ew",
#             #     padx=15,
#             #     pady=8,
#             #     ipady=2
#             # )

#             # max_entry = ttk.Entry(
#             #     table_frame,
#             #     font=("Bookman Antiqua", 10)
#             # )

#             # max_entry.grid(
#             #     row=row,
#             #     column=3,
#             #     sticky="ew",
#             #     padx=15,
#             #     pady=8,
#             #     ipady=2
#             # )

#             # type_combo = ttk.Combobox(
#             #     table_frame,
#             #     values=["Warning", "Critical", "Fault"],
#             #     state="readonly",
#             #     font=("Bookman Antiqua", 10)
#             # )

#             # type_combo.set("Warning")

#             # type_combo.grid(
#             #     row=row,
#             #     column=4,
#             #     sticky="ew",
#             #     padx=15,
#             #     pady=8
#             # )

#             self.alarm_rows.append({
#                 "enable": enable_var,
#                 "name": alarm_name
#                 # "min": min_entry,
#                 # "max": max_entry,
#                 # "type": type_combo
#             })

#         # SAVE BUTTON
#         button_frame = tk.Frame(
#             self,
#             bg="#EEF2F7"
#         )

#         button_frame.pack(
#             fill="x",
#             pady=(5, 15)
#         )

#         save_btn = tk.Button(
#             button_frame,
#             text="Save Settings",
#             font=("Bookman Antiqua", 11, "bold"),
#             bg="#3567E5",
#             fg="white",
#             activebackground="#2F5DD0",
#             activeforeground="white",
#             bd=0,
#             cursor="hand2",
#             width=18,
#             height=1,
#             command=self.save_settings
#         )

#         save_btn.pack()

#     def save_settings(self):
#         pass


import tkinter as tk
from tkinter import ttk


class AlarmSettingsWidget(tk.Frame):

    def __init__(self, parent, alarm_controller):

        super().__init__(
            parent,
            bg="#EEF2F7"
        )


         # IMPORTANT: store controller first
        self.alarm_controller = alarm_controller

        self.alarm_rows = []

        # ======================================================
        # TABLE CARD
        # ======================================================

        table_frame = tk.Frame(
            self,
            bg="white"
        )

        table_frame.pack(
            fill="x",
            pady=(0, 10)
        )

        # ======================================================
        # COLUMN SIZES
        # ======================================================

        table_frame.grid_columnconfigure(
            0,
            weight=1,
            minsize=100
        )

        table_frame.grid_columnconfigure(
            1,
            weight=3,
            minsize=320
        )

        # ======================================================
        # HEADERS
        # ======================================================

        headers = [
            "Enable",
            "Name"
        ]

        for col, header in enumerate(headers):

            tk.Label(
                table_frame,
                text=header,
                font=("Bookman Antiqua", 18, "bold"),
                bg="#1976F3",
                fg="white",
                pady=10
            ).grid(
                row=0,
                column=col,
                sticky="nsew",
                padx=1,
                pady=(0, 2)
            )

        # ======================================================
        # LOAD ALARMS FROM DATABASE
        # ======================================================

        alarms = self.alarm_controller.get_alarm_settings()

        # ======================================================
        # DATA ROWS
        # ======================================================

        for row, alarm in enumerate(alarms, start=1):

            enable_var = tk.BooleanVar(
                value=alarm["is_enabled"]
            )

            checkbox = tk.Checkbutton(
                table_frame,
                variable=enable_var,
                bg="white",
                activebackground="white",
                bd=0,
                highlightthickness=0,
                cursor="hand2"
            )

            checkbox.grid(
                row=row,
                column=0,
                padx=20,
                pady=8
            )

            tk.Label(
                table_frame,
                text=alarm["alarm_name"],
                bg="white",
                fg="#1E3A5F",
                font=("Bookman Antiqua", 16),
                anchor="w"
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=(20, 10),
                pady=8
            )

            # Store database ID + Tkinter variable
            self.alarm_rows.append(
                {
                    "alarm_id": alarm["alarm_id"],
                    "name": alarm["alarm_name"],
                    "enable": enable_var
                }
            )

        # ======================================================
        # SAVE BUTTON
        # ======================================================

        button_frame = tk.Frame(
            self,
            bg="#EEF2F7"
        )

        button_frame.pack(
            fill="x",
            pady=(5, 15)
        )

        save_btn = tk.Button(
            button_frame,
            text="Save Settings",
            font=("Bookman Antiqua", 11, "bold"),
            bg="#3567E5",
            fg="white",
            activebackground="#2F5DD0",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=18,
            height=1,
            command=self.save_settings
        )

        save_btn.pack()

    # ==========================================================
    # SAVE SETTINGS
    # ==========================================================

    def save_settings(self):

        alarm_settings = []

        for alarm in self.alarm_rows:

            alarm_settings.append(
                {
                    "alarm_id": alarm["alarm_id"],
                    "is_enabled": alarm["enable"].get()
                }
            )

        self.alarm_controller.save_alarm_settings(
            alarm_settings
        )

        print("Alarm settings saved successfully")

    # ==========================================================
    # RELOAD FROM DATABASE
    # ==========================================================

    def load_alarm_settings(self):

        alarms = self.alarm_repository.get_all_alarms()

        for alarm in alarms:

            for row in self.alarm_rows:

                if row["alarm_id"] == alarm["alarm_id"]:

                    row["enable"].set(
                        alarm["is_enabled"]
                    )

                    break