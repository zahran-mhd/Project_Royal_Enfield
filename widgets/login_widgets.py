import customtkinter as ctk


class LoginWidget(ctk.CTkFrame):

    def __init__(self, parent, login_callback):
        super().__init__(parent)

        self.login_callback = login_callback

        self.grid_columnconfigure(0, weight=1)

        # Title
        ctk.CTkLabel(
            self,
            text="ROYAL ENFIELD",
            font=("Bookman Antiqua", 24, "bold")
        ).pack(pady=(25, 5))

        ctk.CTkLabel(
            self,
            text="",
            font=("Bookman Antiqua", 14)
        ).pack(pady=(0, 20))

        # Username
        self.username_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Username"
        )
        self.username_entry.pack(pady=10)

        # Password
        self.password_entry = ctk.CTkEntry(
            self,
            width=260,
            placeholder_text="Password",
            show="*"
        )
        self.password_entry.pack(pady=10)

        # Login Button
        self.login_btn = ctk.CTkButton(
            self,
            text="Login",
            width=260,
            command=self.on_login
        )
        self.login_btn.pack(pady=25)

        # Enter key
        self.username_entry.bind("<Return>", lambda e: self.on_login())
        self.password_entry.bind("<Return>", lambda e: self.on_login())

        self.username_entry.focus()

    def on_login(self):
        self.login_callback(
            self.username_entry.get().strip(),
            self.password_entry.get()
        )

    def clear_password(self):
        self.password_entry.delete(0, "end")
        self.password_entry.focus()

    def clear_all(self):
        self.username_entry.delete(0, "end")
        self.password_entry.delete(0, "end")