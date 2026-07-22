import customtkinter as ctk
from tkinter import messagebox

from widgets.login_widgets import LoginWidget


class LoginDialog(ctk.CTkToplevel):

    def __init__(self, parent, context):
        super().__init__(parent)

        self.context = context

        self.title("Login")
        self.geometry("420x320")
        self.resizable(False, False)
        self.update_idletasks()
        width = 420
        height = 320

        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)

        self.geometry(f"{width}x{height}+{x}+{y}")

        self.transient(parent)
        self.grab_set()

        self.login_widget = LoginWidget(
            self,
            self.on_login
        )
        self.login_widget.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

    def on_login(self, username, password):

        success, message = self.context.login_controller.login(
            username,
            password
        )

        if success:
            self.destroy()
        else:
            messagebox.showerror("Login", message)
            self.login_widget.clear_password()