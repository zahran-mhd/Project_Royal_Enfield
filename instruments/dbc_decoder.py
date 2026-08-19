"""
dbc_decoder.py

Loads a DBC file and decodes CAN messages using cantools.
"""

import cantools

# Parameters to monitor
WATCH_PARAMETERS = {

            0x19F:[ "Chrgr_Output_DC_Curr",
                    "Chrgr_Output_DC_Vlt",
                    "Chrgr_Input_AC_Curr",
                    "Chrgr_Input_AC_Vlt"
                ],
            0x50F:[ "HP_DCDC_Output_DC_Curr",
                    "HP_DCDC_Output_DC_Vlt",
                    "HP_DCDC_Input_DC_Curr",
                    "HP_DCDC_Input_DC_Vlt"
                ],
            0x1A7:[ "OBC_temp",
                    "OBC_FET_Temp",
                    "HPDCDC_Temp"
                ],
            0x50E:[ "OBC_Input_AC_under_Vlt",
                    "OBC_Output_Under_Vlt_Flt",
                    "OBC_Input_AC_Over_Vlt",
                    "OBC_Output_Over_Vlt_Flt",
                    "DCDC_Input_Under_Vlt",
                    "DCDC_Output_Under_Vlt_Flt",
                    "DCDC_Input_Over_Vlt",
                    "DCDC_Output_Over_Vlt_Flt",
                    "OBC_Input_Over_Curr",
                    "OBC_Output_Over_Curr",
                    "OBC_Output_Shrt_Ckt_Fail",
                    "DCDC_Input_Over_Curr",
                    "DCDC_Output_Over_Curr",
                    "DCDC_Output_Shrt_Ckt"
                ],

            # 0x50E: [
            #         "OBC_Input_AC_Over_Vlt",
            #         "OBC_Input_AC_under_Vlt",
            #         "OBC_Input_Over_Curr",
            #         "OBC_High_Temp",
            #         "OBC_Low_temp",
            #         "OBC_Temp_Snsr_Fail",
            #         "OBC_Curr_Sensing_Fail",
            #         "OBC_Contactor_or_Relay_Fail",
            #         "OBC_Output_Open_Ckt",
            #         "OBC_Output_Shrt_Ckt_Fail",
            #         "OBC_Output_Over_Vlt_Flt",
            #         "OBC_Output_Under_Vlt_Flt",

            #         "DCDC_Output_Over_Vlt_Flt",
            #         "DCDC_Input_Over_Vlt",
            #         "DCDC_Input_Under_Vlt",
            #         "DCDC_Input_Over_Curr",
            #         "DCDC_Output_Over_Curr",
            #         "DCDC_High_Temp",
            #         "DCDC_Low_Temp",
            #         "DCDC_Temp_Snsr_Fail",
            #         "DC_DC_Curr_Sensing_Fail",
            #         "DCDC_Contactor_or_Relay_Fail",
            #         "DCDC_Output_Open_Ckt",
            #         "DCDC_Output_Shrt_Ckt",
            #         "DCDC_Output_Under_Vlt_Flt"
            #     ],
            0x020:[ "CAN_Rx_Error_Counter"
                ]
        }
class DBCDecoder:

    def __init__(self):
        self.db = None
        self.dbc_file = None
        # Parameters to monitor

    # -------------------------------------------------
    # Load DBC
    # -------------------------------------------------

    def load_dbc(self, filename):
        """
        Load a DBC file.

        Parameters
        ----------
        filename : str
            Path to .dbc file

        Returns
        -------
        bool
            True if loaded successfully
        """

        try:
            self.db = cantools.database.load_file(filename)
            self.dbc_file = filename

            print(f"DBC Loaded : {filename}")

            return True

        except Exception as e:

            print("Failed to load DBC")
            print(e)

            self.db = None
            return False

    # -------------------------------------------------
    # Check whether DBC is loaded
    # -------------------------------------------------

    def is_loaded(self):

        return self.db is not None

    # -------------------------------------------------
    # Decode CAN frame
    # -------------------------------------------------
    # def decode(self, arbitration_id, data):

    #     if self.db is None:
    #         return None

    #     if arbitration_id not in WATCH_PARAMETERS:
    #         return None

    #     try:

    #         message = self.db.get_message_by_frame_id(arbitration_id)

    #         decoded = message.decode(data)

    #         result = []

    #         for parameter in WATCH_PARAMETERS[arbitration_id]:

    #             if parameter in decoded:
    #                 result.append({

    #                     "parameter": parameter,

    #                     "value": decoded[parameter]

    #                 })

    #         return result

    #     except Exception as e:

    #         print(e)

    #         return None



    def decode(self, arbitration_id, data):

        if self.db is None:
            print("DBC not loaded")
            return None

        if arbitration_id not in WATCH_PARAMETERS:
            # print("ID not watched")
            return None

        try:

            # print("Looking for message...")

            message = self.db.get_message_by_frame_id(arbitration_id)

            # print("Message:", message.name)

            decoded = message.decode(data)

            # print("Decoded:", decoded)

            result = []

            # ==========================================
            # DEBUG 0x50E ALARM FRAME
            # ==========================================
            # if arbitration_id == 0x50E:

            #     print("================================")
            #     print("ALARM FRAME RECEIVED")
            #     print(f"ID   : 0x{arbitration_id:X}")
            #     print(f"DATA : {data.hex()}")

            #     print("DECODED:")

            #     for name, value in decoded.items():
            #         print(f"    {name} = {value}")

            #     print("================================")


            for parameter in WATCH_PARAMETERS[arbitration_id]:

                # print("Checking:", parameter)

                if parameter in decoded:

                    result.append({
                        "parameter": parameter,
                        "value": decoded[parameter]
                    })

                

            # print("Result:", result)

            return result

        except Exception as e:

            print("Decode Error:", e)

            return None


    # def decode(self, arbitration_id, data):
    #
    #     """
    #     Decode CAN frame.
    #
    #     Parameters
    #     ----------
    #     arbitration_id : int
    #
    #     data : bytes
    #
    #     Returns
    #     -------
    #     dict
    #     """
    #
    #     if self.db is None:
    #         return None
    #
    #     try:
    #
    #         message = self.db.get_message_by_frame_id(arbitration_id)
    #
    #         signals = message.decode(data)
    #
    #         return {
    #
    #             "message_name": message.name,
    #
    #             "frame_id": arbitration_id,
    #
    #             "signals": signals
    #
    #         }
    #
    #     except Exception:
    #
    #         return None

    # -------------------------------------------------
    # Get Message Name only
    # -------------------------------------------------

    def get_message_name(self, arbitration_id):

        if self.db is None:
            return None

        try:

            message = self.db.get_message_by_frame_id(arbitration_id)

            return message.name

        except Exception:

            return None

    # -------------------------------------------------
    # Print all messages in DBC
    # -------------------------------------------------

    def print_messages(self):

        if self.db is None:
            return

        # print()

        # print("Messages in DBC")

        # print("-----------------------------------")

        # for msg in self.db.messages:

        #     print(
        #         f"0x{msg.frame_id:03X}"
        #         f"   {msg.name}"
        #     )

    # -------------------------------------------------
    # Print Signals of one message
    # -------------------------------------------------

    def print_signals(self, arbitration_id):

        if self.db is None:
            return

        try:

            msg = self.db.get_message_by_frame_id(arbitration_id)

            # print()

            # print(msg.name)

            # print("-----------------------")

            # for sig in msg.signals:

            #     print(sig.name)

        except Exception:

            pass