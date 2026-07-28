from pathlib import Path

from utils.exceptions import BrowserNotFoundError
from utils.logger import get_logger

logger = get_logger(__name__)


class BrowserManager:

    CHROME_PATH = Path(
        r"C:\Program Files\Google\chrome-win64\chrome.exe"
    )

    DRIVER_PATH = Path(
        r"C:\Program Files\Google\chromedriver-win64\chromedriver.exe"
    )

    def get_chrome_path(self):
        return self.CHROME_PATH

    def get_driver_path(self):
        return self.DRIVER_PATH

    def validate(self):

        logger.info("Validating browser installation...")

        if not self.CHROME_PATH.exists():
            raise BrowserNotFoundError(
                "Chrome for Testing was not found.\n\n"
                f"Expected location:\n{self.CHROME_PATH}\n\n"
                "Please install Chrome for Testing and try again."
            )

        if not self.DRIVER_PATH.exists():
            raise BrowserNotFoundError(
                "ChromeDriver was not found.\n\n"
                f"Expected location:\n{self.DRIVER_PATH}\n\n"
                "Please install the matching ChromeDriver and try again."
            )

        logger.info("Browser validation successful.")