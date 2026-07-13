from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.constants import FOUND, NOT_FOUND
from utils.logger import get_logger
from utils.wait_helper import WaitHelper

logger = get_logger(__name__)


class AssetLibrarySite(BaseSite):

    EXPECTED_HOST = "asset-library.vertiv.com"

    SEARCH_INPUT = (
        By.ID,
        "searchInput"
    )

    CLEAR_BUTTON = (
        By.LINK_TEXT,
        "Clear"
    )

    KEYWORD = (
        By.CSS_SELECTOR,
        "li span[title]"
    )

    NO_RESULTS = (
        By.XPATH,
        "//span[text()='No Assets Found']"
    )

    # RESULT_TITLES = (
    #     By.XPATH,
    #     "//tbody//td[2]//div[@title]"
    # )

    def attach(self):

        logger.info("Looking for Asset Library tab.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                logger.info("Asset Library tab found.")

                return

        raise RuntimeError(
            "Asset Library tab is not open."
        )

    def clear_search(self):

        buttons = self.driver.find_elements(
            *self.CLEAR_BUTTON
        )

        if not buttons:
            return

        logger.info("Clearing previous search.")

        buttons[0].click()

        self.wait_for_clear_complete()

    def wait_for_clear_complete(self):

        logger.info(
            "Waiting for blank search to complete."
        )

        #
        # Wait until all keyword chips are gone.
        #

        WaitHelper.until(

            self.driver,

            lambda driver:

                len(
                    driver.find_elements(
                        *self.KEYWORD
                    )
                ) == 0

        )

        #
        # Wait until loading finishes.
        #

        WaitHelper.until(

            self.driver,

            lambda driver:

                "Loading..." not in driver.page_source

        )

        #
        # Ensure the search box is ready again.
        #

        WaitHelper.clickable(
            self.driver,
            self.SEARCH_INPUT
        )

        logger.info(
            "Blank search completed."
        )

    def execute_search(
        self,
        control_number: str
    ):

        logger.info(
            f"Searching control number: {control_number}"
        )

        self.clear_search()

        search = WaitHelper.clickable(
            self.driver,
            self.SEARCH_INPUT
        )

        search.clear()

        search.send_keys(control_number)

        search.send_keys(Keys.ENTER)

        self.wait_for_search_complete(
            control_number
        )

        logger.info("Search completed.")

    def wait_for_search_complete(
        self,
        control_number: str
    ):

        logger.info(
            "Waiting for search results."
        )

        WaitHelper.until(

            self.driver,

            lambda driver:

                self.keyword_matches(
                    control_number
                )

        )

        WaitHelper.until(

            self.driver,

            lambda driver:

                "Loading..." not in driver.page_source

        )

    def keyword_matches(
        self,
        control_number: str
    ) -> bool:

        elements = self.driver.find_elements(
            *self.KEYWORD
        )

        if not elements:
            return False

        return (

            elements[0]
            .get_attribute("title")
            .strip()
            .upper()

            ==

            control_number.upper()

        )

    # def get_result_titles(self) -> list[str]:

    #     elements = self.driver.find_elements(
    #         *self.RESULT_TITLES
    #     )

    #     return [

    #         element.get_attribute("title").strip()

    #         for element in elements

    #         if element.get_attribute("title")

    #     ]

    def search(
        self,
        control_number: str
    ) -> SearchResult:

        self.execute_search(
            control_number
        )

        elements = self.driver.find_elements(
            *self.NO_RESULTS
        )

        if (
            elements
            and
            elements[0].is_displayed()
        ):

            logger.info(
                "No matching document."
            )

            return SearchResult(
                site=Site.ASSET_LIBRARY,
                found=False,
                message=NOT_FOUND
            )

        # titles = self.get_result_titles()

        # logger.info(
        #     f"{len(titles)} search result(s) found."
        # )

        # for title in titles:

        #     if control_number.upper() in title.upper():

        #         logger.info(
        #             f"Document '{control_number}' found."
        #         )

        #         return SearchResult(
        #             site=Site.ASSET_LIBRARY,
        #             found=True,
        #             message=FOUND
        #         )

        # logger.info(
        #     "Search returned documents, but none matched."
        # )

        logger.info(
            "Search returned one or more result(s)."
        )

        return SearchResult(
            site=Site.ASSET_LIBRARY,
            found=True,
            message=FOUND
        )