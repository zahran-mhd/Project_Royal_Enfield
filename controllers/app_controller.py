

from utils.permission import Permissions
class AppController:

    def __init__(self, context):

        self.pages = {}
        self.app = context
        self.sidebar = None
        self.current_page = None

    def register_page(self, page_name, page):

        self.pages[page_name] = page

    def register_sidebar(self, sidebar):

        self.sidebar = sidebar

    def show_page(self, page_name):

        role = self.app.app_state.current_role

        if not Permissions.can_access(role, page_name):
            return

        self.current_page = page_name

        if page_name == "Configuration":
            self.pages[page_name].user_page.controller.load_users()

        self.pages[page_name].tkraise()

        if self.sidebar:
            self.sidebar.highlight_menu(page_name)

    def reset_pages(self):

        self.current_page = None

        for page in self.pages.values():

            if hasattr(page, "reset_page"):
                page.reset_page()
   