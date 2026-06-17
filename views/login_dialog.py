# pages/login_dialog.py
 
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
 
 
class LoginDialog(tk.Toplevel):
 
    def __init__(self, parent, app):
 
        super().__init__(parent)
 
        self.app = app
 
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
 
    # ------------------------------------
    # LOGIN BUTTON CLICK
    # ------------------------------------
 
    def on_login(self):
 
        success, message = (
            self.app.login_controller.login(
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