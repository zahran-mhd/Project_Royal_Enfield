import tkinter as tk
from views.menu_window import MenuWindow

if __name__ == "__main__":

    root = tk.Tk()
    root.title("Royal Enfield Dashboard")
    root.geometry("1400x800")

    app = MenuWindow(root)
    app.pack(fill="both", expand=True)

    root.mainloop()