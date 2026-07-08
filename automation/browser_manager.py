from pathlib import Path
from utils.logger import get_logger
from utils.exceptions import BrowserNotFoundError

logger = get_logger(__name__)

class BrowserManager:

    def __init__(self):
        # DocSweep root directory
        self.base_dir = Path(__file__).resolve().parent.parent

        # browser/
        self.browser_dir = self.base_dir / "browser"

    def get_chrome_path(self):
        return (
            self.browser_dir /
            "chrome-win64" /
            "chrome.exe"
        )

    def get_driver_path(self):
        return (
            self.browser_dir /
            "chromedriver-win64" /
            "chromedriver.exe"
        )

    def validate(self):

        logger.info("Validating browser files...")

        if not self.get_chrome_path().exists():
            raise BrowserNotFoundError(
                f"Chrome for Testing not found:\n{self.get_chrome_path()}"
            )

        if not self.get_driver_path().exists():
            raise FileNotFoundError(
                f"ChromeDriver not found:\n{self.get_driver_path()}"
            )