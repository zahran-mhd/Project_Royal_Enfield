import tkinter as tk

class Sidebar(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1f2937", width=250)

        self.pack_propagate(False)   # Prevent auto-resizing
        
        self.controller = controller

        tk.Label(
            self,
            text="MENU",
            bg="#1f2937",
            fg="white",
            font=("Arial", 18, "bold")
        ).pack(pady=20)

        menus = [
            "Test Settings",
            "Configuration",
            "Live Monitoring",
            "Parameter Settings",
            "Line Regulation",
            "Load Regulation",
            "Historical Trend",
            "Alarm Settings",
            "Report"
        ]

        for menu in menus:
            tk.Button(
                self,
                text=menu,
                 bg="#1f2937",
                fg="white",
                relief="flat",
                anchor="w",
                padx=20,
               command=lambda m=menu: self.controller.show_page(m)
            ).pack(fill="x", padx=10, pady=3, ipady=8)