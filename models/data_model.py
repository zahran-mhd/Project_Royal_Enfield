from dataclasses import dataclass
from dataclasses import field


@dataclass
class DataModel:

    instrument_values: dict = field(
        default_factory=dict
    )