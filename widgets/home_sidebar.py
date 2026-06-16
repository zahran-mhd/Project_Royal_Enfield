import tkinter as tk

class HomeSidebar(tk.Frame):

    def __init__(self, parent):

        super().__init__(
            parent,
            bg="#1f2937",
            width=250
        )
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

        from views.menu_window import MenuWindow

        root = self.winfo_toplevel()

        # Remove HomeScreen
        self.master.destroy()

        # Create MenuWindow
        menu = MenuWindow(root)
        menu.pack(fill="both", expand=True)