import tkinter as tk
from widgets.channel_frame import ChannelFrame
from widgets.table_widgets import TableWidget


class LiveTableFrame(tk.Frame):
    def __init__(self, parent, context):
        super().__init__(parent, bg="white")
        self.context = context

        # Create card first
        self.card = tk.Frame(
            self,
            bg="white",
            bd=1,
            relief="solid"
        )
        self.card.grid(
            row=0,
            column=0,
            columnspan=2,
            padx=10,
            pady=10,
            sticky="nsew"
        )

        # Now create table
        self.create_table()

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=0)

        channels = self.context.channel_repository.get_all_channels()

        self.channel_frames = []
        self.channel_map = {}

        for index, channel in enumerate(channels):

            
            channel_id = channel["ChannelID"]
            channel_name = channel["ChannelName"]
            dut_names = [
        f"DUT{2 * channel_id - 1}",
        f"DUT{2 * channel_id}"
    ]


            channel_frame = ChannelFrame(
                self,
                channel_name=channel_name,
                dut_names=dut_names)

            channel_frame.grid(
                row=1,
                column=index,
                padx=10,
                pady=10,
                sticky="nsew"
            )

            self.channel_frames.append(channel_frame)
            self.channel_map[channel["ChannelID"]] = channel_frame
            
            
    def create_table(self):

        columns = (
    
            "Parameter",
            "DUT1 Hardware Data",
            "DUT1 CAN Data",
             "DUT2 Hardware Data",
            "DUT2 CAN Data",
             "DUT3 Hardware Data",
            "DUT3 CAN Data",
             "DUT4 Hardware Data",
            "DUT4 CAN Data",
            
        )

        self.table = TableWidget(
    self.card,
    columns,
    height=17,
    style_name="LiveTable.Treeview",
    
)
        
        parameters = [
    "OBC Input Voltag",
    "OBC Input Current",
    "OBC Output Voltage",
    "OBC Output Current",
    "OBC_Input_Power",
    "OBC_Output_Powe",
    "OBC Efficiency",
    "HPDCDC Input Voltage",
    "HPDCDC Input Current",
    "HPDCDC Output Voltage",
    "HPDCDC Output Current",
    "HPDCDC_Input_Powe",
    "HPDCDC_Output_Power",
    "HPDCDC_Efficiency",
    "OBC_TEMP",
    "OBC_FET_TEMP",
    "HPDCDC_TEMP"
]

        for parameter in parameters:
            row = [
                parameter,      # 1st column: Parameter
                "0.00",         # 2nd column: DUT1 Hardware Data
                "",             # 3rd column: DUT1 CAN Data
                "",             # 4th column: DUT2 Hardware Data
                "",             # 5th column: DUT2 CAN Data
                "",             # 6th column: DUT3 Hardware Data
                "",             # 7th column: DUT3 CAN Data
                "",             # 8th column: DUT4 Hardware Data
                ""              # 9th column: DUT4 CAN Data
            ]
            self.table.insert(row)

        self.table.pack(fill="both", expand=True, padx=20, pady=10)
