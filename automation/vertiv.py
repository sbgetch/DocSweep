from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.constants import FOUND, NOT_FOUND
from utils.logger import get_logger
from utils.wait_helper import WaitHelper
from utils.network_wait import wait_for_request

logger = get_logger(__name__)


class VertivSite(BaseSite):

    EXPECTED_HOST = "vertiv.com"

    EXPANDED_CLASS = "search-is-expanded"

    SEARCH_FORM = (By.CSS_SELECTOR, "form.search-expand")

    SEARCH_BUTTON = (By.CSS_SELECTOR, "button.search-expand__icon")

    SEARCH_INPUT = (By.CSS_SELECTOR, "input[ng-model='self.query']")

    RESULTS = (By.CSS_SELECTOR, "div.product-tile-component.search-tile")

    NO_RESULTS = (By.ID, "noResults")

    RESULT_TITLES = (By.CSS_SELECTOR, "div.product-tile-component.search-tile h3 a")

    def attach(self):

        logger.info("Looking for Vertiv tab.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                logger.info("Attached to Vertiv.")

                return

        raise RuntimeError("Vertiv website is not open.")

    def search(self, control_number: str) -> SearchResult:

        self.prepare_search()

        self.execute_search(control_number)

        if self.has_no_results():
            return self.build_not_found_result()

        return self.find_matching_result(control_number)

    def prepare_search(self):

        logger.info("Preparing Vertiv search.")

        if self.is_search_expanded():

            logger.info("Search is already expanded.")

            return

        logger.info("Expanding search.")

        button = WaitHelper.clickable(self.driver, self.SEARCH_BUTTON)

        button.click()

        WaitHelper.until(self.driver, lambda driver: self.is_search_expanded())

        logger.info("Search expanded.")

    def execute_search(self, control_number: str):

        logger.info(f"Searching control number: {control_number}")

        search = WaitHelper.clickable(self.driver, self.SEARCH_INPUT)

        # Clear previous network events
        self.driver.get_log("performance")

        search.clear()
        search.send_keys(control_number)
        search.send_keys(Keys.ENTER)

        wait_for_request(self.driver, "/api-lang/en/searchResults/search")

        logger.info("Search completed.")

    def find_matching_result(self, control_number: str) -> SearchResult:

        WaitHelper.present(self.driver, self.RESULTS)

        titles = self.get_result_titles()

        logger.info(f"{len(titles)} search result(s) found.")

        for title in titles:

            if control_number.upper() in title.upper():

                logger.info(f"Document '{control_number}' found.")

                return self.build_found_result()

        logger.info("Search returned documents, but none matched.")

        return self.build_not_found_result()

    def build_found_result(self) -> SearchResult:

        return SearchResult(site=Site.VERTIV, found=True, message=FOUND)

    def build_not_found_result(self) -> SearchResult:

        return SearchResult(site=Site.VERTIV, found=False, message=NOT_FOUND)

    def has_no_results(self) -> bool:

        return WaitHelper.exists(self.driver, self.NO_RESULTS, timeout=5)

    def get_result_titles(self) -> list[str]:

        elements = self.driver.find_elements(*self.RESULT_TITLES)

        return [element.text.strip() for element in elements]

    def is_search_expanded(self) -> bool:

        form = self.driver.find_element(*self.SEARCH_FORM)

        return self.EXPANDED_CLASS in form.get_attribute("class")
