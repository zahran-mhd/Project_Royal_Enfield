import tkinter as tk


class LiveTabs(tk.Frame):

    def __init__(self, parent, callback):
        super().__init__(parent, bg="#eef2f7")

        self.callback = callback
        self.buttons = {}
        self.active_tab = None

        # Container for tabs
        self.tab_frame = tk.Frame(self, bg="#eef2f7")
        self.tab_frame.pack(fill="x", padx=10, pady=5)

        tabs = [
            ("Efficiency Trend", "trend"),
            ("Live Table", "table"),
            ("Live Temperature", "temperature")
        ]

        for text, key in tabs:

            btn = tk.Label(
                self.tab_frame,
                text=text,
                font=("Bookman Antiqua", 15, "bold"),
                bg="#dce3eb",
                fg="#2c3e50",
                padx=20,
                pady=10,
                cursor="hand2"
            )

            btn.pack(side="left", padx=(0, 8))

            btn.bind(
                "<Button-1>",
                lambda e, k=key: self.select_tab(k)
            )

            btn.bind(
                "<Enter>",
                lambda e, b=btn: self.on_hover(b)
            )

            btn.bind(
                "<Leave>",
                lambda e, b=btn, k=key: self.on_leave(b, k)
            )

            self.buttons[key] = btn

        # self.select_tab("trend")

    def select_tab(self, tab_name):

        self.active_tab = tab_name

        for key, btn in self.buttons.items():

            if key == tab_name:
                btn.config(
                    bg="#1f6aa5",
                    font=("Bookman Antiqua", 15, "bold"),
                    fg="white",
                    relief="solid",
                    bd=0
                )
            else:
                btn.config(
                    bg="#dce3eb",
                    fg="#2c3e50"
                )

        self.callback(tab_name)

    def on_hover(self, button):

        if button != self.buttons.get(self.active_tab):
            button.config(bg="#cfd8e3")

    def on_leave(self, button, key):

        if key != self.active_tab:
            button.config(bg="#dce3eb")