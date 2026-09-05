import tkinter as tk

class Header(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#0AA08C", height=80)

        self.pack_propagate(False)

        tk.Label(
            self,
            text="ELMACK LOGO",
            bg="white",
            width=18
        ).pack(side="left", padx=10, pady=10)

        center = tk.Frame(self, bg="#0AA08C")
        center.pack(side="left", expand=True)

        tk.Label(
            center,
            text="APPLICATION DASHBOARD",
            font=("Bookman Antiqua", 18, "bold"),
            fg="white",
            bg="#0AA08C"
        ).pack()

        tk.Label(
            center,
            text="Powered by Elmack Engineering",
            fg="white",
            bg="#0AA08C"
        ).pack()

        tk.Label(
            self,
            text="CUSTOMER LOGO",
            bg="white",
            width=18
        ).pack(side="right", padx=10, pady=10)