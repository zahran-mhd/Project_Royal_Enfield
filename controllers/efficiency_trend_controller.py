class EfficiencyTrendController:

    def __init__(self, view, context):

        self.view = view
        self.context = context

        self.running_duts = []

    def start_live_plot(self, selected_duts):

        # Add newly started DUTs
        for dut in selected_duts:

            if dut not in self.running_duts:
                self.running_duts.append(dut)

        selected_duts = self.running_duts

        # Hide all canvases
        for canvas in self.view.canvas_map.values():
            canvas.grid_forget()

        count = len(selected_duts)

        if count == 0:
            return

        # Reset grid configuration
        for row in range(2):
            self.view.plot_frame.grid_rowconfigure(
                row,
                weight=1
            )

        for column in range(2):
            self.view.plot_frame.grid_columnconfigure(
                column,
                weight=1
            )

        # =========================
        # DUT POSITIONS
        # =========================

        if count == 1:

            positions = [
                (0, 0)
            ]

            self.view.plot_frame.grid_columnconfigure(
                1,
                weight=0
            )

        elif count == 2:

            positions = [
                (0, 0),
                (1, 0)
            ]

            self.view.plot_frame.grid_columnconfigure(
                1,
                weight=0
            )

        elif count == 3:

            positions = [
                (0, 0),
                (1, 0),
                (0, 1)
            ]

        else:

            positions = [
                (0, 0),
                (1, 0),
                (0, 1),
                (1, 1)
            ]

        # =========================
        # PLACE CANVASES
        # =========================

        for dut, (row, column) in zip(
            selected_duts,
            positions
        ):

            canvas = self.view.canvas_map[dut]

            canvas.grid(
                row=row,
                column=column,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            # Update title
            canvas.delete("title")

            canvas.create_text(
                10,
                10,
                text=f"{dut}",
                anchor="nw",
                font=("Segoe UI", 12, "bold"),
                fill="black",
                tags="title"
            )

            # Test data
            canvas.add_charging_points(88.2)
            canvas.add_charging_points(89.5)
            canvas.add_charging_points(90.8)

            canvas.add_discharging_points(91.3)
            canvas.add_discharging_points(89.7)
            canvas.add_discharging_points(87.5)