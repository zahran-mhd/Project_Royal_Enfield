import tkinter as tk
from views.login_dialog import LoginDialog

class HomeSidebar(tk.Frame):

    def __init__(self, parent, context):

        super().__init__(
            parent,
            bg="#1f2937",
            width=250
        )

        self.context = context
        self.parent = parent

        self.pack_propagate(False)

        # MENU Button (Top)
        self.menu_btn = tk.Button(
            self,
            text="MENU",
            bg="#0AA08C",
            fg="white",
            font=("Bookman Antiqua", 12, "bold"),
            cursor="hand2",
            command=self.open_menu,
            relief="flat"
        )
        self.menu_btn.pack(
            side="top",
            fill="x",
            padx=15,
            pady=15,
            ipady=10
        )

        # Spacer
        spacer = tk.Frame(self, bg="#1f2937")
        spacer.pack(fill="both", expand=True)

        # LOGIN Button (Bottom)
        self.login_btn = tk.Button(
            self,
            text="LOGIN",
            bg="#16a34a",
            fg="white",
            font=("Bookman Antiqua", 12, "bold"),
             cursor="hand2",
          command=self.login_logout,   # Change this
            relief="flat"
        )
        self.login_btn.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15,
            ipady=10
        )
        
        self.update_login_button()
    def update_login_button(self):
        if self.context.app_state.logged_in:
            self.login_btn.config(
                text="LOGOUT",
                bg="#dc2626"
            )
        else:
            self.login_btn.config(
                text="LOGIN",
                bg="#16a34a"
            )
            
    # def login_logout(self):

    #     if self.context.app_state.logged_in:

    #         # Logout
    #         self.context.login_controller.logout()

    #         self.update_login_button()

    #         # Destroy old MenuWindow
    #         if self.context.menu_window:

    #             self.context.menu_window.destroy()

    #             self.context.menu_window = None

    #         # Clear old sidebar reference
    #         self.context.app_controller.sidebar = None

    #         # Clear old registered pages
    #         self.context.app_controller.pages.clear()

    #         # Show HomeScreen
    #         self.context.home_screen.tkraise()

    #     else:

    #         self.open_menu()
    # def open_menu(self):

    #     root = self.winfo_toplevel()

    #     if not self.context.app_state.logged_in:

            

    #         login = LoginDialog(
    #             root,
    #             self.context
    #         )

    #         self.wait_window(login)

    #         if not self.context.app_state.logged_in:
    #             return
        
    #     self.context.menu_window.tkraise()
    
    # def login_logout(self):

    #     if self.context.app_state.logged_in:

    #         # ==============================
    #         # LOGOUT
    #         # ==============================

    #         self.context.login_controller.logout()

    #         self.update_login_button()

    #         if self.context.menu_window:

    #             self.context.menu_window.place_forget()

    #         self.context.home_screen.tkraise()

    #     else:

    #         # ==============================
    #         # LOGIN
    #         # ==============================

    #         self.open_menu()

    def login_logout(self):

        if self.context.app_state.logged_in:

            # ==============================
            # LOGOUT
            # ==============================

            self.context.login_controller.logout()

            self.update_login_button()

            # Hide MenuWindow but DO NOT destroy it
            if self.context.menu_window:
                self.context.menu_window.place_forget()

            # Show Home
            self.context.home_screen.tkraise()

        else:

            # ==============================
            # LOGIN
            # ==============================

            self.open_menu()


    # def open_menu(self):

    #     root = self.winfo_toplevel()

    #     if not self.context.app_state.logged_in:

    #         login = LoginDialog(
    #             root,
    #             self.context
    #         )

    #         self.wait_window(login)

    #         if not self.context.app_state.logged_in:
    #             return

    #         self.update_login_button()

    #     self.context.create_menu_window()

    def open_menu(self):

        root = self.winfo_toplevel()

        if not self.context.app_state.logged_in:

            login = LoginDialog(
                root,
                self.context
            )

            self.wait_window(login)

            if not self.context.app_state.logged_in:
                return

            self.update_login_button()

        # Show MenuWindow
        self.context.create_menu_window()

    # def open_menu(self):

    #     root = self.winfo_toplevel()

    #     if not self.context.app_state.logged_in:

    #         login = LoginDialog(
    #             root,
    #             self.context
    #         )

    #         self.wait_window(login)

    #         if not self.context.app_state.logged_in:
    #             return

    #         self.update_login_button()

    #         # Create fresh MenuWindow
    #         self.context.create_menu_window()

    #     else:

    #         if self.context.menu_window:

    #             self.context.menu_window.tkraise()

