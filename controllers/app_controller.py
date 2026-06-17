class AppController:

    def __init__(self,app):
        self.pages = {}
        self.app = app

    def register_page(self, page_name, page):
        self.pages[page_name] = page

    def show_page(self, page_name):
        if page_name in self.pages:
            self.pages[page_name].tkraise()