import tkinter as tk


class RegulationTable(tk.Frame):

    def __init__(
        self,
        parent,
        columns,
        row_values
    ):

        super().__init__(
            parent,
            bg="white"
        )

        self.columns = columns
        self.row_values = row_values

        self.create_table()

    # --------------------------------------------------
    # CREATE TABLE
    # --------------------------------------------------

    def create_table(self):

        # --------------------------------------------------
        # TABLE HEADERS
        # --------------------------------------------------

        for column_index, column_name in enumerate(
            self.columns
        ):

            header = tk.Label(
                self,
                text=column_name,
                font=("Arial", 9, "bold"),
                fg="white",
                bg="#1F3F68",
                wraplength=130,
                justify="center",
                height=3,
                relief="solid",
                borderwidth=1
            )

            header.grid(
                row=0,
                column=column_index,
                sticky="nsew"
            )

            self.grid_columnconfigure(
                column_index,
                weight=1
            )


        # --------------------------------------------------
        # DATA ROWS
        # --------------------------------------------------

        for row_index, row_data in enumerate(
            self.row_values,
            start=1
        ):

            # Exclude the last column
            # because regulation is one merged cell

            for column_index in range(
                len(self.columns) - 1
            ):

                cell_value = ""

                if column_index < len(row_data):

                    cell_value = row_data[column_index]

                cell = tk.Label(
                    self,
                    text=cell_value,
                    font=("Arial", 9),
                    bg="white",
                    fg="#1F3F68",
                    relief="solid",
                    borderwidth=1
                )

                cell.grid(
                    row=row_index,
                    column=column_index,
                    sticky="nsew"
                )


        # --------------------------------------------------
        # MERGED REGULATION CELL
        # --------------------------------------------------

        regulation_cell = tk.Label(
            self,
            text="",
            font=("Arial", 10, "bold"),
            bg="white",
            fg="#1F3F68",
            relief="solid",
            borderwidth=1
        )

        regulation_cell.grid(
            row=1,
            column=len(self.columns) - 1,
            rowspan=len(self.row_values),
            sticky="nsew"
        )
