from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service

from automation.browser_manager import BrowserManager
from utils.logger import get_logger

from config import VERTIV_URL, ASSET_LIBRARY_URL, ORACLE_URL, MASW_URL

logger = get_logger(__name__)


class Browser:

    def __init__(self):
        self.driver = None
        self.manager = BrowserManager()

    def start(self):

        self.manager.validate()

        options = Options()

        options.binary_location = str(self.manager.get_chrome_path())

        options.add_argument("--start-maximized")

        options.set_capability("goog:loggingPrefs", {"performance": "ALL"})

        self.driver = webdriver.Chrome(
            service=Service(str(self.manager.get_driver_path())), options=options
        )

        self.driver.execute_cdp_cmd("Network.enable", {})

        return self.driver

    def open_startup_tabs(self):

        urls = [VERTIV_URL, ASSET_LIBRARY_URL, ORACLE_URL, MASW_URL]

        self.driver.get(urls[0])

        for url in urls[1:]:
            self.driver.switch_to.new_window("tab")
            self.driver.get(url)

    def is_running(self) -> bool:

        if not self.driver:
            return False

        try:

            self.driver.current_url

            return True

        except Exception:

            return False

    def stop(self):
        if self.driver:
            logger.info("Closing browser.")
            self.driver.quit()
