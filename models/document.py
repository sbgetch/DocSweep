from dataclasses import dataclass


@dataclass
class Document:

    row: int

    control_number: str

    found: bool = False