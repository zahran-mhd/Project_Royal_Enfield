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
        top = 35
        bottom = height - 40

        # =========================
        # TITLE (FIXED)
        # =========================
        self.create_text(
            width // 2,
            18,
            text=f"{self.channel_name} ({self.dut_name}) - Charging / Discharging Trend",
            font=("Segoe UI", 11, "bold")
        )

        # =========================
        # AXES
        # =========================
        self.create_line(left, bottom, right, bottom, width=2)
        self.create_line(left, top, left, bottom, width=2)
        
          # EMPTY STATE TEXT (NEW)
    # =========================
        if not self.charging_points and not self.discharging_points:

            self.create_text(
                (left + right) // 2,
                (top + bottom) // 2,
                text="No Data Available",
                fill="gray",
                font=("Segoe UI", 12, "italic")
            )
            return

        # =========================
        # GRID (unchanged)
        # =========================
        for i in range(0, 101, 20):
            y = bottom - ((bottom - top) * i / 100)

            self.create_line(left, y, right, y, fill="#e5e7eb")
            self.create_text(left - 18, y, text=str(i), font=("Segoe UI", 8))

        divisions = 6
        for i in range(divisions + 1):
            x = left + (right - left) * i / divisions

            self.create_line(x, top, x, bottom, fill="#e5e7eb")
            self.create_text(x, bottom + 15, text=str(i), font=("Segoe UI", 8))

        # =========================
        # LABELS
        # =========================
        self.create_text(width // 2, height - 15, text="Cycles", font=("Segoe UI", 9))
        self.create_text(18, height // 2, text="Efficiency (%)", angle=90, font=("Segoe UI", 9))

        # =========================
        # SAMPLE LINES
        # =========================
        charging_y = top + (bottom - top) * 0.30
        discharging_y = top + (bottom - top) * 0.70

        self.create_line(left, charging_y, right, charging_y, fill="green", width=3)
        self.create_text(right - 70, charging_y - 10, text="Charging", fill="green", font=("Segoe UI", 9, "bold"))

        self.create_line(left, discharging_y, right, discharging_y, fill="red", width=3)
        self.create_text(right - 85, discharging_y - 10, text="Discharging", fill="red", font=("Segoe UI", 9, "bold"))