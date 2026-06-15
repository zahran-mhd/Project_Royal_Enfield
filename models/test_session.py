# models/test_session.py

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class TestSession:

    # -----------------------------
    # TEST INFORMATION
    # -----------------------------

    test_name: str = ""

    serial_number: str = ""

    operator: str = ""

    # -----------------------------
    # TIMING
    # -----------------------------

    start_time: datetime = None

    end_time: datetime = None

    # -----------------------------
    # EXECUTION
    # -----------------------------

    current_step: str = ""

    total_steps: int = 0

    completed_steps: int = 0

    # -----------------------------
    # RESULT
    # -----------------------------

    verdict: str = "NOT_RUN"

    # -----------------------------
    # MEASUREMENTS
    # -----------------------------

    measurements: dict = field(
        default_factory=dict
    )

    # -----------------------------
    # FAILURES
    # -----------------------------

    failed_steps: list = field(
        default_factory=list
    )