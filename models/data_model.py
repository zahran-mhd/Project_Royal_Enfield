# models/data_model.py

from dataclasses import dataclass, field


@dataclass
class DataModel:

    # Input

    input_voltage: float = 0.0

    input_current: float = 0.0

    input_power: float = 0.0

    # Output

    output_voltage: float = 0.0

    output_current: float = 0.0

    output_power: float = 0.0

    # Efficiency

    efficiency: float = 0.0

    # Temperature

    temp_ch1: float = 0.0

    temp_ch2: float = 0.0

    temp_ch3: float = 0.0

    temp_ch4: float = 0.0

    # Graph Data

    timestamps: list = field(default_factory=list)

    efficiency_points: list = field(default_factory=list)

    temperature_points: list = field(default_factory=list)