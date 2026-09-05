import tkinter as tk

class CustomRadioButton(tk.Frame):
    def __init__(self, parent, text, variable, value, **kwargs):
        super().__init__(parent, bg="white", **kwargs)

        self.variable = variable
        self.value = value

        self.circle = tk.Label(
            self,
            text="○",
            font=("Bookman Antiqua Symbol", 12),
            bg="white",
            cursor="hand2"
        )
        self.circle.pack(side="left")

        self.label = tk.Label(
            self,
            text=text,
            bg="white",
            cursor="hand2",
            font=("Bookman Antiqua", 10)
        )
        self.label.pack(side="left", padx=(5, 0))

        self.circle.bind("<Button-1>", self.select)
        self.label.bind("<Button-1>", self.select)

        self.variable.trace_add("write", self.update_state)
        self.update_state()

    def select(self, event=None):
        self.variable.set(self.value)

    def update_state(self, *args):
        if self.variable.get() == self.value:
            self.circle.config(text="◉")
        else:
            self.circle.config(text="○")