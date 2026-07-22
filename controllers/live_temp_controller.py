import random
from pathlib import Path

from PIL import Image, ImageTk


class LiveTempController:

    def __init__(self, view, context):

        self.view = view
        self.context = context

        self.img_x = 65
        self.img_y = 25

        self.img_w = 620
        self.img_h = 100

        self.canvases = {}
        self.temp_labels = {}

        self.load_image()

    # =====================================================
    # Load Image
    # =====================================================
    def load_image(self):

        base_dir = Path(__file__).resolve().parents[1]

        image_path = base_dir / "assets" / "OBC.jpg"

        image = Image.open(image_path)

        image = image.resize(
            (
                self.img_w,
                self.img_h
            ),
            Image.Resampling.LANCZOS
        )

        self.temp_image = ImageTk.PhotoImage(image)

    # =====================================================
    # Create Temperature Labels
    # =====================================================
    def create_temp_labels(
        self,
        canvas,
        label_list
    ):

        positions = [

            # Top
            (
                self.img_x + 100,
                self.img_y - 12
            ),

            (
                self.img_x + 310,
                self.img_y - 12
            ),

            (
                self.img_x + 520,
                self.img_y - 12
            ),

            # Right
            (
                self.img_x + self.img_w + 35,
                self.img_y + 25
            ),

            (
                self.img_x + self.img_w + 35,
                self.img_y + 75
            ),

            # Bottom
            (
                self.img_x + 100,
                self.img_y + self.img_h + 15
            ),

            (
                self.img_x + 310,
                self.img_y + self.img_h + 15
            ),

            (
                self.img_x + 520,
                self.img_y + self.img_h + 15
            ),

            # Left
            (
                self.img_x - 35,
                self.img_y + 25
            ),

            (
                self.img_x - 30,
                self.img_y + 65
            )
        ]

        for i, (x, y) in enumerate(positions):

            label_id = canvas.create_text(
                x,
                y,
                text=f"T{i + 1}: 0°C",
                font=("Arial", 10, "bold"),
                fill="blue"
            )

            label_list.append(label_id)

    # =====================================================
    # Update Temperatures
    # =====================================================
    def update_temperatures(self):

        for dut_name, canvas in self.canvases.items():

            for i, label_id in enumerate(
                self.temp_labels[dut_name]
            ):

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
                    label_id,
                    text=f"T{i + 1}: {temp}°C",
                    fill=color
                )

        self.view.after(
            3000,
            self.update_temperatures
        )

    # =====================================================
    # Start Monitoring
    # =====================================================
    def start_monitoring(self):

        self.update_temperatures()