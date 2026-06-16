from dataclasses import dataclass

@dataclass
class InstrumentData:

    instrument_id: int = None

    sno: int = 0

    instrument_name: str = ""

    address: str = ""

    instrument_sno: str = ""

    calibration_due_date: str = ""

    status: int = 1

    is_locked: int = 0

    channel_id: int = None

    is_shared: int = 0