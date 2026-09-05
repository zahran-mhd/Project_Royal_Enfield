import os
import glob
import subprocess
import sys
from datetime import datetime

import tkinter as tk
from tkinter import ttk, filedialog
from tkcalendar import DateEntry


# Extensions we treat as "reports"
EXCEL_PATTERNS = ("*.xlsx", "*.xls", "*.xlsm", "*.csv")


class ReportsWidget(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        # ---- state ----
        self.selected_folder = None
        self.all_files = []        
        self.filtered_files = [] 

        # ================= FILTER CARD =================
        filter_frame = tk.Frame(
            self,
            bg="white",
            bd=0
        )
        filter_frame.pack(
            fill="x",
            pady=(10, 20)
        )

        for col in range(3):
            filter_frame.grid_columnconfigure(col, weight=1)

        # Heading
        tk.Label(
            filter_frame,
            text="Filter Options",
            font=("Bookman Antiqua", 15, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=0,
            column=0,
            columnspan=3,
            sticky="w",
            padx=25,
            pady=(20, 10)
        )

        ttk.Separator(
            filter_frame,
            orient="horizontal"
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            padx=25,
            pady=(0, 20)
        )

        # ================= FOLDER SELECT ROW =================
        upload_frame = tk.Frame(
            filter_frame,
            bg="white"
        )
        upload_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="w",
            padx=25,
            pady=(0, 15)
        )

        upload_btn = tk.Button(
            upload_frame,
            text="Select Folder",
            font=("Bookman Antiqua", 10, "bold"),
            bg="#3567E5",
            fg="white",
            activebackground="#2F5DD0",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=14,
            command=lambda: self.select_folder()
        )
        upload_btn.pack(side="left", ipady=6)

        self.upload_file_label = tk.Label(
            upload_frame,
            text="No folder selected",
            font=("Bookman Antiqua", 10),
            bg="white",
            fg="#64748B"
        )
        self.upload_file_label.pack(side="left", padx=(12, 0))

        self.remove_folder_btn = tk.Button(
            upload_frame,
            text="✕",
            font=("Bookman Antiqua", 10, "bold"),
            bg="white",
            fg="#DC2626",
            activebackground="white",
            activeforeground="#B91C1C",
            bd=0,
            cursor="hand2",
            command=lambda: self.clear_folder()
        )

        # Labels
        tk.Label(
            filter_frame,
            text="Report Name",
            font=("Bookman Antiqua", 10, "bold"),
            bg="white",
            fg="#243B64"
        ).grid(
            row=3,
            column=0,
            sticky="w",
            padx=25,
            pady=(0, 6)
        )

        date_label_row = tk.Frame(filter_frame, bg="white")
        date_label_row.grid(
            row=3,
            column=1,
            sticky="w",
            padx=15,
            pady=(0, 6)
        )

        tk.Label(
            date_label_row,
            text="Report Date",
            font=("Bookman Antiqua", 10, "bold"),
            bg="white",
            fg="#243B64"
        ).pack(side="left")

        # tk.Label(
        #     filter_frame,
        #     text="Report Type",
        #     font=("Bookman Antiqua", 10, "bold"),
        #     bg="white",
        #     fg="#243B64"
        # ).grid(
        #     row=2,
        #     column=2,
        #     sticky="w",
        #     padx=15,
        #     pady=(0, 6)
        # )

        self.use_date_filter = tk.BooleanVar(value=False)

        self.report_name = ttk.Entry(
            filter_frame,
            font=("Bookman Antiqua", 10)
        )
        self.report_name.grid(
            row=4,
            column=0,
            sticky="ew",
            padx=25,
            pady=(0, 25)
        )

        self.report_date = DateEntry(
            filter_frame,
            date_pattern="dd-mm-yyyy",
            font=("Bookman Antiqua", 10)
        )
        self.report_date.grid(
            row=4,
            column=1,
            sticky="ew",
            padx=15,
            pady=(0, 25)
        )

        self.report_date.bind("<<DateEntrySelected>>", self.on_date_selected)

        # self.report_type = ttk.Combobox(
        #     filter_frame,
        #     values=["Daily", "Weekly", "Monthly", "Custom"],
        #     state="readonly",
        #     font=("Bookman Antiqua", 10)
        # )

        # self.report_type.set(
        #     "Select report type"
        # )

        # self.report_type.grid(
        #     row=3,
        #     column=2,
        #     sticky="ew",
        #     padx=15,
        #     pady=(0, 25)
        # )

        btn_wrapper = tk.Frame(
            filter_frame,
            bg="white"
        )
        btn_wrapper.grid(
            row=4,
            column=2,
            sticky="w",
            padx=(15, 25),
            pady=(0, 25)
        )

        filter_btn = tk.Button(
            btn_wrapper,
            text="Filter",
            font=("Bookman Antiqua", 10, "bold"),
            bg="#3567E5",
            fg="white",
            activebackground="#2F5DD0",
            activeforeground="white",
            bd=0,
            cursor="hand2",
            width=12,
            command=lambda: self.apply_filters()
        )
        filter_btn.pack(ipady=8)

        clear_btn = tk.Button(
            btn_wrapper,
            text="Clear",
            font=("Bookman Antiqua", 9),
            bg="white",
            fg="#3567E5",
            activebackground="#EEF2F7",
            bd=0,
            cursor="hand2",
            width=12,
            command=lambda: self.clear_filters()
        )
        clear_btn.pack(pady=(6, 0))

        # ================= REPORT CARD =================
        report_frame = tk.Frame(
            self,
            bg="white",
            bd=0
        )

        report_frame.pack(
            fill="both",
            expand=True
        )

        tk.Label(
            report_frame,
            text="Available Reports",
            font=("Bookman Antiqua", 15, "bold"),
            bg="white",
            fg="#243B64"
        ).pack(
            anchor="w",
            padx=20,
            pady=(20, 10)
        )

        ttk.Separator(
            report_frame,
            orient="horizontal"
        ).pack(
            fill="x",
            padx=20,
            pady=(0, 15)
        )

      
        self.list_container = tk.Frame(report_frame, bg="white")
        self.list_container.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=(0, 20)
        )

        self.render_reports([])  

    # ------------------------------------------------------------------
    # Folder selection / scanning
    # ------------------------------------------------------------------
    def select_folder(self):
        folder_path = filedialog.askdirectory(
            title="Select a folder containing Excel reports"
        )

        if not folder_path:
            return

        self.selected_folder = folder_path
        self.upload_file_label.config(
            text=folder_path,
            fg="#243B64"
        )
        self.remove_folder_btn.pack(side="left", padx=(8, 0))

        self.all_files = self._scan_folder(folder_path)
        self.filtered_files = list(self.all_files)
        self.render_reports(self.filtered_files)

    def clear_folder(self):
        self.selected_folder = None
        self.all_files = []
        self.filtered_files = []

        self.upload_file_label.config(
            text="No folder selected",
            fg="#64748B"
        )
        self.remove_folder_btn.pack_forget()

        self.report_name.delete(0, tk.END)
        self.use_date_filter.set(False)
        self.report_date.set_date(datetime.now().date())

        self.render_reports([])

    def _scan_folder(self, folder_path):
        found = []
        for pattern in EXCEL_PATTERNS:
            found.extend(glob.glob(os.path.join(folder_path, pattern)))
        found.sort(key=lambda p: os.path.basename(p).lower())
        return found

    # ------------------------------------------------------------------
    # Filtering
    # ------------------------------------------------------------------
    def on_date_selected(self, event=None):
        self.use_date_filter.set(True)


    def apply_filters(self):
        if not self.all_files:
            self.render_reports([], message="No folder selected yet.")
            return

        try:
            results = list(self.all_files)

            name_query = self.report_name.get().strip().lower()
            if name_query:
                results = [
                    f for f in results
                    if name_query in os.path.basename(f).lower()
                ]

            date_active = self.use_date_filter.get()
            if date_active:
                selected_date = self.report_date.get_date()
                results = [
                    f for f in results
                    if datetime.fromtimestamp(os.path.getmtime(f)).date() == selected_date
                ]

            self.filtered_files = results

            if not results:
                if date_active:
                    msg = "Record not found for the selected date."
                elif name_query:
                    msg = "Record not found for that report name."
                else:
                    msg = "No reports found."
                self.render_reports([], message=msg)
            else:
                self.render_reports(results)

        except Exception as e:
            self.render_reports([], message=f"Could not apply filter: {e}")

    def clear_filters(self):
        self.report_name.delete(0, tk.END)
        self.use_date_filter.set(False)
        self.report_date.set_date(datetime.now().date())
        self.filtered_files = list(self.all_files)

        if self.filtered_files:
            self.render_reports(self.filtered_files)
        else:
            self.render_reports([], message="No reports found.")

    # ------------------------------------------------------------------
    # Rendering the list
    # ------------------------------------------------------------------
    def render_reports(self, files, message="No reports found."):
        for widget in self.list_container.winfo_children():
            widget.destroy()

        if not files:
            empty_box = tk.Frame(self.list_container, bg="#F7F9FC")
            empty_box.pack(fill="x")
            tk.Label(
                empty_box,
                text=message,
                font=("Bookman Antiqua", 11),
                bg="#F7F9FC",
                fg="#334155"
            ).pack(anchor="w", padx=15, pady=15)
            return

        for file_path in files:
            self._add_report_row(file_path)

    def _add_report_row(self, file_path):
        row = tk.Frame(self.list_container, bg="#F7F9FC")
        row.pack(fill="x", pady=(0, 8))

        name = os.path.basename(file_path)
        mtime = datetime.fromtimestamp(os.path.getmtime(file_path)).strftime("%d-%m-%Y")

        name_btn = tk.Button(
            row,
            text=name,
            font=("Bookman Antiqua", 10, "bold"),
            bg="#F7F9FC",
            fg="#3567E5",
            bd=0,
            cursor="hand2",
            anchor="w",
            activebackground="#EEF2F7",
            command=lambda p=file_path: self.open_report(p)
        )
        name_btn.pack(side="left", padx=15, pady=10, fill="x", expand=True)

        tk.Label(
            row,
            text=mtime,
            font=("Bookman Antiqua", 9),
            bg="#F7F9FC",
            fg="#64748B"
        ).pack(side="right", padx=15)

    # ------------------------------------------------------------------
    # Opening a report
    # ------------------------------------------------------------------
    def open_report(self, file_path):
        try:
            if sys.platform.startswith("win"):
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.call(("open", file_path))
            else:
                subprocess.call(("xdg-open", file_path))
        except Exception as e:
            print(f"Could not open file: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Reports")
    root.geometry("900x600")
    widget = ReportsWidget(root)
    widget.pack(fill="both", expand=True, padx=20, pady=20)
    root.mainloop()
