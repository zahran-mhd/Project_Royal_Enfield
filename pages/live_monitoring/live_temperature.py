import tkinter as tk
from pathlib import Path
from PIL import Image, ImageTk
import random

from widgets.channel_frame import ChannelFrame


class LiveTemperatureFrame(tk.Frame):

    def __init__(self, parent, context):
        super().__init__(parent, bg="white")

        self.context = context

        # -----------------------------
        # Grid Configuration
        # -----------------------------
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # -----------------------------
        # Image properties
        # -----------------------------
        self.img_x = 65
        self.img_y = 25
        self.img_w = 620
        self.img_h = 100

        # Store canvases & labels
        self.canvases = {}
        self.temp_labels = {}

        self.load_image()

        # -----------------------------
        # Image Section
        # -----------------------------
        self.image_frame = tk.Frame(self, bg="white")
        self.image_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="n",
            pady=15
        )

        self.image_frame.grid_columnconfigure(0, weight=1)
        self.image_frame.grid_columnconfigure(1, weight=1)

        dut_names = [
            "DUT1",
            "DUT2",
            "DUT3",
            "DUT4"
        ]

        positions = [
            (0, 0),
            (1, 0),
            (0, 1),
            (1, 1)
        ]

        for name, (r, c) in zip(dut_names, positions):
            self.create_dut_card(
                self.image_frame,
                name,
                r,
                c
            )

        # Create Channel Frames
        self.create_channel_section()

        # Start temperature updates
        self.update_temperatures()

    # =====================================================
    # Load Image
    # =====================================================
    def load_image(self):

        base_dir = Path(__file__).resolve().parents[2]

        image_path = base_dir / "assets" / "OBC.jpg"

        image = Image.open(image_path)

        image = image.resize(
            (self.img_w, self.img_h),
            Image.Resampling.LANCZOS
        )

        self.temp_image = ImageTk.PhotoImage(image)

    # =====================================================
    # Create DUT Card
    # =====================================================
    def create_dut_card(self, parent, name, row, column):

        card = tk.Frame(parent, bg="white")

        card.grid(
            row=row,
            column=column,
            padx=20,
            pady=15
        )

        tk.Label(
            card,
            text=name,
            font=("Segoe UI", 15, "bold"),
            bg="white"
        ).pack(pady=(0, 2))

        canvas = tk.Canvas(
            card,
            width=1400,
            height=150,
            bg="white",
            highlightthickness=0
        )

        canvas.pack()
        
                # Move only DUT3 and DUT4 to the right
        img_x = self.img_x

        if name in ("DUT3", "DUT4"):
            img_x += 15      # Move right by 15 pixels

        canvas.create_image(
            self.img_x,
            self.img_y,
            image=self.temp_image,
            anchor="nw"
        )

        self.canvases[name] = canvas
        self.temp_labels[name] = []

        self.create_temp_labels(
            canvas,
            self.temp_labels[name]
        )

    # =====================================================
    # Create Temperature Labels
    # =====================================================
    def create_temp_labels(self, canvas, label_list):

        positions = [

    # ---------------- Top ----------------
    (self.img_x + 100, self.img_y - 12),   # T1
    (self.img_x + 310, self.img_y - 12),   # T2
    (self.img_x + 520, self.img_y - 12),   # T3

    # ---------------- Right ----------------
    (self.img_x + self.img_w + 35, self.img_y + 25),    # T4
    (self.img_x + self.img_w + 35, self.img_y + 75),    # T5

    # ---------------- Bottom ----------------
    (self.img_x + 100, self.img_y + self.img_h + 15),  # T6
    (self.img_x + 310, self.img_y + self.img_h + 15),  # T7
    (self.img_x + 520, self.img_y + self.img_h + 15),  # T8

    # ---------------- Left ----------------
    (self.img_x - 35, self.img_y + 25),    # T9
    (self.img_x - 30, self.img_y + 65),    # T10
]
        for i, (x, y) in enumerate(positions):

            lbl = canvas.create_text(
                x,
                y,
                text=f"T{i+1}: 0°C",
                font=("Arial", 10, "bold"),
                fill="blue"
            )

            label_list.append(lbl)

    # =====================================================
    # Update Temperatures
    # =====================================================
    def update_temperatures(self):

        for dut_name, canvas in self.canvases.items():

            for i, lbl in enumerate(self.temp_labels[dut_name]):

                temp = round(
                    random.uniform(20, 80),
                    1
                )

                if temp > 60:
                    color = "red"
                elif temp > 40:
                    color = "orange"
                else:
                    color = "green"

                canvas.itemconfig(
                    lbl,
                    text=f"T{i+1}: {temp}°C",
                    fill=color
                )

        self.after(
            3000,
            self.update_temperatures
        )
        
        
        # =====================================================
    # Create Channel Section
    # =====================================================
    def create_channel_section(self):

        channels = self.context.channel_repository.get_all_channels()

        self.channel_frames = []
        self.channel_map = {}

        for index, channel in enumerate(channels):

            channel_id = channel["ChannelID"]

            channel_frame = ChannelFrame(
                self,
                channel_name=channel["ChannelName"],
                dut_names=[
                    f"DUT{2 * channel_id - 1}",
                    f"DUT{2 * channel_id}"
                ]
            )

            channel_frame.grid(
                row=1,
                column=index,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            self.channel_frames.append(channel_frame)
            self.channel_map[channel_id] = channel_frame