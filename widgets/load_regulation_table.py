import tkinter as tk


class LoadRegulationTable(tk.Frame):

    def __init__(self, parent, title_text, columns):
        super().__init__(parent, bg="#EEF2F7")

        card = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid",
            width=1500,
            height=280
        )

        card.pack(fill="x")
        card.pack_propagate(False)

        tk.Label(
            card,
            text=title_text,
            font=("Bookman Antiqua", 11, "bold"),
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
            font=("Bookman Antiqua", 10, "bold"),
            bg="white"
        ).grid(
            row=1,
            column=0,
            columnspan=len(columns),
            sticky="nsew"
        )

        # Headers
        for col, text in enumerate(columns):

            tk.Label(
                card,
                text=text,
                font=("Bookman Antiqua", 7, "bold"),
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

        for r, (load, current) in enumerate(loads, start=3):

            tk.Label(
                card,
                text=load,
                relief="solid",
                bd=1
            ).grid(
                row=r,
                column=0,
                sticky="nsew"
            )

            tk.Label(
                card,
                text=current,
                relief="solid",
                bd=1
            ).grid(
                row=r,
                column=1,
                sticky="nsew"
            )

            for c in range(2, len(columns)):

                tk.Entry(
                    card,
                    justify="center",
                    width=8,
                    font=("Bookman Antiqua", 8)
                ).grid(
                    row=r,
                    column=c,
                    sticky="nsew"
                )

        last_row = len(loads) + 3

        tk.Label(
            card,
            text="",
            relief="solid",
            bd=1
        ).grid(
            row=last_row,
            column=0,
            columnspan=len(columns)-2,
            sticky="nsew"
        )

        tk.Label(
            card,
            text="Load Regulation",
            font=("Bookman Antiqua", 10, "bold"),
            relief="solid",
            bd=1
        ).grid(
            row=last_row,
            column=len(columns)-2,
            sticky="nsew"
        )

        tk.Entry(card).grid(
            row=last_row,
            column=len(columns)-1,
            sticky="nsew"
        )

        for col in range(len(columns)):
            card.grid_columnconfigure(
                col,
                weight=1,
                uniform="table"
            )