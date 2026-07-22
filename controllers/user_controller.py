from widgets.form_popup import FormPopup
from tkinter import messagebox


class UserController:
    def __init__(self,view,context):
        self.view = view
        self.context = context
        self.user_repository = context.user_repository
        self.selected_channel_id = None
    def load_users(self):

        rows = self.user_repository.get_all_users()

        current_role = self.context.app_state.current_role.lower()

        if current_role == "admin":
            rows = [
                row for row in rows
                if row["Role"].lower() != "root"
            ]

        self.view.display_users(rows)
        
    def add_user(self):

        def save(values):

            username = values[0]
            password = values[1]
            role = values[2]

            self.user_repository.add_user(
                username,
                password,
                role
            )

            self.load_users()

        FormPopup(
            self.view,
            "Add User",
            ["Username", "Password", "Role"],
            save,
            dropdowns={
                "Role": [
                    "Admin",
                    "Operator"
                ]
            }
        )
        
        
    def delete_user(self, username):

        user = self.user_repository.get_user(username)

        if not user:
            messagebox.showerror(
                "Error",
                "User not found."
            )
            return

        # Logged-in user
        current_user = self.context.app_state.current_user
        current_role = self.context.app_state.current_role

        # Prevent Admin from deleting their own account
        if (
            current_role.lower() == "admin"
            and current_user.lower() == username.lower()
        ):
            messagebox.showwarning(
                "Access Denied",
                "Admin users cannot delete their own account."
            )
            return

        confirm = messagebox.askyesno(
            "Delete User",
            f"Are you sure you want to delete '{username}'?"
        )

        if not confirm:
            return

        self.user_repository.delete_user(username)

        messagebox.showinfo(
            "Success",
            "User deleted successfully."
        )

        self.load_users()
        
    def edit_user(self, username):

        # print("Received:", username, type(username))

        user = self.user_repository.get_user(username)

        if not user:
            print("User not found")
            return

        prefill = [
            user["username"],
            user["role"]
        ]

        def save(values):

            self.user_repository.update_user(
                username,          # old username
                values[0],         # new username
                user["Password"],  # existing password
                values[1]          # role
            )

            self.load_users()

        FormPopup(
            self.view,
            title="Edit User Configuration",
            fields=["Username", "Role"],
            prefill=prefill,
            on_save=save,
            dropdowns={
                "Role": [
                    "Admin",
                    "Operator"
                ]
            }
        )
    
    
            
    