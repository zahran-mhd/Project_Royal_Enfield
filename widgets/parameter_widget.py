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
            fg="yellow",
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
                bg="black",
                relief="solid",
                bd=1,
                width=80,
                height=28
            )

            frame.grid(
                row=r,
                column=c,
                sticky="nsew"
            )

            frame.grid_propagate(False)

            value = tk.StringVar()

            entry = ttk.Entry(
                frame,
                justify="center",
                textvariable=value
            )

            entry.pack(
                fill="both",
                expand=True,
                padx=1,
                pady=1
            )

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


def section_title(parent, text, row, column, columnspan=1):

    label = tk.Label(
        parent,
        text=text,
        bg="white",
        font=("Arial",12,"bold")
    )

    label.grid(
        row=row,
        column=column,
        columnspan=columnspan,
        sticky="w",
        pady=(15,15)
    )

    return label


def table_header(parent, text, row, column):

    lbl = tk.Label(
        parent,
        text=text,
        bg="#f2f2f2",
        relief="solid",
        bd=1,
        font=("Arial",10,"bold"),
        padx=12,
        pady=7
    )

    lbl.grid(
        row=row,
        column=column,
        sticky="nsew"
    )

    return lbl


def table_label(parent, text, row, column):

    lbl = tk.Label(
        parent,
        text=text,
        bg="white",
        relief="solid",
        bd=1,
        padx=12,
        width=14,  
        pady=10
    )

    lbl.grid(
        row=row,
        column=column,
        sticky="nsew"
    )

    return lbl

def table_entry(parent, row, column):

    frame = tk.Frame(
        parent,
        bg="black",      # Border color
        relief="solid",
        bd=1,
        width=120,
        height=38
    )

    frame.grid(
        row=row,
        column=column,
        sticky="nsew"
    )

    frame.grid_propagate(False)

    entry = ttk.Entry(
        frame,
        justify="center"
    )

    entry.pack(
        fill="both",
        expand=True,
        padx=1,
        pady=1
    )

    return entry


def load_header(parent):

    top = tk.Frame(parent, bg="white")
    top.pack(fill="x", padx=40, pady=(15,25))

    # Configure all columns
    for i in range(9):
        top.grid_columnconfigure(i, weight=0)

    # Dwell Time
    tk.Label(
        top,
        text="Dwell Time",
        bg="white",
        font=("Arial",11,"bold")
    ).grid(row=0, column=0, sticky="w", padx=(0,8))

    dwell_time = ttk.Entry(
        top,
        width=10
    )

    dwell_time.grid(
        row=0,
        column=1,
        sticky="w"
    )

    tk.Label(
        top,
        text="Sec",
        bg="white",
        font=("Arial",11)
   ).grid(row=0, column=2, sticky="w", padx=(5,70))


    # Input Voltage
    tk.Label(
        top,
        text="Input Voltage",
        bg="white",
        font=("Arial",11,"bold")
    ).grid(row=0, column=3, sticky="w", padx=(0,8))

    input_voltage = ttk.Entry(
        top,
        width=10
    )

    input_voltage.grid(
        row=0,
        column=4,
        sticky="w"
    )
    tk.Label(
        top,
        text="V",
        bg="white",
        font=("Arial",11)
   ).grid(row=0, column=5, sticky="w", padx=(5,70))


    # Input Frequency
    tk.Label(
        top,
        text="Input Frequency",
        bg="white",
        font=("Arial",11,"bold")
    ).grid(row=0, column=6, sticky="w", padx=(0,8))

    input_frequency = ttk.Entry(
        top,
        width=10
    )

    input_frequency.grid(
        row=0,
        column=7,
        sticky="w"
    )

    tk.Label(
        top,
        text="Hz",
        bg="white",
        font=("Arial",11)
    ).grid(row=0, column=8, sticky="w", padx=(5,0))

    return {
    "frame": top,
    "dwell_time": dwell_time,
    "input_voltage": input_voltage,
    "input_frequency": input_frequency
}



def regulation_step(parent, title):

    frame = tk.Frame(
        parent,
        bg="white"
    )

    # Column sizes
    frame.grid_columnconfigure(0, minsize=90)
    frame.grid_columnconfigure(1, minsize=70)
    frame.grid_columnconfigure(2, minsize=95)
    frame.grid_columnconfigure(3, minsize=95)

    # ==========================
    # Header Row
    # ==========================

    tk.Label(
        frame,
        bg="white",
        relief="solid",
        bd=1
    ).grid(row=0, column=0, sticky="nsew")

    tk.Label(
        frame,
        bg="white",
        relief="solid",
        bd=1
    ).grid(row=0, column=1, sticky="nsew")

    tk.Label(
        frame,
        text="HV Load (%)",
        bg="#DCEEFF",
        font=("Arial",10,"bold"),
        relief="solid",
        bd=1
    ).grid(row=0, column=2, sticky="nsew")

    tk.Label(
        frame,
        text="Set HV\nCurrent (A)",
        bg="#DCEEFF",
        font=("Arial",10,"bold"),
        relief="solid",
        bd=1
    ).grid(row=0, column=3, sticky="nsew")

    # ==========================
    # Left merged cell
    # ==========================

    tk.Label(
        frame,
        text=title,
        bg="#DCEEFF",
        font=("Arial",12),
        justify="center",
        relief="solid",
        bd=1
    ).grid(
        row=1,
        column=0,
        rowspan=5,
        sticky="nsew"
    )

    # ==========================
    # Middle merged Entry
    # ==========================

    entry_frame = tk.Frame(
        frame,
        bg="#DCEEFF",
        relief="solid",
        bd=1
    )

    entry_frame.grid(
        row=1,
        column=1,
        rowspan=5,
        sticky="nsew"
    )

    step_voltage = ttk.Entry(
    entry_frame,
    justify="center"
    )

    step_voltage.pack(
        fill="both",
        expand=True,
        padx=1,
        pady=1
    )

    # ==========================
    # Right side rows
    # ==========================

    loads = [
        "No Load",
        "25",
        "50",
        "75",
        "100"
    ]
    entries = {}

    for i, value in enumerate(loads):

        tk.Label(
            frame,
            text=value,
            bg="#DCEEFF",
            relief="solid",
            bd=1
        ).grid(
            row=i+1,
            column=2,
            sticky="nsew"
        )

        eframe = tk.Frame(
            frame,
            bg="#DCEEFF",
            relief="solid",
            bd=1
        )

        eframe.grid(
            row=i+1,
            column=3,
            sticky="nsew"
        )

        entry = ttk.Entry(
            eframe,
            justify="center"
        )

        entry.pack(
            fill="both",
            expand=True,
            padx=1,
            pady=1
        )

        entries[value] = entry

    # RETURN AFTER THE LOOP
    return {
        "frame": frame,
        "step_voltage": step_voltage,
        "load_entries": entries
        
    }


def load_regulation_panel(parent, title):

    panel = tk.Frame(parent, bg="white")

    tk.Label(
        panel,
        text=title,
        bg="white",
        font=("Arial",13,"bold")
    ).pack(
        anchor="center",
        pady=(0,18)
    )


    steps = {}

    for i in range(1,4):

        step = regulation_step(
            panel,
            f"Step {i}\nHV\nVoltage"
        )

        step["frame"].pack(
            pady=12
        )

        steps[f"step{i}"] = step

    return {
        "panel": panel,
        "steps": steps
    }