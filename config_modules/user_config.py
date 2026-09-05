import tkinter as tk
from widgets.ctk_table import CTkTableWidget
from widgets.form_popup import FormPopup
from tkinter import messagebox
import customtkinter as ctk
from controllers.user_controller import UserController




class UserConfig(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#eef2f7")
        self.context = context
        self.controller = UserController(self,context)
        self.user_data = []
        self.user_repository = context.user_repository
     
        self.create_ui()
        self.user_tabel()
        self.controller.load_users()

        

    def create_ui(self):

        # Main Card
        self.card = ctk.CTkFrame(
            self,
            fg_color="white",
            corner_radius=10
        )
        self.card.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=20
        )

        # Header
        header = ctk.CTkFrame(
            self.card,
            fg_color="transparent"
        )
        header.pack(
            fill="x",
            padx=15,
            pady=(15, 10)
        )

        # Add Instrument Button
        add_btn = ctk.CTkButton(
            header,
            text="+ Add User",
            font=ctk.CTkFont(
                family="Bookman Antiqua",
                size=16,
                weight="bold"
            ),
            fg_color="#16A34A",
            hover_color="#15803D",
            text_color="white",
            corner_radius=8,
            width=170,
            height=38,
            command=self.controller.add_user
        )
        add_btn.pack(side="left")
        
   
        
        
    def user_tabel(self):

        columns = (
            "S.No",
            "Username",
            "Role",
           
            
        )

      
        table_frame = tk.Frame(self.card, bg="white", height=420)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)
        table_frame.pack_propagate(False)

        self.table = CTkTableWidget(
            table_frame,
            columns=columns
        )
        self.table.pack(fill="x", padx=20, pady=10)
        self.table.delete_callback = self.controller.delete_user
        self.table.edit_callback = self.controller.edit_user
        
    

   
    def display_users(self, rows):

        self.table.clear()

        for i, row in enumerate(rows, start=1):

            self.table.insert(
                [
                    i,
                    row["Username"],
                    row["Role"]
                ],
                key=row["Username"]
            )
    
            
    # def edit_user(self, username):

    #     # print("Received:", username, type(username))

    #     user = self.user_repository.get_user(username)

    #     if not user:
    #         print("User not found")
    #         return

    #     prefill = [
    #         user["username"],
    #         user["role"]
    #     ]

    #     def save(values):

    #         self.user_repository.update_user(
    #             username,          # old username
    #             values[0],         # new username
    #             user["Password"],  # existing password
    #             values[1]          # role
    #         )

    #         self.load_users()

    #     FormPopup(
    #         self,
    #         title="Edit User Configuration",
    #         fields=["Username", "Role"],
    #         prefill=prefill,
    #         on_save=save,
    #         dropdowns={
    #             "Role": [
    #                 "Admin",
    #                 "Operator"
    #             ]
    #         }
    #     )
    
    
    
