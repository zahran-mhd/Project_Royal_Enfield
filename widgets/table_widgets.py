import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TableWidget(tk.Frame):

    def __init__(self, parent, columns, key_column=0,
                 style_name="LiveTable.Treeview",
                 height=17):
        super().__init__(parent)

        self.columns = columns
        self.key_column = key_column
        self.row_keys = {}

        self.setup_style()

        self.tree = ttk.Treeview(
            self,
            columns=self.columns,
            show="headings",
            height=height,
            style=style_name
        )

        self.tree.pack(fill="both", expand=True)
        
          
        self.tree.tag_configure("even", background="white")
        self.tree.tag_configure("odd", background="#f2f2f2")

        self.setup_columns()

        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Motion>", self.on_hover)
      

        self.edit_callback = None
        self.delete_callback = None

    # ---------------- STYLE ----------------
    def setup_style(self):
        style = ttk.Style()
        style.theme_use("default")

        # Live Table Style
        style.configure(
            "LiveTable.Treeview",
            rowheight=23,
          borderwidth=1,
    relief="solid",
            font=("Segoe UI", 10)
        )

        style.configure(
            "LiveTable.Treeview.Heading",
            background="#1d4ed8",
            foreground="white",
            font=("Segoe UI", 12, "bold")
        )

        # Config Style
        style.configure(
            "Config.Treeview",
            borderwidth=1,
    relief="solid",
            rowheight=35,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Config.Treeview.Heading",
            background="#1d4ed8",
            foreground="white",
            font=("Segoe UI", 11, "bold")
        )
        
  

    # ---------------- COLUMNS ----------------
    def setup_columns(self):
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(
                col,
                width=75,
                anchor="center",
                stretch=True
            )

  
    
    def insert(self, row, key=None):

        row = list(row)

        if len(row) == len(self.columns) - 1:
            row.append("Edit | Delete")

        tag = "even" if len(self.tree.get_children()) % 2 == 0 else "odd"

        item_id = self.tree.insert(
            "",
            "end",
            values=row,
            tags=(tag,)
        )

        self.row_keys[item_id] = key
        return item_id
        # ---------------- CLEAR ----------------
    def clear(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.row_keys.clear()
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

        # print("Row Values:", values)

        # Action column
        if column != f"#{len(self.columns)}":
            return

        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return

        x, y, width, height = bbox
        click_x = event.x - x

        # Actual database ID
        key = values[self.key_column]

        # print("Selected Instrument ID:", key)

        if click_x < width / 2:
            if self.edit_callback:
                self.edit_callback(key)
        else:
            if self.delete_callback:
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