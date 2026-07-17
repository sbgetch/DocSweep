from dataclasses import dataclass


@dataclass
class Document:
    row: int
    control_number: str
    masw: str = ""
    vertiv: str = ""
    asset_library: str = ""
    pd_cloud: str = ""
