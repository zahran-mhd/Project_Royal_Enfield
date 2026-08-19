# import random
# from pathlib import Path

# from PIL import Image, ImageTk


# class LiveTempController:

#     def __init__(self, view, context):

#         self.view = view
#         self.context = context

#         self.img_x = 95
#         self.img_y = 30

#         self.img_w = 520
#         self.img_h = 100

#         self.canvases = {}
#         self.temp_labels = {}

#         # Store latest temperatures for each DUT
#         self.temperature_values = {
#             1: {},
#             2: {},
#             3: {},
#             4: {}
#         }

#         self.load_image()

#     # =====================================================
#     # Load Image
#     # =====================================================
#     def load_image(self):

#         base_dir = Path(__file__).resolve().parents[1]

#         image_path = base_dir / "assets" / "OBC.jpg"

#         image = Image.open(image_path)

#         image = image.resize(
#             (
#                 self.img_w,
#                 self.img_h
#             ),
#             Image.Resampling.LANCZOS
#         )

#         self.temp_image = ImageTk.PhotoImage(image)

#     # =====================================================
#     # Create Temperature Labels
#     # =====================================================
#     def create_temp_labels(
#         self,
#         canvas,
#         label_list,
#         img_x
#     ):

#         positions = [

#     # Top
#     (img_x + self.img_w * 0.15, self.img_y - 15),
#     (img_x + self.img_w * 0.50, self.img_y - 15),
#     (img_x + self.img_w * 0.85, self.img_y - 15),

#     # Right
#     (img_x + self.img_w + 50, self.img_y + 30),
#     (img_x + self.img_w + 50, self.img_y + 70),

#     # Bottom
#     (img_x + self.img_w * 0.15, self.img_y + self.img_h + 15),
#     (img_x + self.img_w * 0.50, self.img_y + self.img_h + 15),
#     (img_x + self.img_w * 0.85, self.img_y + self.img_h + 15),

#     # Left
#     (img_x - 45, self.img_y + 30),
#     (img_x - 45, self.img_y + 70),
# ]

#         for i, (x, y) in enumerate(positions):

#             label_id = canvas.create_text(
#                 x,
#                 y,
#                 text=f"T{i + 1}: 0°C",
#                 font=("Arial", 8, "bold"),
#                 fill="blue"
#             )

#             label_list.append(label_id)

#     # =====================================================
#     # Update Temperatures
#     # =====================================================
#     def update_temperatures(self):

#         for dut_name, canvas in self.canvases.items():

#             for i, label_id in enumerate(
#                 self.temp_labels[dut_name]
#             ):

#                 temp = round(
#                     random.uniform(20, 80),
#                     1
#                 )

#                 if temp > 60:
#                     color = "red"

#                 elif temp > 40:
#                     color = "orange"

#                 else:
#                     color = "green"

#                 canvas.itemconfig(
#                     label_id,
#                     text=f"T{i + 1}: {temp}°C",
#                     fill=color
#                 )

#         self.view.after(
#             3000,
#             self.update_temperatures
#         )

#     # =====================================================
#     # Start Monitoring
#     # =====================================================
#     def start_monitoring(self):

#         self.update_temperatures()

#     def reset(self, selected_duts):

#         for dut in selected_duts:

#             self.temperature_values[dut] = {}

#         self.view.reset_display(selected_duts)

    
from pathlib import Path

from PIL import Image, ImageTk


class LiveTempController:

    def __init__(self, view, context):

        self.view = view
        self.context = context

        self.img_x = 95
        self.img_y = 30

        self.img_w = 520
        self.img_h = 100

        self.canvases = {}
        self.temp_labels = {}

        # -------------------------------------------------
        # Latest temperatures
        # -------------------------------------------------
        self.temperature_values = {
            1: {},
            2: {},
            3: {},
            4: {}
        }

        # -------------------------------------------------
        # DAQ instrument used for DUT1/DUT2
        # -------------------------------------------------
        self.daq_instrument_id = "DAQ970A_1"

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

        self.temp_image = ImageTk.PhotoImage(
            image
        )

    # =====================================================
    # Create Temperature Labels
    # =====================================================

    def create_temp_labels(
        self,
        canvas,
        label_list,
        img_x
    ):

        positions = [

            # Top
            (
                img_x + self.img_w * 0.15,
                self.img_y - 15
            ),

            (
                img_x + self.img_w * 0.50,
                self.img_y - 15
            ),

            (
                img_x + self.img_w * 0.85,
                self.img_y - 15
            ),

            # Right
            (
                img_x + self.img_w + 50,
                self.img_y + 30
            ),

            (
                img_x + self.img_w + 50,
                self.img_y + 70
            ),

            # Bottom
            (
                img_x + self.img_w * 0.15,
                self.img_y + self.img_h + 15
            ),

            (
                img_x + self.img_w * 0.50,
                self.img_y + self.img_h + 15
            ),

            (
                img_x + self.img_w * 0.85,
                self.img_y + self.img_h + 15
            ),

            # Left
            (
                img_x - 45,
                self.img_y + 30
            ),

            (
                img_x - 45,
                self.img_y + 70
            ),
        ]

        for i, (x, y) in enumerate(positions):

            label_id = canvas.create_text(
                x,
                y,
                text=f"T{i + 1}: --°C",
                font=("Arial", 8, "bold"),
                fill="black"
            )

            label_list.append(
                label_id
            )

    # =====================================================
    # Get DAQ Temperature Data
    # =====================================================

    def get_daq_temperatures(self):

        try:

            instrument_values = (
                self.context
                .data_model
                .instrument_values
            )

            daq_values = instrument_values.get(
                self.daq_instrument_id,
                {}
            )

            return daq_values

        except Exception as ex:

            print(
                f"DAQ temperature read error: {ex}"
            )

            return {}

    # =====================================================
    # Update Temperatures
    # =====================================================

    # def update_temperatures(self):

    #     # -------------------------------------------------
    #     # Get latest DAQ values
    #     # -------------------------------------------------

    #     daq_values = self.get_daq_temperatures()

    #     # -------------------------------------------------
    #     # DUT1 and DUT2
    #     # -------------------------------------------------

    #     dut_mapping = {
    #         "DUT1": 1,
    #         "DUT2": 2
    #     }

    #     for dut_name, dut_number in (
    #         dut_mapping.items()
    #     ):

    #         # ---------------------------------------------
    #         # Get DUT data
    #         # ---------------------------------------------

    #         dut_values = daq_values.get(
    #             dut_name,
    #             {}
    #         )

    #         # ---------------------------------------------
    #         # Store latest values
    #         # ---------------------------------------------

    #         self.temperature_values[
    #             dut_number
    #         ] = dut_values

    #         # ---------------------------------------------
    #         # Get canvas
    #         # ---------------------------------------------

    #         canvas = self.canvases.get(
    #             dut_name
    #         )

    #         if canvas is None:
    #             continue

    #         labels = self.temp_labels.get(
    #             dut_name,
    #             []
    #         )

    #         # ---------------------------------------------
    #         # Update T1 - T10
    #         # ---------------------------------------------

    #         for i, label_id in enumerate(
    #             labels
    #         ):

    #             parameter = f"T{i + 1}"

    #             temp = dut_values.get(
    #                 parameter
    #             )

    #             # -----------------------------------------
    #             # No DAQ value available
    #             # -----------------------------------------

    #             if temp is None:

    #                 canvas.itemconfig(
    #                     label_id,
    #                     text=f"{parameter}: --°C",
    #                     fill="black"
    #                 )

    #                 continue

    #             # -----------------------------------------
    #             # Convert to float
    #             # -----------------------------------------

    #             try:

    #                 temp = float(temp)

    #             except (
    #                 TypeError,
    #                 ValueError
    #             ):

    #                 canvas.itemconfig(
    #                     label_id,
    #                     text=f"{parameter}: --°C",
    #                     fill="black"
    #                 )

    #                 continue

    #             # -----------------------------------------
    #             # Temperature color
    #             # -----------------------------------------

    #             if temp > 60:

    #                 color = "red"

    #             elif temp > 40:

    #                 color = "orange"

    #             else:

    #                 color = "green"

    #             # -----------------------------------------
    #             # Update label
    #             # -----------------------------------------

    #             canvas.itemconfig(
    #                 label_id,
    #                 text=f"{parameter}: {temp:.1f}°C",
    #                 fill=color
    #             )

    #     # -------------------------------------------------
    #     # Schedule next update
    #     # -------------------------------------------------

    #     self.view.after(
    #         1000,
    #         self.update_temperatures
    #     )


    def update_temperatures(self):

        # -------------------------------------------------
        # DAQ values
        # -------------------------------------------------

        instrument_values = (
            getattr(
                self.context.data_model,
                "instrument_values",
                {}
            )
        )

        # -------------------------------------------------
        # Get DAQ970A data
        # -------------------------------------------------

        daq_data = instrument_values.get(
            6,
            {}
        )

        # -------------------------------------------------
        # Update each DUT
        # -------------------------------------------------

        for dut_name, canvas in self.canvases.items():

            dut_data = daq_data.get(
                dut_name,
                {}
            )

            labels = self.temp_labels.get(
                dut_name,
                []
            )

            for i, label_id in enumerate(labels):

                parameter = f"T{i + 1}"

                temp = dut_data.get(
                    parameter
                )

                # -----------------------------------------
                # No DAQ value yet
                # -----------------------------------------

                if temp is None:

                    canvas.itemconfig(
                        label_id,
                        text=f"{parameter}: --°C",
                        fill="black"
                    )

                    continue

                # -----------------------------------------
                # Store latest value
                # -----------------------------------------

                dut_no = int(
                    dut_name.replace(
                        "DUT",
                        ""
                    )
                )

                self.temperature_values[
                    dut_no
                ][parameter] = temp

                # -----------------------------------------
                # Temperature color
                # -----------------------------------------

                if temp > 60:

                    color = "red"

                elif temp > 40:

                    color = "orange"

                else:

                    color = "green"

                # -----------------------------------------
                # Update GUI
                # -----------------------------------------

                canvas.itemconfig(
                    label_id,
                    text=f"{parameter}: {temp:.1f}°C",
                    fill=color
                )

        # -------------------------------------------------
        # Schedule next update
        # -------------------------------------------------

        self.view.after(
            1000,
            self.update_temperatures
        )
    # =====================================================
    # Start Monitoring
    # =====================================================

    def start_monitoring(self):

        self.update_temperatures()

    # =====================================================
    # Reset
    # =====================================================

    def reset(self, selected_duts):

        for dut in selected_duts:

            self.temperature_values[dut] = {}

        self.view.reset_display(
            selected_duts
        )