import tkinter as tk

from widgets.home_sidebar import HomeSidebar
from widgets.header import Header
from widgets.sub_header import SubHeader


class HomeScreen(tk.Frame):

    def __init__(self, parent, app):

        super().__init__(parent)

        self.app = app
        
        
        # ================= Header =================
        self.header = Header(self)
        self.header.pack(side="top", fill="x")
        self.sidebar = HomeSidebar(self,self.app)
        self.sidebar.pack(side="left", fill="y")
        body_frame = tk.Frame(self, bg="white")
        body_frame.pack(fill="both", expand=True)
        
        # ================= Right Section =================
        right_frame = tk.Frame(body_frame, bg="#f5f5f5")
        right_frame.pack(side="right", fill="both", expand=True)
        
        # ================= Sub Header =================
        self.sub_header = SubHeader(right_frame)
        self.sub_header.pack(side="top", fill="x")

        self.main_content = tk.Frame(
            self,
            bg="#f5f5f5"
        )
        self.main_content.pack(
            side="right",
            fill="both",
            expand=True
        )