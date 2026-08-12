import tkinter as tk

from utils.permission import Permissions

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
            font=("Bookman Antiqua", 20, "bold")
        ).pack(pady=20)
        
        role = self.controller.app.app_state.current_role

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

            if not Permissions.can_access(role, menu):
                continue

            btn = tk.Button(
                self,
                text=menu,
                bg="#1f2937",
                 font=("Bookman Antiqua",12),
                fg="white",
                relief="flat",
                anchor="w",
                padx=20,
                cursor="hand2",
                command=lambda m=menu: self.controller.show_page(m)
            )

            btn.pack(
                fill="x",
                padx=10,
                pady=3,
                ipady=8
            )

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

            
            

                
    def reset_sidebar(self):

        # Reset selected menu
        self.highlight_menu("Test Settings")

        