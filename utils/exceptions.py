class DocSweepError(Exception):
    """Base exception for DocSweep."""
    pass


class BrowserNotFoundError(DocSweepError):
    pass


class SiteNotReadyError(DocSweepError):
    pass