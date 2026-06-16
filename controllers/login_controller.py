# controllers/login_controller.py

class LoginController:

    def __init__(self, app):

        self.app = app

    # ------------------------------------
    # LOGIN
    # ------------------------------------

    def login(self, username, password):

        username = username.strip()

        if not username:
            return False, "Username is required"

        if not password:
            return False, "Password is required"

        user = self.app.user_repository.authenticate(
            username,
            password
        )

        if user is None:

            return False, "Invalid username or password"

        # ------------------------------------
        # UPDATE APP STATE
        # ------------------------------------

        self.app.app_state.logged_in = True

        self.app.app_state.current_user = (
            user["Username"]
        )

        self.app.app_state.current_role = (
            user["Role"]
        )

        return True, "Login Successful"

    # ------------------------------------
    # LOGOUT
    # ------------------------------------

    def logout(self):

        self.app.app_state.logged_in = False

        self.app.app_state.current_user = ""

        self.app.app_state.current_role = ""

        self.app.app_state.test_running = False

    # ------------------------------------
    # ROLE CHECK
    # ------------------------------------

    def has_role(self, role):

        return (
            self.app.app_state.current_role.lower()
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