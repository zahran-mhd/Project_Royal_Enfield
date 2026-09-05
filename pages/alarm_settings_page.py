# import tkinter as tk

# from widgets.alarm_settings_widget import (
#     AlarmSettingsWidget
# )


# class AlarmSettingsPage(tk.Frame):

#     def __init__(self, parent):
#         super().__init__(parent, bg="#EEF2F7")

#         # TITLE
#         title = tk.Label(
#             self,
#             text="Alarm Settings",
#             font=("Bookman Antiqua", 18, "bold"),
#               bg="#f5f5f5",
          
#         )

#         title.pack(
           
#             padx=15,
          
#         )

#         AlarmSettingsWidget(
#             self
#         ).pack(
#             fill="x",
#             padx=25
#         )

import tkinter as tk

from widgets.alarm_settings_widget import (
    AlarmSettingsWidget
)


class AlarmSettingsPage(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(
            parent,
            bg="#EEF2F7"
        )

        self.context = context

        # TITLE
        title = tk.Label(
            self,
            text="Alarm Settings",
            font=("Bookman Antiqua", 18, "bold"),
            bg="#f5f5f5",
        )

        title.pack(
            padx=15,
        )

        # ALARM SETTINGS WIDGET
        AlarmSettingsWidget(
            self,
            self.context.alarm_controller
        ).pack(
            fill="x",
            padx=25
        )