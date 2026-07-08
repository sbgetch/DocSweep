from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.constants import FOUND, NOT_FOUND
from utils.logger import get_logger
from utils.wait_helper import WaitHelper

logger = get_logger(__name__)


class VertivSite(BaseSite):

    URL = "https://www.vertiv.com/en-us/"
    EXPECTED_HOST = "vertiv.com"

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

    RESULTS = (
        By.CSS_SELECTOR,
        "div.product-tile-component.search-tile"
    )

    NO_RESULTS = (
        By.ID,
        "noResults"
    )

    RESULT_TITLES = (
        By.CSS_SELECTOR,
        "div.product-tile-component.search-tile h3 a"
    )

    def is_open(self) -> bool:

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                return True

        return False

    def attach(self):

        logger.info("Looking for Vertiv tab.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                logger.info("Attached to Vertiv.")

                return

        raise RuntimeError(
            "Vertiv website is not open."
        )

    def prepare_search(self):

        logger.info("Preparing Vertiv search.")

        if self.is_search_expanded():
            logger.info("Search is already expanded.")
            return

        logger.info("Expanding search.")

        button = WaitHelper.clickable(
            self.driver,
            self.SEARCH_BUTTON
        )

        button.click()

        WaitHelper.until(
            self.driver,
            lambda driver: self.is_search_expanded()
        )

        logger.info("Search expanded.")

    def search(self, control_number):

        logger.info(
            f"Searching control number: {control_number}"
        )

        search = WaitHelper.clickable(
            self.driver,
            self.SEARCH_INPUT
        )

        search.clear()
        search.send_keys(control_number)
        search.send_keys(Keys.ENTER)

        logger.info("Waiting for search to complete...")

        if self.has_no_results():

            logger.info("No search results.")

            return SearchResult(
                site=Site.VERTIV,
                found=False,
                message=NOT_FOUND
            )

        WaitHelper.present(
            self.driver,
            self.RESULTS
        )

        titles = self.get_result_titles()

        logger.info(
            f"{len(titles)} search result(s) found."
        )

        for title in titles:

            if control_number.upper() in title.upper():

                logger.info(
                    f"Document '{control_number}' found."
                )

                return SearchResult(
                    site=Site.VERTIV,
                    found=True,
                    message=FOUND
                )

        logger.info("Search returned documents, but none matched the control number.")

        return SearchResult(
            site=Site.VERTIV,
            found=False,
            message=NOT_FOUND
        )

    def is_search_expanded(self) -> bool:

        form = self.driver.find_element(
            *self.SEARCH_FORM
        )

        return (
            self.EXPANDED_CLASS
            in form.get_attribute("class")
        )

    def get_result_titles(self) -> list[str]:

        elements = self.driver.find_elements(
            *self.RESULT_TITLES
        )

        return [
            element.text.strip()
            for element in elements
        ]
    
    def has_no_results(self) -> bool:

        return WaitHelper.exists(
            self.driver,
            self.NO_RESULTS,
            timeout=5
        )