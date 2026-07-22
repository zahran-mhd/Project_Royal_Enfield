import customtkinter as ctk


class CTkTableWidget(ctk.CTkFrame):

    def __init__(
            self,
            parent,
            columns,
            column_widths=None,
            action_column=True):

        super().__init__(parent, corner_radius=10,fg_color="white",border_width=1,border_color="#d1d5db")

        self.columns = columns
        self.column_widths = column_widths or [120] * len(columns)
        self.action_column = action_column

        self.edit_callback = None
        self.delete_callback = None

        self.rows = []
        self.selected_row = None

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=0)
        self.grid_columnconfigure(0, weight=1)

        self._create_header()

        self.body = ctk.CTkFrame(
    self,
    fg_color="white",
    corner_radius=8
)
        self.body.grid(
            row=1,
            column=0,
            sticky="nsew",
            padx=2,
            pady=(0, 2)
        )

    # -----------------------------------------------------
    # Header
    # -----------------------------------------------------
    def _create_header(self):

        header = ctk.CTkFrame(
            self,
            fg_color="#2563eb",
            corner_radius=8,
            height=40
        )

        header.grid(row=0, column=0, sticky="ew", padx=2, pady=2)

        total = len(self.columns)

        if self.action_column:
            total += 1

        for i in range(total):
            header.grid_columnconfigure(i, weight=1,uniform="table")

        for i, col in enumerate(self.columns):

            lbl = ctk.CTkLabel(
                header,
                text=col,
                text_color="white",
                font=("Segoe UI", 14, "bold")
            )

            lbl.grid(row=0, column=i, sticky="nsew", padx=5, pady=8)

        if self.action_column:

            lbl = ctk.CTkLabel(
                header,
                text="Actions",
                text_color="white",
                font=("Segoe UI", 14, "bold")
            )

            lbl.grid(
                row=0,
                column=len(self.columns),
                sticky="nsew",
                padx=5
            )

    # -----------------------------------------------------
    # Insert Row
    # -----------------------------------------------------
    def insert(self, values, key=None):

        index = len(self.rows)

        bg = "#FFFFFF" if index % 2 == 0 else "#F5F5F5"

        row = ctk.CTkFrame(
            self.body,
             fg_color=bg,
    corner_radius=0,
    border_width=1,
    border_color="#E5E7EB",
    height=42
        )

        row.pack(fill="x", padx=2, pady=1)

        total = len(self.columns)

        if self.action_column:
            total += 1

        for i in range(total):
            row.grid_columnconfigure(i, weight=1,uniform="table")

        for col, value in enumerate(values):

            lbl = ctk.CTkLabel(
                row,
                text=str(value),
    anchor="center",
    justify="center",
    font=("Segoe UI", 12)
            )

            lbl.grid(
                row=0,
                column=col,
                sticky="nsew",
                padx=5,
                pady=8
            )

        if self.action_column:

            action = ctk.CTkFrame(row, fg_color="transparent")
            action.grid(
                row=0,
                column=len(values),
                padx=5,
                pady=5
            )

            edit_btn = ctk.CTkButton(
                action,
                text="Edit",
                width=70,
                height=30,
                fg_color="#2563eb",
                command=lambda k=key: self._edit(k)
            )

            edit_btn.pack(side="left", padx=3)

            delete_btn = ctk.CTkButton(
                action,
                text="Delete",
                width=70,
                height=30,
                fg_color="#dc2626",
                hover_color="#b91c1c",
                command=lambda k=key: self._delete(k)
            )

            delete_btn.pack(side="left", padx=3)

        row.bind("<Enter>", lambda e, r=row: self._hover(r, True))
        row.bind("<Leave>", lambda e, r=row, c=bg: self._hover(r, False, c))
        row.bind("<Button-1>", lambda e, r=row: self.select_row(r))

        self.rows.append(row)

    # -----------------------------------------------------
    # Hover
    # -----------------------------------------------------
    def _hover(self, row, enter, color="#FFFFFF"):

        if row == self.selected_row:
            return

        if enter:
            row.configure(fg_color="#DBEAFE")
        else:
            row.configure(fg_color=color)

    # -----------------------------------------------------
    # Selection
    # -----------------------------------------------------
    def select_row(self, row):

        if self.selected_row:
            self.selected_row.configure(fg_color="#FFFFFF")

        self.selected_row = row

        row.configure(fg_color="#BFDBFE")

    # -----------------------------------------------------
    # Callbacks
    # -----------------------------------------------------
    def _edit(self, key):

        if self.edit_callback:
            self.edit_callback(key)

    def _delete(self, key):

        if self.delete_callback:
            self.delete_callback(key)

    # -----------------------------------------------------
    # Clear
    # -----------------------------------------------------
    def clear(self):

        for row in self.rows:
            row.destroy()

        self.rows.clear()