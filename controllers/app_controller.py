class AppController:

    def __init__(self, app):
        self.pages = {}
        self.app = app
        self.sidebar = None

    def register_page(self, page_name, page):
        self.pages[page_name] = page

    def register_sidebar(self, sidebar):
        self.sidebar = sidebar

    def show_page(self, page_name):

        if page_name in self.pages:
            self.pages[page_name].tkraise()

            if self.sidebar:
                self.sidebar.highlight_menu(page_name)