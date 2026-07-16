from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    StaleElementReferenceException
)

from automation.base_site import BaseSite

from models.search_result import SearchResult
from models.site import Site

from utils.constants import FOUND, NOT_FOUND
from utils.logger import get_logger
from utils.wait_helper import WaitHelper

logger = get_logger(__name__)


class MASWSite(BaseSite):

    EXPECTED_HOST = "amerplmpwiap01.int.vertivco.com"

    SEARCH_INPUT = (
        By.ID,
        "mcpForm:attValue"
    )

    SEARCH_BUTTON = (
        By.ID,
        "mcpForm:advancedSearchButton"
    )

    SEARCH_STATUS = (
        By.CSS_SELECTOR,
        "#mcpForm\\:itemDetailTable .ui-datatable-header label:first-of-type"
    )

    NO_RESULTS = (
        By.XPATH,
        "//td[contains(., 'No Item found with the given Criteria')]"
    )

    def attach(self):

        logger.info("Looking for MASW tab.")

        for handle in self.driver.window_handles:

            self.driver.switch_to.window(handle)

            if self.EXPECTED_HOST in self.driver.current_url.lower():

                logger.info("MASW tab found.")

                return

        raise RuntimeError(
            "MASW tab is not open."
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

        #
        # Reserved for future setup.
        #

        return

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

        self.wait_for_search_complete(
            control_number
        )

        logger.info(
            "MASW search completed."
        )

    def wait_for_search_complete(
        self,
        control_number: str,
        timeout=30
    ):

        logger.info(
            "Waiting for MASW search."
        )

        self.wait_for_status_update(

            control_number,

            timeout

        )

        logger.info(
            "MASW search finished."
        )

    def wait_for_status_update(
        self,
        control_number: str,
        timeout: int
    ):

        WaitHelper.until(

            self.driver,

            lambda driver:

                self.search_status_matches(
                    control_number
                ),

            timeout=timeout

        )

    def search_status_matches(
        self,
        control_number: str
    ) -> bool:

        try:

            text = self.driver.find_element(
                *self.SEARCH_STATUS
            ).text.upper()

            return (

                control_number.upper()

                in

                text

            )

        except StaleElementReferenceException:

            #
            # PrimeFaces refreshes the table.
            #

            return False

    def has_no_results(
        self
    ) -> bool:

        elements = self.driver.find_elements(
            *self.NO_RESULTS
        )

        return (

            bool(elements)

            and

            elements[0].is_displayed()

        )

    def build_found_result(
        self
    ) -> SearchResult:

        return SearchResult(

            site=Site.MASW,

            found=True,

            message=FOUND

        )

    def build_not_found_result(
        self
    ) -> SearchResult:

        return SearchResult(

            site=Site.MASW,

            found=False,

            message=NOT_FOUND

        )