import tkinter as tk
class StatusPanel(tk.LabelFrame):
    def __init__(self, parent, title, items=None):
        # Set background color based on title
        bg_color = "#d4edda" if title.lower() == "charging" else "#f8d7da"
        super().__init__(
            parent,
            text=title,
            font=("Segoe UI", 10, "bold"),
            padx=8,
            pady=8,
             bg=bg_color
        )
        
   

        # Default items (Temperature)
        if items is None:
            items = [
                ("max", "Max Temp", "-- °C"),
                ("min", "Min Temp", "-- °C"),
            ]

        self.value_labels = {}

        for row, (key, label_text, default_value) in enumerate(items):
            tk.Label(self, text=label_text).grid(
                row=row, column=0, sticky="w", pady=3
            )

            value_lbl = tk.Label(
                self,
                text=default_value,
                width=10,
                relief="solid",
                bg="white"
            )
            value_lbl.grid(row=row, column=1, padx=5, pady=3)

            self.value_labels[key] = value_lbl
            
    def set_active(self, color):
        self.config(bg=color)

        for child in self.winfo_children():
            try:
                child.config(bg=color)
            except:
                pass
    # ---------------- Update Methods ----------------

    def update_value(self, key, value):
        if key in self.value_labels:
            self.value_labels[key].config(text=value)

    def update_values(self, **kwargs):
        for key, value in kwargs.items():
            self.update_value(key, value)