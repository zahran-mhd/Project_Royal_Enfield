# import tkinter as tk


# class RegulationTable(tk.Frame):

#     def __init__(
#         self,
#         parent,
#         columns,
#         row_values
#     ):

#         super().__init__(
#             parent,
#             bg="white"
#         )

#         self.columns = columns
#         self.row_values = row_values

#         self.create_table()

#     # --------------------------------------------------
#     # CREATE TABLE
#     # --------------------------------------------------

#     def create_table(self):

#         # --------------------------------------------------
#         # TABLE HEADERS
#         # --------------------------------------------------

#         for column_index, column_name in enumerate(
#             self.columns
#         ):

#             header = tk.Label(
#                 self,
#                 text=column_name,
#                 font=("Bookman Antiqua", 9, "bold"),
#                 fg="white",
#                 bg="#1F3F68",
#                 wraplength=130,
#                 justify="center",
#                 height=3,
#                 relief="solid",
#                 borderwidth=1
#             )

#             header.grid(
#                 row=0,
#                 column=column_index,
#                 sticky="nsew"
#             )

#             self.grid_columnconfigure(
#                 column_index,
#                 weight=1
#             )


#         # --------------------------------------------------
#         # DATA ROWS
#         # --------------------------------------------------

#         for row_index, row_data in enumerate(
#             self.row_values,
#             start=1
#         ):

#             # Exclude the last column
#             # because regulation is one merged cell

#             for column_index in range(
#                 len(self.columns) - 1
#             ):

#                 cell_value = ""

#                 if column_index < len(row_data):

#                     cell_value = row_data[column_index]

#                 cell = tk.Label(
#                     self,
#                     text=cell_value,
#                     font=("Bookman Antiqua", 9),
#                     bg="white",
#                     fg="#1F3F68",
#                     relief="solid",
#                     borderwidth=1
#                 )

#                 cell.grid(
#                     row=row_index,
#                     column=column_index,
#                     sticky="nsew"
#                 )


#         # --------------------------------------------------
#         # MERGED REGULATION CELL
#         # --------------------------------------------------

#         regulation_cell = tk.Label(
#             self,
#             text="",
#             font=("Bookman Antiqua", 10, "bold"),
#             bg="white",
#             fg="#1F3F68",
#             relief="solid",
#             borderwidth=1
#         )

#         regulation_cell.grid(
#             row=1,
#             column=len(self.columns) - 1,
#             rowspan=len(self.row_values),
#             sticky="nsew"
#         )
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

        # Store all cell widgets
        self.cells = {}

        # Store merged regulation cell
        self.regulation_cell = None

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
                font=("Bookman Antiqua", 9, "bold"),
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

            # Exclude last column
            # because regulation is merged

            for column_index in range(
                len(self.columns) - 1
            ):

                cell_value = ""

                if column_index < len(row_data):

                    cell_value = row_data[column_index]

                cell = tk.Label(
                    self,
                    text=cell_value,
                    font=("Bookman Antiqua", 9),
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

                # ------------------------------------------
                # STORE CELL
                # ------------------------------------------

                self.cells[
                    (row_index - 1, column_index)
                ] = cell

        # --------------------------------------------------
        # MERGED REGULATION CELL
        # --------------------------------------------------

        self.regulation_cell = tk.Label(
            self,
            text="",
            font=("Bookman Antiqua", 10, "bold"),
            bg="white",
            fg="#1F3F68",
            relief="solid",
            borderwidth=1
        )

        self.regulation_cell.grid(
            row=1,
            column=len(self.columns) - 1,
            rowspan=len(self.row_values),
            sticky="nsew"
        )

    # ==================================================
    # UPDATE CELL
    # ==================================================

    def update_cell(
        self,
        row,
        column,
        value
    ):

        # ----------------------------------------------
        # Allow column name
        # ----------------------------------------------

        if isinstance(column, str):

            if column not in self.columns:

                print(
                    f"Unknown column: {column}"
                )

                return

            column_index = self.columns.index(
                column
            )

        else:

            column_index = column

        # ----------------------------------------------
        # Regulation column
        # ----------------------------------------------

        if column_index == len(self.columns) - 1:

            self.regulation_cell.config(
                text="" if value is None else str(value)
            )

            return

        # ----------------------------------------------
        # Normal cell
        # ----------------------------------------------

        cell = self.cells.get(
            (row, column_index)
        )

        if cell is None:

            print(
                f"Cell not found: "
                f"row={row}, "
                f"column={column}"
            )

            return

        cell.config(
            text="" if value is None else str(value)
        )

    # ==================================================
    # UPDATE ROW
    # ==================================================

    def update_row(
        self,
        row,
        values
    ):

        for column, value in values.items():

            self.update_cell(
                row=row,
                column=column,
                value=value
            )

    # ==================================================
    # CLEAR TABLE
    # ==================================================

    def clear(self):

        for cell in self.cells.values():

            cell.config(
                text=""
            )

        if self.regulation_cell:

            self.regulation_cell.config(
                text=""
            )