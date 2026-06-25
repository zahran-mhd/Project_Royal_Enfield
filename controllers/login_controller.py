# controllers/login_controller.py

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

        # ------------------------------------
        # UPDATE APP STATE
        # ------------------------------------

        self.context.app_state.logged_in = True

        self.context.app_state.current_user = (
            user["Username"]
        )

        self.context.app_state.current_role = (
            user["Role"]
        )

        return True, "Login Successful"

    # ------------------------------------
    # LOGOUT
    # ------------------------------------

    def logout(self):

        self.context.app_state.logged_in = False

        self.context.app_state.current_user = ""

        self.context.app_state.current_role = ""

        self.context.app_state.test_running = False

    # ------------------------------------
    # ROLE CHECK
    # ------------------------------------

    def has_role(self, role):

        return (
            self.context.app_state.current_role.lower()
            == role.lower()
        )

    # ------------------------------------
    # ROOT
    # ------------------------------------

    def is_root(self):

        return self.has_role("root")

    # ------------------------------------
    # ADMIN
    # ------------------------------------

    def is_admin(self):

        return self.has_role("admin")

    # ------------------------------------
    # OPERATOR
    # ------------------------------------

    def is_operator(self):

        return self.has_role("operator")