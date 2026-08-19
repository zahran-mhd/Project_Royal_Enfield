from models.instrument_data import InstrumentData
from widgets.form_popup import FormPopup
from tkinter import messagebox

class InstrumentController:

    def __init__(self, view, context):
        self.view = view
        self.context = context

        self.instrument_repository = context.instrument_repository
        self.channel_repository = context.channel_repository
        self.selected_channel_id = None

    def initialize(self):

        channels = self.channel_repository.get_all_channels()

        if channels:
            self.selected_channel_id = channels[0]["ChannelID"]

        self.load_instruments()

    def load_instruments(self):

        if not self.selected_channel_id:
            return

        instruments = self.instrument_repository.get_by_channel(
            self.selected_channel_id
        )

        self.view.display_instruments(instruments)

    def set_channel(self, channel_id):

        self.selected_channel_id = channel_id

        self.load_instruments()
        
        
    # def add_data(self):

    #     def save(values):

    #         instrument = InstrumentData(
    #             instrument_name=values[0],
    #             address=values[1],
    #             instrument_sno=values[2],
    #             calibration_due_date=values[3],
    #             # status=values[4],
    #             channel_id=self.selected_channel_id
    #         )

    #         self.instrument_repository.add(instrument)
    #         self.load_instruments()

    #     FormPopup(
    #         self.view,
    #         "Add Instrument",
    #         [
    #             "Instrument Name",
    #             "Address",
    #             "Serial Number",
    #             "Calibration Date"
                
    #         ],
    #         save
    #     )

    def add_data(self):

        instrument_types = self.instrument_repository.get_instrument_types()

        type_map = {
            name: instrument_type_id
            for instrument_type_id, name in instrument_types
        }

        def save(values):

            instrument = InstrumentData(

                instrument_name=values[0],

                instrument_type_id=type_map[values[1]],

                address=values[2],

                instrument_sno=values[3],

                calibration_due_date=values[4],

                channel_id=self.selected_channel_id
            )

            print(instrument)

            self.instrument_repository.add(instrument)

            self.load_instruments()

        FormPopup(

            self.view,

            "Add Instrument",

            [

                "Instrument Name",

                "Instrument Type",

                "Address",

                "Serial Number",

                "Calibration Date"

            ],

            save,

            dropdowns={

                "Instrument Type": list(type_map.keys())

            }

        )
        
    # def delete_instrument(self, instrument_id):

    #     confirm = messagebox.askyesno(
    #         "Delete",
    #         "Are you sure you want to delete this instrument?"
    #     )

    #     if not confirm:
    #         return

    #     self.instrument_repository.delete(instrument_id)
    #     self.load_instruments()

    def delete_instrument(self, key):

        instrument_id, channel_id = key

        confirm = messagebox.askyesno(
            "Delete",
            "Are you sure you want to delete this instrument?"
        )

        if not confirm:
            return

        self.instrument_repository.delete(
            instrument_id,
            channel_id
        )

        self.load_instruments()
    def edit_instrument(self, key):

        instrument_types = self.instrument_repository.get_instrument_types()
        
        type_map = {
            name: instrument_type_id
            for instrument_type_id, name in instrument_types
        }
        instrument_id, channel_id = key
        print("Edit Instrument ID:", instrument_id)

        instrument = self.instrument_repository.get_by_id(instrument_id)
        if instrument:
            print("Channel:", instrument.channel_id)
        if not instrument:
            return

        def save(values):

            updated = InstrumentData(
                instrument_id=instrument.instrument_id,
                instrument_name=values[0],
                address=values[1],
                instrument_sno=values[2],
                calibration_due_date=values[3],
                status=values[4],
                is_locked=instrument.is_locked,
                channel_id=instrument.channel_id,
                is_shared=instrument.is_shared
            )

            self.instrument_repository.update(updated)
            self.load_instruments()

        FormPopup(

            self.view,

            "Edit Instrument",

            [

                "Instrument Name",

                "Instrument Type",

                "Address",

                "Serial Number",

                "Calibration Date"

            ],

            save,

            prefill=[

                instrument.instrument_name,

                instrument.instrument_type,

                instrument.address,

                instrument.instrument_sno,

                instrument.calibration_due_date

            ],

            dropdowns={

                "Instrument Type": list(type_map.keys())

            },

            readonly_fields=[

                "Instrument Type"

            ]
        )