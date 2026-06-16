import tkinter as tk
from tkinter import ttk
from tkinter import messagebox



class TableWidget(tk.Frame):

    def __init__(self, parent, columns, action_column_index=None):
        super().__init__(parent)

        self.columns = columns
        self.action_column_index = action_column_index

        self.tree = ttk.Treeview(self, columns=columns, show="headings")
        self.tree.pack(fill="both", expand=True)

        self.setup_columns()
        self.setup_style()

        # 🔥 Bind click event
        self.tree.bind("<Button-1>", self.on_click)
        self.tree.bind("<Motion>", self.on_hover)

        # callbacks (set from outside)
        self.on_edit = None
        self.on_delete = None
        self.action_column_index = len(columns)
        
    def update_row(self, row_id, new_values):
        self.tree.item(row_id, values=new_values)
    def insert(self, row):
        row = list(row)

        # ensure action column exists
        if len(row) == len(self.columns) - 1:
            row.append("Edit    Delete")

        self.tree.insert("", "end", values=row)
        
    def on_hover(self, event):
        region = self.tree.identify("region", event.x, event.y)

        if region == "cell":
            self.tree.config(cursor="hand2")
        else:
            self.tree.config(cursor="")

    def setup_columns(self):
        for col in self.columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, anchor="center")

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

    # ---------- DATA METHODS ----------
    def clear(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

    def insert_row(self, values, tags=None):
        self.tree.insert("", "end", values=values, tags=tags)
        
        
      

    def get_selected(self):
        selected = self.tree.focus()
        return self.tree.item(selected, "values"), selected

    def delete_selected(self):
        selected = self.tree.focus()
        if selected:
            self.tree.delete(selected)
            
    def on_click(self, event):
        row_id = self.tree.identify_row(event.y)
        column = self.tree.identify_column(event.x)

        if not row_id:
            return

        values = self.tree.item(row_id, "values")

        # only action column
        if column != f"#{len(self.columns)}":
            return

        bbox = self.tree.bbox(row_id, column)
        if not bbox:
            return

        x, y, width, height = bbox
        click_x = event.x - x

        # split icon area
        if click_x < width / 2:
            self.edit_row(row_id, values)
        else:
            self.delete_row(row_id)
    
            
            
    def edit_row(self, row_id, values):

        sno = values[0]

        if hasattr(self, "edit_callback"):
            self.edit_callback(sno)
        
   

    def delete_row(self, row_id):

        values = self.tree.item(row_id, "values")

        sno = values[0]

        if not messagebox.askyesno(
            "Delete",
            f"Delete instrument S.No {sno}?"
        ):
            return

        if hasattr(self, "delete_callback"):
            self.delete_callback(sno)

       
                
            
    def update_row(self, row_id, new_values):
        updated_row = list(new_values)

        # re-add action column (IMPORTANT)
        updated_row.append("Edit    Delete")

        self.tree.item(row_id, values=updated_row)