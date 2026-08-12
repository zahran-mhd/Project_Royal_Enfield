import tkinter as tk
from datetime import datetime


class SubHeader(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(
            parent,
            bg="white",
            height=55
        )

        self.context = context
        self.pack_propagate(False)

        # Bottom Border
        tk.Frame(
            self,
            bg="#D8DCE3",
            height=1
        ).pack(side="bottom", fill="x")

        # Main Body
        body = tk.Frame(
            self,
            bg="white"
        )
        body.pack(
            fill="both",
            expand=True,
            padx=20
        )

        # Three Equal Columns
        body.grid_columnconfigure(0, weight=1, uniform="column")
        body.grid_columnconfigure(1, weight=1, uniform="column")
        body.grid_columnconfigure(2, weight=1, uniform="column")

        # --------------------------------------------------
        # LEFT : USER
        # --------------------------------------------------

        self.user_lbl = tk.Label(
            body,
            text="Not Logged In",
            bg="white",
            fg="#1F2937",
            font=("Segoe UI", 11, "bold"),
            anchor="w"
        )
        self.user_lbl.grid(
            row=0,
            column=0,
            sticky="ew"
        )

        # --------------------------------------------------
        # CENTER : STATUS
        # --------------------------------------------------

        self.status_lbl = tk.Label(
            body,
            text="Status",
            bg="white",
            fg="#374151",
            font=("Segoe UI", 11),
            anchor="center"
        )
        self.status_lbl.grid(
            row=0,
            column=1,
            sticky="ew"
        )

        # --------------------------------------------------
        # RIGHT : TIME
        # --------------------------------------------------

        self.clock_lbl = tk.Label(
            body,
            text="",
            bg="white",
            fg="#374151",
            font=("Consolas", 11),
            anchor="e"
        )
        self.clock_lbl.grid(
            row=0,
            column=2,
            sticky="ew"
        )

        self.update_user()
        self.update_clock()

    # ------------------------------------------------------
    # CLOCK
    # ------------------------------------------------------

    def update_clock(self):

        self.clock_lbl.config(
            text=datetime.now().strftime("%I:%M:%S %p")
        )

        self.after(
            1000,
            self.update_clock
        )

    # ------------------------------------------------------
    # USER / STATUS
    # ------------------------------------------------------

    def update_user(self):

        if self.context.app_state.logged_in:

            username = self.context.app_state.current_user
            role = self.context.app_state.current_role

            self.user_lbl.config(
                text=f"{username} ({role})"
            )

           

        else:

            self.user_lbl.config(
                text="Not Logged In"
            )

          

        self.after(
            1000,
            self.update_user
        )