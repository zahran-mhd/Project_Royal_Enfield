from dataclasses import dataclass

@dataclass
class InstrumentData:

    instrument_id: int = None

    sno: int = 0

    instrument_name: str = ""

    # New fields
    instrument_type_id: int = None

    instrument_type: str = ""

    driver_class: str = ""

    worker_class: str = ""

    # Existing fields
    address: str = ""

    instrument_sno: str = ""

    calibration_due_date: str = ""

    status: int = 0

    is_locked: int = 0

    channel_id: int = None

    is_shared: int = 0