import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TableWidget(tk.Frame):

    def __init__(self, parent, columns,key_column=0):
        super().__init__(parent)

        self.columns = columns
        self.key_column = key_column

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        self.setup_columns()
        self.setup_style()

        # Bind events
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Motion>", self.on_hover)

        # callbacks (set from outside)
        self.edit_callback = None
        self.delete_callback = None

    # ---------------- STYLE ----------------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        style.configure(
            "Treeview.Heading",
            background="#1d4ed8",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )

        style.configure(
            "Treeview",
            rowheight=35,
            font=("Segoe UI", 10)
        )

    # ---------------- COLUMNS ----------------
    def setup_columns(self):
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

    # ---------------- INSERT ----------------
    def insert(self, row):
        row = list(row)

        # Ensure action column exists
        if len(row) == len(self.columns) - 1:
            row.append("Edit | Delete")

        self.tree.insert("", "end", values=row)

    # ---------------- CLEAR ----------------
    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    # ---------------- HOVER ----------------
    def on_hover(self, event):
        region = self.tree.identify("region", event.x, event.y)

        if region == "cell":
            self.tree.config(cursor="hand2")
        else:
            self.tree.config(cursor="")

    # ---------------- CLICK HANDLER ----------------
    def on_click(self, event):

        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not row_id:
            return

        values = self.tree.item(row_id, "values")

        print("Row Values:", values)

        # Action column
        if column != f"#{len(self.columns)}":
            return

        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return

        x, y, width, height = bbox
        click_x = event.x - x

        # IMPORTANT
        key = values[self.key_column]

        print("Selected Key:", key)

        if click_x < width / 2:
            if hasattr(self, "edit_callback"):
                self.edit_callback(key)
        else:
            if hasattr(self, "delete_callback"):
                self.delete_callback(key)

    # ---------------- GET SELECTED ----------------
    def get_selected(self):
        selected = self.tree.focus()
        return self.tree.item(selected, "values"), selected

    # ---------------- DELETE SELECTED ----------------
    def delete_selected(self):
        selected = self.tree.focus()

        if selected:
            self.tree.delete(selected)

    # ---------------- UPDATE ROW ----------------
    def update_row(self, row_id, new_values):
        updated_row = list(new_values)
        updated_row.append("Edit | Delete")

        self.tree.item(row_id, values=updated_row)