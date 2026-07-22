import tkinter as tk

class Sidebar(tk.Frame):

    def __init__(self, parent, controller):
        super().__init__(parent, bg="#1f2937", width=250)

        self.pack_propagate(False)   # Prevent auto-resizing
        
        self.controller = controller
        self.menu_buttons = {}
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
            "Endurance-Live Monitoring",
            "Parameter Settings",
            "Line Regulation",
            "Load Regulation",
            "Historical Trend",
            "Alarm Settings",
            "Report"
        ]

        for menu in menus:
            btn = tk.Button(
                self,
                text=menu,
                 bg="#1f2937",
                fg="white",
                relief="flat",
                anchor="w",
                padx=20,
                cursor="hand2",
               command=lambda m=menu: self.controller.show_page(m)
            )
            btn.pack(fill="x", padx=10, pady=3, ipady=8)
            self.menu_buttons[menu] = btn
            
            
            
            
        self.highlight_menu("Test Settings")
        
        
        
    def on_menu_click(self,menu):
        self.highlight_menu(menu)
        self.controller.show_page(menu)
        
    def highlight_menu(self, selected_menu):

        for menu, btn in self.menu_buttons.items():

            if menu == selected_menu:
                btn.config(
                    bg="#2563eb",
                    fg="white"
                )
            else:
                btn.config(
                    bg="#1f2937",
                    fg="white"
                )
                
    def hide_configuration(self):
        if "Configuration" in self.menu_buttons:
            self.menu_buttons["Configuration"].pack_forget()
            
            

                
    def reset_sidebar(self):

        # Reset selected menu
        self.highlight_menu("Test Settings")

        # Reset role-based menu
        self.update_menu_by_role("")
        
    
    def update_menu_by_role(self, role):

        config_btn = self.menu_buttons["Configuration"]

        if role.lower() == "operator":

            if config_btn.winfo_ismapped():
                config_btn.pack_forget()

        else:

            if not config_btn.winfo_ismapped():

                config_btn.pack(
                    fill="x",
                    padx=10,
                    pady=3,
                    ipady=8,
                    before=self.menu_buttons["Endurance-Live Monitoring"]
                )