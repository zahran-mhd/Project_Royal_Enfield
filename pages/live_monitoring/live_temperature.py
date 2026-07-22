import tkinter as tk

from widgets.channel_frame import ChannelFrame
from controllers.live_temp_controller import LiveTempController


class LiveTemperatureFrame(tk.Frame):

    def __init__(self, parent, context):

        super().__init__(
            parent,
            bg="white"
        )

        self.context = context

        # --------------------------------
        # Controller
        # --------------------------------
        self.controller = LiveTempController(
            self,
            self.context
        )

        # --------------------------------
        # Grid Configuration
        # --------------------------------
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.grid_rowconfigure(0, weight=0)
        self.grid_rowconfigure(1, weight=1)

        # --------------------------------
        # Image Section
        # --------------------------------
        self.image_frame = tk.Frame(
            self,
            bg="white"
        )

        self.image_frame.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="n",
            pady=15
        )

        self.image_frame.grid_columnconfigure(
            0,
            weight=1
        )

        self.image_frame.grid_columnconfigure(
            1,
            weight=1
        )

        # --------------------------------
        # Create DUT Cards
        # --------------------------------
        dut_names = [
            "DUT1",
            "DUT2",
            "DUT3",
            "DUT4"
        ]

        positions = [
            (0, 0),
            (0, 1),
            (1, 0),
            (1, 1)
        ]

        for name, (row, column) in zip(
            dut_names,
            positions
        ):

            self.create_dut_card(
                self.image_frame,
                name,
                row,
                column
            )

        # --------------------------------
        # Create Channel Section
        # --------------------------------
        self.create_channel_section()

        # --------------------------------
        # Start Temperature Updates
        # --------------------------------
        self.controller.start_monitoring()

    # =====================================================
    # Create DUT Card
    # =====================================================
    def create_dut_card(
        self,
        parent,
        name,
        row,
        column
    ):

        card = tk.Frame(
            parent,
            bg="white"
        )

        card.grid(
            row=row,
            column=column,
            padx=20,
            pady=15
        )

        # --------------------------------
        # DUT Name
        # --------------------------------
        tk.Label(
            card,
            text=name,
            font=("Segoe UI", 15, "bold"),
            bg="white"
        ).pack(
            pady=(0, 2)
        )

        # --------------------------------
        # Canvas
        # --------------------------------
        canvas = tk.Canvas(
            card,
            width=1400,
            height=150,
            bg="white",
            highlightthickness=0
        )

        canvas.pack()

        # --------------------------------
        # Image Position
        # --------------------------------
        img_x = self.controller.img_x

        if name in ("DUT3", "DUT4"):
            img_x += 15

        # --------------------------------
        # Display Image
        # --------------------------------
        canvas.create_image(
            img_x,
            self.controller.img_y,
            image=self.controller.temp_image,
            anchor="nw"
        )

        # --------------------------------
        # Store Canvas
        # --------------------------------
        self.controller.canvases[name] = canvas

        self.controller.temp_labels[name] = []

        # --------------------------------
        # Create Temperature Labels
        # --------------------------------
        self.controller.create_temp_labels(
            canvas,
            self.controller.temp_labels[name]
        )

    # =====================================================
    # Create Channel Section
    # =====================================================
    def create_channel_section(self):

        channels = (
            self.context
            .channel_repository
            .get_all_channels()
        )

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

            self.channel_frames.append(
                channel_frame
            )

            self.channel_map[channel_id] = (
                channel_frame
            )