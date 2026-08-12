class LoginController:

    def __init__(self, context):
        self.context = context

    # ------------------------------------
    # LOGIN
    # ------------------------------------

    def login(self, username, password):

        username = username.strip()

        if not username:
            return False, "Username is required"

        if not password:
            return False, "Password is required"

        user = self.context.user_repository.authenticate(
            username,
            password
        )

        if user is None:
            return False, "Invalid username or password"

        # Update app state
        self.context.app_state.logged_in = True
        self.context.app_state.current_user = user["Username"]
        self.context.app_state.current_role = user["Role"]
        
        
        # Update existing SubHeader
        home_screen = getattr(
            self.context,
            "home_screen",
            None
        )

        if home_screen:
            home_screen.sub_header.update_user()

        # Do not access old sidebar here
        # MenuWindow will create a fresh sidebar

        return True, "Login Successful"

    # ------------------------------------
    # LOGOUT
    # ------------------------------------
    def logout(self):

        self.context.app_state.logged_in = False
        self.context.app_state.current_user = ""
        self.context.app_state.current_role = ""
        self.context.app_state.test_running = False

        # Clear global selected DUTs
        self.context.selected_duts.clear()

        # Reset all page-specific data
        self.context.app_controller.reset_pages()

        # Reset sidebar
        if self.context.app_controller.sidebar:
            self.context.app_controller.sidebar.reset_sidebar()

        # Update existing SubHeader
        home_screen = getattr(
            self.context,
            "home_screen",
            None
        )

        if home_screen:
            home_screen.sub_header.update_user()
     

    # ------------------------------------
    # ROLE CHECK
    # ------------------------------------

    def has_role(self, role):

        return (
            self.context.app_state.current_role.lower()
            == role.lower()
        )

    def is_root(self):
        return self.has_role("root")

    def is_admin(self):
        return self.has_role("admin")

    def is_operator(self):
        return self.has_role("operator")