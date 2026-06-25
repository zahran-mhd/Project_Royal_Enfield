import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from tkinter import ttk


class FormPopup:

    def __init__(self, parent, title, fields, on_save, prefill=None, dropdowns=None):
        self.parent = parent
        self.fields = fields
        self.on_save = on_save
        self.prefill = prefill
        self.dropdowns = dropdowns or {}

        self.entries = {}

        # Create popup hidden
        self.popup = tk.Toplevel(parent)
        self.popup.withdraw()
        # Start invisible
        self.popup.attributes("-alpha", 0.0)
        self.popup.title(title)
        self.popup.configure(bg="#f4f6f9")
        self.popup.resizable(False, False)

        self.build_form()

        # Calculate required size
        self.popup.update_idletasks()

        width = max(500, self.popup.winfo_reqwidth())
        height = max(350, self.popup.winfo_reqheight())

        x = (self.popup.winfo_screenwidth() - width) // 2
        y = (self.popup.winfo_screenheight() - height) // 2

        self.popup.geometry(f"{width}x{height}+{x}+{y}")

        # Show popup
        self.popup.deiconify()
        self.popup.transient(parent)
        self.popup.grab_set()
        
                # Smooth fade-in
        self.fade_in()
        
    def fade_in(self, alpha=0.0):
        alpha += 0.1

        if alpha <= 1.0:
            self.popup.attributes("-alpha", alpha)
            self.popup.after(20, lambda: self.fade_in(alpha))
    def fade_out(self, alpha=1.0):
        alpha -= 0.1

        if alpha > 0:
            self.popup.attributes("-alpha", alpha)
            self.popup.after(20, lambda: self.fade_out(alpha))
        else:
            self.popup.destroy()
    def build_form(self):

        # Main card
        card = tk.Frame(
            self.popup,
            bg="white",
            bd=1,
            relief="solid"
        )
        card.pack(fill="both", expand=True, padx=20, pady=20)

        # Title
        tk.Label(
            card,
            text="",
            font=("Segoe UI", 14, "bold"),
            bg="white",
            fg="#1f2937"
        ).pack(pady=(15, 20))

        # Form Area
        form_frame = tk.Frame(card, bg="white")
        form_frame.pack(fill="x", padx=30)

        for i, label in enumerate(self.fields):

            tk.Label(
                form_frame,
                text=label,
                font=("Segoe UI", 10),
                bg="white"
            ).grid(
                row=i,
                column=0,
                sticky="w",
                pady=8
            )

            if label in self.dropdowns:

                entry = ttk.Combobox(
                    form_frame,
                    values=self.dropdowns[label],
                    state="readonly",
                    width=29
                )

                if self.dropdowns[label]:
                    entry.current(0)

            elif "date" in label.lower():

                entry = DateEntry(
                    form_frame,
                    width=28,
                    date_pattern="yyyy-mm-dd",
                    font=("Segoe UI", 10)
                )

            else:

                entry = tk.Entry(
                    form_frame,
                    width=32,
                    font=("Segoe UI", 10)
                )

            entry.grid(
                row=i,
                column=1,
                padx=(20, 0),
                pady=8,
                sticky="w"
            )

            self.entries[label] = entry

            if self.prefill:

                if isinstance(entry, DateEntry):
                    entry.set_date(self.prefill[i])

                elif isinstance(entry, ttk.Combobox):
                    entry.set(self.prefill[i])

                else:
                    entry.insert(0, self.prefill[i])

        # Button Frame
        btn_frame = tk.Frame(card, bg="white")
        btn_frame.pack(pady=25)

        tk.Button(
            btn_frame,
            text="Save",
            width=12,
            bg="#16a34a",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.save
        ).pack(side="left", padx=10)

        tk.Button(
            btn_frame,
            text="Cancel",
            width=12,
            bg="#dc2626",
            fg="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.popup.destroy
        ).pack(side="left", padx=10)

    def save(self):
        try:
            values = [self.entries[field].get() for field in self.fields]

            if any(not value.strip() for value in values):
                messagebox.showwarning(
                    "Warning",
                    "All fields are required"
                )
                return

            self.on_save(values)

            self.popup.destroy()

        except Exception as e:
            messagebox.showerror("Error", str(e))
            print("Save Error:", e)
        
   