import tkinter as tk
from tkinter import ttk, messagebox


class DeleteDutPopup:

    def __init__(self, parent, duts, on_delete):

        self.on_delete = on_delete
        self.variables = {}

        self.popup = tk.Toplevel(parent)
        self.popup.title("Delete DUT")
        self.popup.geometry("350x400")
        self.popup.transient(parent)
        self.popup.grab_set()

        tk.Label(
            self.popup,
            text="Select DUT(s) to Delete",
            font=("Bookman Antiqua", 13, "bold")
        ).pack(pady=10)

        frame = tk.Frame(self.popup)
        frame.pack(fill="both", expand=True, padx=15)

        for dut in duts:

            var = tk.BooleanVar()

            cb = tk.Checkbutton(
                frame,
                text=dut["dut_name"],
                variable=var
            )

            cb.pack(anchor="w", pady=3)

            self.variables[dut["dut_id"]] = var

        button_frame = tk.Frame(self.popup)
        button_frame.pack(pady=15)

        tk.Button(
            button_frame,
            text="Delete",
            bg="red",
            fg="white",
            width=12,
            command=self.delete
        ).pack(side="left", padx=10)

        tk.Button(
            button_frame,
            text="Cancel",
            width=12,
            command=self.popup.destroy
        ).pack(side="left")


    def delete(self):

        selected = [
            dut_id
            for dut_id, var in self.variables.items()
            if var.get()
        ]

        if not selected:

            messagebox.showwarning(
                "Warning",
                "Please select at least one DUT."
            )
            return

        if not messagebox.askyesno(
            "Confirm",
            "Delete selected DUT(s)?"
        ):
            return

        self.on_delete(selected)

        self.popup.destroy()