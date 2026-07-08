from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from automation.browser_manager import BrowserManager
from utils.logger import get_logger

logger = get_logger("Browser")

class Browser:

    def __init__(self):
        self.driver = None
        self.manager = BrowserManager()

    def start(self):

        # Validate browser files exist
        logger.info("Launching Chrome for Testing...")

        self.manager.validate()

        options = Options()

        options.binary_location = str(
            self.manager.get_chrome_path()
        )

        options.add_argument("--start-maximized")

        self.driver = webdriver.Chrome(
            service=Service(
                str(self.manager.get_driver_path())
            ),
            options=options
        )

        logger.info("Browser launched successfully.")

        return self.driver

    def stop(self):
        if self.driver:
            logger.info("Closing browser.")
            self.driver.quit()