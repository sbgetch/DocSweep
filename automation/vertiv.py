from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.logger import get_logger

logger = get_logger("Vertiv")

class VertivSite(BaseSite):

    URL = "https://www.vertiv.com/en-us/"

    EXPANDED_CLASS = "search-is-expanded"

    SEARCH_FORM = (
        By.CSS_SELECTOR,
        "form.search-expand"
    )

    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "button.search-expand__icon"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[ng-model='self.query']"
    )

    def open(self):

        logger.info("Opening Vertiv website.")

        self.driver.get(self.URL)

    def wait_until_ready(self):

        logger.info("Waiting for Vertiv search.")

        WebDriverWait(self.driver, 15).until(

            EC.element_to_be_clickable(

                (By.CSS_SELECTOR,
                 "input[ng-model='self.query']")
            )
        )

        logger.info("Vertiv ready.")

    def search(self, control_number):

        logger.info(f"Searching {control_number}")

        search = self.driver.find_element(

            By.CSS_SELECTOR,

            "input[ng-model='self.query']"
        )

        search.clear()

        search.send_keys(control_number)

        search.send_keys(Keys.ENTER)

        return SearchResult(
            site=Site.VERTIV,
            found=True,
            message="Temporary"
        )
    
    def is_search_expanded(self) -> bool:

        form = self.driver.find_element(*self.SEARCH_FORM)

        return self.EXPANDED_CLASS in form.get_attribute("class")
    
    def prepare_search(self):

        logger.info("Preparing Vertiv search...")

        if self.is_search_expanded():
            logger.info("Search is already expanded.")
            return

        logger.info("Expanding search.")

        button = WebDriverWait(self.driver, 15).until(
            EC.element_to_be_clickable(self.SEARCH_BUTTON)
        )

        button.click()

        WebDriverWait(self.driver, 15).until(
            lambda driver: self.is_search_expanded()
        )

        logger.info("Search expanded.")