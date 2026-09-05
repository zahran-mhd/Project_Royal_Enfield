import tkinter as tk
from PIL import Image, ImageTk


class Header(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#0AA08C", height=80)

        self.pack_propagate(False)

        # ======================================================
        # ELMACK LOGO
        # ======================================================

        logo_frame = tk.Frame(
            self,
            bg="#173A8F",
            width=210,
            height=80
        )

        logo_frame.pack(
            side="left",
            padx=5
        )

        logo_frame.pack_propagate(False)

        logo_image = Image.open(
            "assets/elmack.png"
        )

        # Keep original aspect ratio
        logo_image.thumbnail(
            (200, 70),
            Image.Resampling.LANCZOS
        )

        self.elmack_logo = ImageTk.PhotoImage(
            logo_image
        )

        tk.Label(
            logo_frame,
            image=self.elmack_logo,
            bg="#173A8F",
            bd=0
        ).pack(
            expand=True
        )

        # ======================================================
        # CENTER
        # ======================================================

        center = tk.Frame(
            self,
            bg="#173A8F"
        )

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
            font=("Arial", 9),
            fg="white",
            bg="#173A8F"
        ).pack(
            pady=(2, 0)
        )

        # ======================================================
        # CUSTOMER LOGO
        # ======================================================

        customer_frame = tk.Frame(
            self,
            bg="#173A8F",
            width=210,
            height=80
        )

        customer_frame.pack(
            side="right",
            padx=5
        )

        customer_frame.pack_propagate(False)

        customer_image = Image.open(
            "assets/relogo.png"
        )

        # Keep original aspect ratio
        customer_image.thumbnail(
            (200, 70),
            Image.Resampling.LANCZOS
        )

        self.customer_logo = ImageTk.PhotoImage(
            customer_image
        )

        tk.Label(
            customer_frame,
            image=self.customer_logo,
            bg="#173A8F",
            bd=0
        ).pack(
            expand=True
        )