import tkinter as tk


# class AlarmPopup(tk.Toplevel):

#     def __init__(self, parent, controller, dut, parameter):
#         super().__init__(parent)

#         self.controller = controller

#         self.title("Alarm")

#         tk.Label(
#             self,
#             text=f"DUT {dut}\n{parameter} Alarm",
#             font=("Segoe UI", 12, "bold")
#         ).pack(padx=20, pady=20)

#         tk.Button(
#             self,
#             text="Resume",
#             command=self.resume
#         ).pack(fill="x", padx=10, pady=5)

#         tk.Button(
#             self,
#             text="Proceed to Next Cycle",
#             command=self.next_cycle
#         ).pack(fill="x", padx=10, pady=5)



class AlarmPopup:

    def __init__(self, parent, controller, alarms):

        self.parent = parent
        self.controller = controller
        self.alarms = alarms

        self.popup = tk.Toplevel(parent)

        self.popup.title("CAN Alarm")
        self.popup.geometry("650x500")

        self.popup.transient(parent)
        self.popup.grab_set()

        # =========================
        # TITLE
        # =========================

        tk.Label(
            self.popup,
            text="CAN ALARM DETECTED",
            font=("Arial", 18, "bold")
        ).pack(pady=15)

        # =========================
        # ALARM LIST
        # =========================

        alarm_frame = tk.Frame(self.popup)
        alarm_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        for alarm in self.alarms:

            dut_id = alarm["dut_id"]
            parameter = alarm["parameter"]

            tk.Label(
                alarm_frame,
                text=f"DUT {dut_id}  →  {parameter}",
                font=("Arial", 12)
            ).pack(
                anchor="w",
                pady=3
            )

        # =========================
        # BUTTONS
        # =========================

        button_frame = tk.Frame(self.popup)
        button_frame.pack(pady=20)

        tk.Button(
            button_frame,
            text="Resume",
            command=self.resume
        ).pack(
            side="left",
            padx=10
        )

        tk.Button(
            button_frame,
            text="Proceed to Next Cycle",
            command=self.next_cycle
        ).pack(
            side="left",
            padx=10
        )

    def resume(self):

        self.controller.alarm_active = False

        self.controller.resume_test()

        self.popup.grab_release()
        self.popup.destroy()

    def next_cycle(self):

        self.controller.alarm_active = False

        self.controller.proceed_to_next_cycle()

        self.popup.grab_release()
        self.popup.destroy()
        # self.controller.next_cycle()
        # self.destroy()
