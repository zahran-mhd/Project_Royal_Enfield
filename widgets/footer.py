import tkinter as tk

class Footer(tk.Frame):

    def __init__(self, parent,context):
        super().__init__(parent, bg="#0AA08C", height=40,bd=2,relief="solid")

        self.pack_propagate(False)
        # tk.Label(
        #     self,
        #     text="FOOTER",
        #     bg="red",
        #     fg="white"
        # ).pack(expand=True)
        self.context=context

        center = tk.Frame(self, bg="#0AA08C")
        center.pack(side="left", expand=True)

        tk.Button(
    center,
    text="Home",
    font=("Bookman Antiqua", 12, "bold"),
    fg="white",
    bg="#0AA08C",
    activebackground="#0AA08C",
    activeforeground="white",
    relief="flat",
     cursor="hand2",
    borderwidth=0,
    command=self.open_home
).pack(pady=10)

    # def open_home(self):

    #     from views.home_window import HomeScreen

    #     root = self.winfo_toplevel()

    #     # Remove all widgets currently displayed
    #     for widget in root.winfo_children():
    #         widget.destroy()

    #     # Open Home Screen
    #     home = HomeScreen(root,self.app)
    #     home.pack(fill="both", expand=True)

    def open_home(self):

        self.context.home_screen.tkraise()