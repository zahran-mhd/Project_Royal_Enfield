import tkinter as tk
from datetime import datetime

class SubHeader(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#F2F2F2", height=60)
        self.context = context
        self.pack_propagate(False)

        self.user_lbl = tk.Label(
            self,
            text="👤 Guest",
            width=20,
            relief="groove",
            font=("Arial", 11, "bold")
        )
        self.user_lbl.pack(side="left", padx=15, pady=10)

        self.status_lbl = tk.Label(
            self,
            text="STATUS",
            width=20,
            relief="groove",
            font=("Arial", 11, "bold")
        )
        self.status_lbl.pack(side="left", expand=True)

        self.clock_lbl = tk.Label(
            self,
            width=22,
            relief="groove",
            font=("Arial", 11, "bold")
        )
        self.clock_lbl.pack(side="right", padx=15)

        self.update_clock()
        self.update_user()
        print("update_user called")
    def update_clock(self):
        self.clock_lbl.config(
            text=datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        )
        self.after(1000, self.update_clock)
        
    def update_user(self):
        username = self.context.app_state.current_user
        role = self.context.app_state.current_role

        if username:
            self.user_lbl.config(
                text=f"👤 {username} ({role})"
            )
        else:
            self.user_lbl.config(text="👤 Guest")