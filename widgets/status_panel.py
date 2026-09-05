import tkinter as tk


class StatusPanel(tk.LabelFrame):

    def __init__(self, parent, title, items=None, value_width=13):

        bg_color = "#d4edda" if title.lower() == "charging" else "#f8d7da"

        super().__init__(
            parent,
            text=title,
            font=("Bookman Antiqua", 10, "bold"),
            padx=8,
            pady=8,
            bg=bg_color
        )

        if items is None:
            items = [
                ("max", "Max Temp", "-- °C"),
                ("min", "Min Temp", "-- °C"),
            ]

        self.value_labels = {}

        for row, (key, label_text, default_value) in enumerate(items):

            lbl = tk.Label(
                self,
                text=label_text,
                bg=bg_color
            )

            lbl.grid(
                row=row,
                column=0,
                sticky="w",
                pady=3
            )

            value_lbl = tk.Label(
                self,
                text=default_value,
                width=value_width,
                relief="solid",
                bg="white"
            )

            value_lbl.grid(
                row=row,
                column=1,
                padx=5,
                pady=3
            )

            self.value_labels[key] = value_lbl

    # --------------------------------------------------

    def set_active(self, color):

        self.config(bg=color)

        for child in self.winfo_children():

            if isinstance(child, tk.Label):

                if child in self.value_labels.values():
                    # Don't recolor value boxes
                    continue

                child.config(bg=color)

    # --------------------------------------------------

    def set_value(self, key, value):

        if key in self.value_labels:
            self.value_labels[key].config(text=value)

    # Backward compatibility
    def update_value(self, key, value):
        self.set_value(key, value)

    def update_values(self, **kwargs):

        for key, value in kwargs.items():
            self.set_value(key, value)