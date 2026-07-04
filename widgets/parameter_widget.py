import tkinter as tk
from tkinter import ttk


def create_label(parent, text, row, column):

    label = tk.Label(
        parent,
        text=text,
        bg="white",
        font=("Arial", 11)
    )
    label.grid(
        row=row,
        column=column,
        sticky="w",
        pady=(5, 2)
    )

    return label


def create_entry(parent, row, column, width=25):

    entry = ttk.Entry(
        parent,
        width=width
    )

    entry.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="ew"
    )

    return entry


def create_combobox(parent, row, column, values):

    combo = ttk.Combobox(
        parent,
        values=values,
        state="readonly"
    )

    combo.grid(
        row=row,
        column=column,
        padx=5,
        pady=5,
        sticky="ew"
    )

    return combo

def create_button(
    parent,
    text,
    bg,
    fg,
    row,
    column,
    command=None
):

    btn = tk.Button(
        parent,
        text=text,
        bg=bg,
        fg=fg,
        relief="flat",
        padx=15,
        pady=8,
        command=command
    )

    btn.grid(
        row=row,
        column=column,
        padx=4,
        pady=5
    )

    return btn

def parameter_row(parent, row, label_text, unit):

    tk.Label(
        parent,
        text=label_text,
        bg="white",
        font=("Arial",11)
    ).grid(
        row=row,
        column=0,
        sticky="w",
        padx=15,
        pady=(5,2)
    )

    entry = ttk.Entry(parent,width=28)
    entry.grid(
        row=row+1,
        column=0,
        padx=(15,5),
        pady=(0,10),
        sticky="ew"
    )

    tk.Label(
        parent,
        text=unit,
        bg="white",
        font=("Arial",11)
    ).grid(
        row=row+1,
        column=1,
        padx=(5,15),
        sticky="w"
    )

    return entry


def create_table(parent, columns, rows=3):

    table = tk.Frame(parent, bg="white")

    # Make columns expand equally
    for c in range(len(columns)):
        table.grid_columnconfigure(c, weight=1)

    # ---------- Header ----------
    for c, text in enumerate(columns):
        lbl = tk.Label(
            table,
            text=text,
            bg="#3b5bdb",
            fg="white",
            font=("Arial", 11, "bold"),
            relief="solid",
            bd=1,
            padx=10,
            pady=10
        )
        lbl.grid(
            row=0,
            column=c,
            sticky="nsew"
        )

    # ---------- Rows ----------
    for r in range(1, rows + 1):

        # S.No
        tk.Label(
            table,
            text=str(r),
            bg="white",
            font=("Arial", 11),
            relief="solid",
            bd=1
        ).grid(
            row=r,
            column=0,
            sticky="nsew"
        )

        # Entry Cells
        for c in range(1, len(columns)):

            frame = tk.Frame(
                table,
                bg="white",
                relief="solid",
                bd=1
            )

            frame.grid(
                row=r,
                column=c,
                sticky="nsew"
            )

            entry = ttk.Entry(
                frame,
                justify="center"
            )

            entry.pack(
                fill="both",
                expand=True,
                padx=2,
                pady=2
            )

    return table

def create_bottom_button(parent, text, color):

    btn = tk.Button(
        parent,
        text=text,
        bg=color,
        fg="white",
        relief="flat",
        font=("Arial", 11, "bold"),
        padx=20,
        pady=8
    )

    return btn