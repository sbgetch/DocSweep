from dataclasses import dataclass
from models.site import Site


@dataclass
class SearchResult:
    site: Site
    found: bool
    message: str = ""
