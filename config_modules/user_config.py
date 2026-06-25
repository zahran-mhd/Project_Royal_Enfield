import tkinter as tk
from widgets.table_config import TableWidget
from widgets.form_popup import FormPopup

from tkinter import messagebox



class UserConfig(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#eef2f7")
        self.context = context
        self.user_data = []
        self.user_repository = context.user_repository
     
        self.create_ui()
        self.user_tabel()
        self.load_users()

        

    def create_ui(self):
        self.card = tk.Frame(self, bg="white")
        self.card.pack(fill="both", expand=True, padx=20, pady=20)
        
        
        # Header Frame
        header_frame = tk.Frame(self.card, bg="white")
        header_frame.pack(fill="x", padx=10, pady=(10, 15))

         # Add Button
        add_btn = tk.Button(
            header_frame,
            text="+ Add User",
            font=("Segoe UI", 10, "bold"),
            bg="#16a34a",
            fg="white",
            activebackground="#15803d",
            activeforeground="white",
            relief="flat",
            cursor="hand2",
            padx=15,
            pady=8,
            command=self.add_user
        )
        add_btn.pack(side="left")
        
   
        
        
    def user_tabel(self):

        columns = (
            "S.No",
            "Username",
        
            "Role",
            "Action",
            
        )

        self.table = TableWidget(
    self.card,
    columns,
    key_column=1   # Username column
)
        self.table.pack(fill="both", expand=True, padx=20, pady=10)
        self.table.delete_callback = self.delete_user
        self.table.edit_callback = self.edit_user
        
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
            self,
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

        print("added data successfully")
            
    def load_users(self):

        self.table.clear()

        rows = self.user_repository.get_all_users()

        # print("Rows from DB:", [dict(row) for row in rows])

        for i, row in enumerate(rows, start=1):
            self.table.insert([
                i,
                row["Username"],
           
                row["Role"],
                "Edit | Delete"
            ])
            
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
            self,
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
    # def delete_user(self, username):

    #     confirm = messagebox.askyesno(
    #     "Delete User",
    #     f"Are you sure you want to delete user '{username}'?"
    # )

    #     if not confirm:
    #         return

    #     self.user_repository.delete_user(username)
    #     self.load_users()
    
    
    def delete_user(self, username):

        user = self.user_repository.get_user(username)

        if not user:
            messagebox.showerror(
                "Error",
                "User not found."
            )
            return

        # Logged-in user from app_state
        current_user = self.context.app_state.current_user
        current_role = self.context.app_state.current_role

        # print("Current User:", current_user)
        # print("Current Role:", current_role)

        # Prevent Admin/Root from deleting their own account
        if (
            current_user == username and
            current_role.lower() in ["admin", "root"]
        ):
            messagebox.showwarning(
                "Access Denied",
                "You cannot delete your own account."
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