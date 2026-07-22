class ConfigurationController:

    def __init__(self, view, context):
        self.view = view
        self.context = context

    def show_instrument(self, channel_id):
        self.view.instrument_page.controller.set_channel(channel_id)

        self.view.hide_pages()
        self.view.instrument_page.pack(fill="both", expand=True)

        self.highlight_tab(self.view.channel_buttons[channel_id])

    def show_user(self):
        self.view.user_page.controller.load_users()

        self.view.hide_pages()
        self.view.user_page.pack(fill="both", expand=True)

        self.highlight_tab(self.view.user_btn)

    def highlight_tab(self, selected_btn):
        default_bg = "#dce3eb"
        default_fg = "#2c3e50"
        active_bg = "#1f6aa5"
        active_fg = "white"

        for btn in self.view.channel_buttons.values():
            btn.config(bg=default_bg, fg=default_fg)

        self.view.user_btn.config(bg=default_bg, fg=default_fg)

        selected_btn.config(bg=active_bg, fg=active_fg)