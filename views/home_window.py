
import tkinter as tk

from widgets.home_sidebar import HomeSidebar
from widgets.header import Header
from widgets.sub_header import SubHeader

from pages.home_page import HomePage


class HomeScreen(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(parent)

        self.context = context
        self.controller = context.app_controller

        # Store reference in context
        self.context.home_screen = self

        # ==================================================
        # HEADER
        # ==================================================

        self.header = Header(self)
        self.header.pack(
            side="top",
            fill="x"
        )

        # ==================================================
        # BODY
        # ==================================================

        body_frame = tk.Frame(
            self,
            bg="white"
        )
        body_frame.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ==================================================
        # SIDEBAR
        # ==================================================

        self.sidebar = HomeSidebar(
            body_frame,
            self.context
        )
        self.sidebar.pack(
            side="left",
            fill="y"
        )

        # ==================================================
        # RIGHT CONTENT
        # ==================================================

        right_frame = tk.Frame(
            body_frame,
            bg="#f5f5f5"
        )
        right_frame.pack(
            side="left",
            fill="both",
            expand=True
        )

        # ==================================================
        # SUB HEADER
        # ==================================================

        self.sub_header = SubHeader(
            right_frame,
            self.context
        )
        self.sub_header.pack(
            side="top",
            fill="x"
        )

        # ==================================================
        # MAIN CONTENT
        # ==================================================

        self.main_content = tk.Frame(
            right_frame,
            bg="#f5f5f5"
        )
        self.main_content.pack(
            side="top",
            fill="both",
            expand=True
        )

        # ==================================================
        # PAGES
        # ==================================================

        self.create_pages()

        # ==================================================
        # PLACE PAGES
        # ==================================================

        self.place_pages()

    # ======================================================
    # CREATE PAGES
    # ======================================================

    def create_pages(self):

        home_page = HomePage(
            self.main_content,
            self.context
        )

        self.controller.register_page(
            "Home Page",
            home_page
        )

    # ======================================================
    # PLACE PAGES
    # ======================================================

    def place_pages(self):

        for page in self.controller.pages.values():

            page.place(
                relx=0,
                rely=0,
                relwidth=1,
                relheight=1
            )
