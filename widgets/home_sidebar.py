import tkinter as tk

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
            bg="#2563eb",
            fg="white",
            font=("Arial", 12, "bold"),
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
            font=("Arial", 12, "bold"),
            command=self.open_menu,
            relief="flat"
        )
        self.login_btn.pack(
            side="bottom",
            fill="x",
            padx=15,
            pady=15,
            ipady=10
        )

    def open_menu(self):

        root = self.winfo_toplevel()

        if not self.context.app_state.logged_in:

            from views.login_dialog import LoginDialog

            login = LoginDialog(
                root,
                self.context
            )

            self.wait_window(login)

            if not self.context.app_state.logged_in:
                return
        
        self.context.menu_window.tkraise()

    # def open_menu(self):

    #     root = self.winfo_toplevel()

    #     if not self.app.app_state.logged_in:

    #         from views.login_dialog import LoginDialog

    #         login = LoginDialog(root, self.app)

    #         self.wait_window(login)

    #         if not self.app.app_state.logged_in:
    #             return
    #     print(self.app.menu_window)
    #     print(self.app.menu_window.winfo_exists())
    #     self.app.menu_window.tkraise()
    # def open_menu(self):

    #     root = self.winfo_toplevel()

    #     # Login only once
    #     if not self.app.app_state.logged_in:

    #         from views.login_dialog import LoginDialog

    #         login = LoginDialog(root, self.app)

    #         self.wait_window(login)

    #         if not self.app.app_state.logged_in:
    #             return

    #     # Menu already exists?
    #     if (
    #             self.app.main_window
    #             and self.app.main_window.winfo_exists()
    #         ):

    #         self.app.main_window.tkraise()
    #         return

    #     from views.menu_window import MenuWindow

    #     self.master.destroy()

    #     self.app.main_window = MenuWindow(
    #         root,
    #         self.app
    #     )

    #     self.app.main_window.pack(
    #         fill="both",
    #         expand=True
    #     )
        
    # def open_menu(self):

    #     from views.login_dialog import LoginDialog

    #     root = self.winfo_toplevel()

    #     login = LoginDialog(
    #         root,
    #         self.app
    #     )

    #     self.wait_window(login)

    #     if not self.app.app_state.logged_in:
    #         return

    #     from views.menu_window import MenuWindow

    #     self.master.destroy()

    #     menu = MenuWindow(
    #         root,
    #         self.app
    #     )

    #     self.app.main_window = menu

    #     menu.pack(
    #         fill="both",
    #         expand=True
    #     )