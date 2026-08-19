import tkinter as tk


class EfficiencyTrendCanvas(tk.Canvas):

    def __init__(self, parent, dut_name, channel_name, **kwargs):
        super().__init__(
            parent,
            bg="white",
            highlightthickness=1,
            highlightbackground="#d0d7de",
            **kwargs
        )

        # =========================
        # FIXED ATTRIBUTES
        # =========================
        self.dut_name = dut_name
        self.channel_name = channel_name

        self.charging_points = []
        self.discharging_points = []

        self.bind("<Configure>", self.on_resize)
        
        self.after(50, self.draw_graph)

    # =========================
    # RESIZE EVENT
    # =========================
    def on_resize(self, event):
        self.draw_graph()

    # =========================
    # DATA UPDATES
    # =========================
    def add_charging_points(self, value):
        self.charging_points.append(value)
        if len(self.charging_points) > 200:
            self.charging_points.pop(0)
        self.draw_graph()

    def add_discharging_points(self, value):
        self.discharging_points.append(value)
        if len(self.discharging_points) > 200:
            self.discharging_points.pop(0)
        self.draw_graph()

    # =========================
    # DRAW GRAPH
    # =========================
    def draw_graph(self):

        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        if width < 150 or height < 120:
            return

        left = 60
        right = width - 20
        top = 40
        bottom = height - 40

        # --------------------------------------------------
        # Title
        # --------------------------------------------------
        self.create_text(
            width // 2,
            18,
            text=f"{self.channel_name} ({self.dut_name})",
            font=("Segoe UI", 11, "bold")
        )

        # --------------------------------------------------
        # Axes
        # --------------------------------------------------
        self.create_line(left, bottom, right, bottom, width=2)
        self.create_line(left, top, left, bottom, width=2)

        # --------------------------------------------------
        # No Data
        # --------------------------------------------------
        if not self.charging_points and not self.discharging_points:

            self.create_text(
                (left + right) // 2,
                (top + bottom) // 2,
                text="No Data Available",
                fill="gray",
                font=("Segoe UI", 12, "italic")
            )
            return

        # --------------------------------------------------
        # Calculate Y-axis range
        # --------------------------------------------------
        all_values = self.charging_points + self.discharging_points

        min_eff = min(all_values)
        max_eff = max(all_values)

        min_eff = max(0, min_eff - 1)
        max_eff = min(100, max_eff + 1)

        if max_eff == min_eff:
            max_eff += 1
            min_eff -= 1

        # --------------------------------------------------
        # Horizontal grid / Y-axis labels
        # --------------------------------------------------
        grid_lines = 5

        for i in range(grid_lines + 1):

            y = bottom - (bottom - top) * i / grid_lines

            value = min_eff + (max_eff - min_eff) * i / grid_lines

            self.create_line(
                left,
                y,
                right,
                y,
                fill="#e5e7eb"
            )

            self.create_text(
                left - 25,
                y,
                text=f"{value:.1f}",
                font=("Segoe UI", 8)
            )

        # --------------------------------------------------
        # Vertical grid / X-axis labels
        # --------------------------------------------------
        max_cycles = max(
            len(self.charging_points),
            len(self.discharging_points),
            1
        )

        for i in range(max_cycles):

            if max_cycles == 1:
                x = left
            else:
                x = left + (right - left) * i / (max_cycles - 1)

            self.create_line(
                x,
                top,
                x,
                bottom,
                fill="#e5e7eb"
            )

            self.create_text(
                x,
                bottom + 15,
                text=str(i+1),
                font=("Segoe UI", 8)
            )#modify(str(i+1) for 1 index)

        # --------------------------------------------------
        # Axis Labels
        # --------------------------------------------------
        self.create_text(
            width // 2,
            height - 15,
            text="Cycle",
            font=("Segoe UI", 9)
        )

        self.create_text(
            20,
            height // 2,
            text="Efficiency (%)",
            angle=90,
            font=("Segoe UI", 9)
        )

        # --------------------------------------------------
        # Legend
        # --------------------------------------------------
        legend_x = right - 120

        self.create_line(
            legend_x,
            top + 10,
            legend_x + 20,
            top + 10,
            fill="green",
            width=2
        )

        self.create_text(
            legend_x + 25,
            top + 10,
            text="Charging",
            anchor="w",
            font=("Segoe UI", 9)
        )

        self.create_line(
            legend_x,
            top + 28,
            legend_x + 20,
            top + 28,
            fill="red",
            width=2
        )

        self.create_text(
            legend_x + 25,
            top + 28,
            text="Discharging",
            anchor="w",
            font=("Segoe UI", 9)
        )

        # --------------------------------------------------
        # Plot Series
        # --------------------------------------------------
        self.draw_series(
            self.charging_points,
            "green",
            left,
            right,
            top,
            bottom,
            min_eff,
            max_eff
        )

        self.draw_series(
            self.discharging_points,
            "red",
            left,
            right,
            top,
            bottom,
            min_eff,
            max_eff
        )
    def draw_series(
            self,
            values,
            color,
            left,
            right,
            top,
            bottom,
            min_eff,
            max_eff
        ):

        if len(values) == 0:
            return

        if len(values) == 1:
            x = left
            value = values[0]
            y = bottom - (
                (value - min_eff) /
                (max_eff - min_eff)
            ) * (bottom - top)

            self.create_oval(
                x - 4, y - 4,
                x + 4, y + 4,
                fill=color,
                outline=color
            )
            return

        points = []

        for i, value in enumerate(values):

            x = left + (right - left) * i / (len(values) - 1)

            y = bottom - (
                (value - min_eff) /
                (max_eff - min_eff)
            ) * (bottom - top)

            points.extend([x, y])

        self.create_line(
            *points,
            fill=color,
            width=2,
            smooth=False
        )

        for x, y in zip(points[::2], points[1::2]):

            self.create_oval(
                x - 3,
                y - 3,
                x + 3,
                y + 3,
                fill=color,
                outline=color
            )

    def reset(self):

        self.charging_points.clear()
        self.discharging_points.clear()

        self.delete("all")

        self.draw_graph()