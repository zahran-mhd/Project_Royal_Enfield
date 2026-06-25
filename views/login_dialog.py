# pages/login_dialog.py
 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
 
 
class LoginDialog(tk.Toplevel):
 
    def __init__(self, parent, context):
 
        super().__init__(parent)
 
        self.context = context
 
        self.title("Login")
 
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
 
        ttk.Label(self, text="Username").pack()
 
        ttk.Entry(
            self,
            textvariable=self.username_var
        ).pack()
 
        ttk.Label(self, text="Password").pack()
 
        ttk.Entry(
            self,
            textvariable=self.password_var,
            show="*"
        ).pack()
 
        ttk.Button(
            self,
            text="Login",
            command=self.on_login
        ).pack()
    def login(self, username, password):

        user = self.context.user_repository.authenticate(
            username,
            password
        )

        if not user:
            return False, "Invalid username or password"

        # Store logged-in user
        self.context.current_user = {
            "Username": user["Username"],
            "Role": user["Role"]
        }

        print("Current User:", self.context.current_user)

        return True, "Login Successful"
    # ------------------------------------
    # LOGIN BUTTON CLICK
    # ------------------------------------
 
    def on_login(self):
 
        success, message = (
            self.context.login_controller.login(
                self.username_var.get(),
                self.password_var.get()
            )
        )
 
        if success:
 
            self.destroy()
 
        else:
 
            messagebox.showerror(
                "Login",
                message
            )