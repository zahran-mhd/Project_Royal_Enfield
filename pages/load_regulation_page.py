import tkinter as tk


class LoadRegulationPage(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent, bg="#EEF2F7")

        title = tk.Label(
            self,
            text="OBC Load Regulation",
            font=("Segoe UI", 16, "bold"),
            bg="#EEF2F7",
            fg="#0B1B44"
        )
        title.pack(anchor="w", padx=20, pady=(10, 5))

        self.create_table(
            title_text="OBC Load Regulation - CAN Data",
            columns=[
                "HV\nLoad\n(%)",
                "Set HV\nCurrent\n(A)",
                "Input AC\nVoltage\nCAN (V)",
                "Input AC\nCurrent CAN\n(A)",
                "Input\nPower\nCAN\n(W)",
                "Output\nOBC\nVoltage\nCAN (V)",
                "Output\nOBC\nCurrent\nCAN (A)",
                "Output Power\nCAN (W)",
                "Efficiency CAN\n(%)"
            ]
        )

        self.create_table(
            title_text="OBC Load Regulation - Power Analyser Data",
            columns=[
                "HV\nLoad\n(%)",
                "Set HV\nCurrent\n(A)",
                "Input AC\nVoltage\nPower\nAnalyser (V)",
                "Input AC\nCurrent\nPowerAnalyser\n(A)",
                "Input\nPower\nFactor",
                "Input\nPower\nPower\nAnalyser\n(W)",
                "OBC\nOutput\nVoltage\nPower\nAnalyser\n(V)",
                "OBC Output\nCurrent Power\nAnalyser (A)",
                "OBC Output\nPower Analyser\n(W)",
                "Efficiency\nPower\nAnalyser\n(%)"
            ]
        )

    def create_table(self, title_text, columns):

        card = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
            width=1500,
            height=280
        )

        card.pack(
            pady=(5, 30)
        )

        card.pack_propagate(False)

        tk.Label(
            card,
            text=title_text,
            font=("Segoe UI", 11, "bold"),
            bg="#DCE8D6"
        ).grid(
            row=0,
            column=0,
            columnspan=len(columns),
            sticky="nsew"
        )

        tk.Label(
            card,
            text="HV : 84Vdc",
            font=("Segoe UI", 10, "bold"),
            bg="white"
        ).grid(
            row=1,
            column=0,
            columnspan=len(columns),
            sticky="nsew"
        )

        # Column Headers
        for col, text in enumerate(columns):

            tk.Label(
                card,
                text=text,
                font=("Segoe UI", 7, "bold"),
                bg="#F3F3F3",
                relief="solid",
                bd=1,
                justify="center"
            ).grid(
                row=2,
                column=col,
                sticky="nsew",
                padx=1,
                pady=1
            )

        loads = [
            ("No Load", "0.00"),
            ("25", "6.40"),
            ("50", "12.80"),
            ("75", "19.20"),
            ("100", "25.60")
        ]

        # Data Rows
        for r, (load, current) in enumerate(loads, start=3):

            tk.Label(
                card,
                text=load,
                relief="solid",
                bd=1
            ).grid(
                row=r,
                column=0,
                sticky="nsew",
                padx=1,
                pady=1
            )

            tk.Label(
                card,
                text=current,
                relief="solid",
                bd=1
            ).grid(
                row=r,
                column=1,
                sticky="nsew",
                padx=1,
                pady=1
            )

            for c in range(2, len(columns)):

                entry = tk.Entry(
                    card,
                    justify="center",
                    width=8,
                    font=("Segoe UI", 8)
                )

                entry.grid(
                    row=r,
                    column=c,
                    sticky="nsew",
                    padx=1,
                    pady=1
                )

        # Last Row
        last_row = len(loads) + 3

        tk.Label(
            card,
            text="",
            relief="solid",
            bd=1,
            bg="white"
        ).grid(
            row=last_row,
            column=0,
            columnspan=len(columns)-2,
            sticky="nsew"
        )

        tk.Label(
            card,
            text="Load Regulation",
            font=("Segoe UI", 10, "bold"),
            relief="solid",
            bd=1
        ).grid(
            row=last_row,
            column=len(columns)-2,
            sticky="nsew"
        )

        tk.Entry(
            card
        ).grid(
            row=last_row,
            column=len(columns)-1,
            sticky="nsew"
        )

        # Column Configuration
        for col in range(len(columns)):
            card.grid_columnconfigure(
                col,
                weight=1,
                uniform="table"
            )

        # Row Configuration
        card.grid_rowconfigure(0, minsize=25)
        card.grid_rowconfigure(1, minsize=22)
        card.grid_rowconfigure(2, minsize=32)

        for row in range(3, 8):
            card.grid_rowconfigure(row, minsize=22)

        card.grid_rowconfigure(last_row, minsize=25)