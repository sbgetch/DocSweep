import time

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.constants import FOUND, NOT_FOUND
from utils.logger import get_logger
from utils.wait_helper import WaitHelper

logger = get_logger(__name__)


class PDCloudSite(BaseSite):

    EXPECTED_HOST = "egup.fa.us2.oraclecloud.com"

    ADVANCED_SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "a[aria-label*='Advanced Search']"
    )

    SEARCH_INPUT = (
        By.CSS_SELECTOR,
        "input[aria-label=' Keyword']"
    )

    SEARCH_BUTTON = (
        By.CSS_SELECTOR,
        "button[id$='::search']"
    )

    RESULT_TABLE = (
        By.CSS_SELECTOR,
        "table[summary='Item Search Results']"
    )

    BUSY_CLASS = "p_AFBusy"

    def attach(self):

        logger.info("Looking for PD Cloud tab.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                logger.info("PD Cloud tab found.")
                return

        raise RuntimeError(
            "PD Cloud tab is not open."
        )

    def search(
        self,
        control_number: str
    ) -> SearchResult:

        self.prepare_search()

        self.execute_search(
            control_number
        )

        if self.has_no_results():

            logger.info(
                "No matching document."
            )

            return self.build_not_found_result()

        logger.info(
            "Search returned one or more result(s)."
        )

        return self.build_found_result()

    def prepare_search(self):

        logger.info(
            "Preparing Advanced Search."
        )

        if self.is_search_expanded():

            logger.info(
                "Advanced Search already expanded."
            )

            return

        logger.info(
            "Expanding Advanced Search."
        )

        button = WaitHelper.clickable(
            self.driver,
            self.ADVANCED_SEARCH_BUTTON
        )

        button.click()

        WaitHelper.until(

            self.driver,

            lambda driver:
                self.is_search_expanded()

        )

        logger.info(
            "Advanced Search expanded."
        )

    def execute_search(
        self,
        control_number: str
    ):

        logger.info(
            f"Searching control number: {control_number}"
        )

        search = WaitHelper.clickable(
            self.driver,
            self.SEARCH_INPUT
        )

        search.clear()

        search.send_keys(
            control_number
        )

        button = WaitHelper.clickable(
            self.driver,
            self.SEARCH_BUTTON
        )

        button.click()

        self.wait_for_search_complete()

        logger.info(
            "Search completed."
        )

    def wait_for_search_complete(
        self,
        timeout=30
    ):

        logger.info(
            "Waiting for PD Cloud search to complete."
        )

        #
        # Busy indicator may appear very briefly.
        #

        try:

            WaitHelper.until(

                self.driver,

                lambda driver:

                    self.BUSY_CLASS

                    in

                    driver.find_element(
                        *self.RESULT_TABLE
                    ).get_attribute("class"),

                timeout=2

            )

        except TimeoutException:

            pass

        #
        # Wait until busy disappears.
        #

        WaitHelper.until(

            self.driver,

            lambda driver:

                self.BUSY_CLASS

                not in

                driver.find_element(
                    *self.RESULT_TABLE
                ).get_attribute("class"),

            timeout=timeout

        )

        #
        # Wait until the table content stops changing.
        #

        stable_count = 0
        previous_html = ""

        end_time = time.time() + timeout

        while time.time() < end_time:

            html = self.driver.find_element(
                *self.RESULT_TABLE
            ).get_attribute(
                "innerHTML"
            )

            if html == previous_html:

                stable_count += 1

                if stable_count >= 3:

                    break

            else:

                stable_count = 0
                previous_html = html

            time.sleep(0.2)

        logger.info(
            "PD Cloud search finished."
        )

    def has_no_results(
        self
    ) -> bool:

        elements = self.driver.find_elements(

            By.XPATH,

            "//*[normalize-space()='No results found.']"

        )

        if elements:

            logger.info(
                "Oracle returned 'No results found.'"
            )

            return True

        return False

    def build_found_result(
        self
    ) -> SearchResult:

        return SearchResult(

            site=Site.PD_CLOUD,

            found=True,

            message=FOUND

        )

    def build_not_found_result(
        self
    ) -> SearchResult:

        return SearchResult(

            site=Site.PD_CLOUD,

            found=False,

            message=NOT_FOUND

        )

    def is_search_expanded(
        self
    ) -> bool:

        button = self.driver.find_element(
            *self.ADVANCED_SEARCH_BUTTON
        )

        return (

            button.get_attribute(
                "aria-expanded"
            )

            ==

            "true"

        )