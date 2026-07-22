from dataclasses import dataclass

from automation.base_site import BaseSite


@dataclass(frozen=True)
class SiteConfig:
    name: str
    result_attribute: str
    site: BaseSite
