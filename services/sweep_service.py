import time
from datetime import timedelta

from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException
)

from automation.vertiv import VertivSite
from automation.asset_library import AssetLibrarySite
from automation.pd_cloud import PDCloudSite
from automation.masw import MASWSite

from utils.logger import get_logger

logger = get_logger(__name__)

ERROR = "ERROR"


class SweepService:

    def __init__(self, driver):

        self.vertiv = VertivSite(driver)
        self.asset_library = AssetLibrarySite(driver)
        self.pd_cloud = PDCloudSite(driver)
        self.masw = MASWSite(driver)

    def sweep(self, documents):
        
        overall_start = time.perf_counter()
        
        logger.info(
            f"Starting sweep for {len(documents)} document(s)."
        )


        self.sweep_site(
            site=self.vertiv,
            site_name="Vertiv",
            attribute="vertiv",
            documents=documents
        )

        self.sweep_site(
            site=self.asset_library,
            site_name="Asset Library",
            attribute="asset_library",
            documents=documents
        )

        self.sweep_site(
            site=self.pd_cloud,
            site_name="PD Cloud",
            attribute="pd_cloud",
            documents=documents
        )

        self.sweep_site(
            site=self.masw,
            site_name="MASW",
            attribute="masw",
            documents=documents
        )

        overall_elapsed = timedelta(
            seconds=round(
                time.perf_counter() - overall_start
            )
        )

        logger.info(
            f"Overall elapsed: {overall_elapsed}"
        )

        logger.info("Sweep complete.")

    def sweep_site(
        self,
        site,
        site_name: str,
        attribute: str,
        documents
    ):

        logger.info(
            f"Starting {site_name} sweep."
        )

        start_time = time.perf_counter()

        site.attach()

        total = len(documents)

        found = 0
        not_found = 0
        errors = 0

        for index, document in enumerate(
            documents,
            start=1
        ):

            self.log_progress(

                site_name,

                index,

                total,

                document.control_number

            )

            try:

                result = site.search(
                    document.control_number
                )

                setattr(
                    document,
                    attribute,
                    result.message
                )

                if result.found:

                    found += 1

                else:

                    not_found += 1

            except Exception as exception:

                logger.exception(

                    f"{site_name} failed: "
                    f"{document.control_number} "
                    f"({self.get_error_reason(exception)})"

                )

                setattr(
                    document,
                    attribute,
                    ERROR
                )

                errors += 1

        logger.info(
            f"{site_name} sweep complete."
        )

        elapsed = timedelta(
            seconds=round(
                time.perf_counter() - start_time
            )
        )

        logger.info(
            f"{site_name} Summary"
        )

        logger.info(
            f"  Found     : {found}"
        )

        logger.info(
            f"  Not Found : {not_found}"
        )

        logger.info(
            f"  Errors    : {errors}"
        )

        logger.info(
            f"  Elapsed   : {elapsed}"
        )

    def log_progress(
        self,
        site_name: str,
        current: int,
        total: int,
        control_number: str
    ):

        logger.info(

            f"{site_name} "
            f"({current}/{total}): "
            f"{control_number}"

        )

    def get_error_reason(
        self,
        exception: Exception
    ) -> str:

        if isinstance(
            exception,
            TimeoutException
        ):

            return (
                "Timed out waiting for search results."
            )

        if isinstance(
            exception,
            StaleElementReferenceException
        ):

            return (
                "The page refreshed while searching."
            )

        if isinstance(
            exception,
            NoSuchElementException
        ):

            return (
                "Expected page element was not found."
            )

        if isinstance(
            exception,
            NoSuchWindowException
        ):

            return (
                "Browser tab was closed."
            )

        if isinstance(
            exception,
            WebDriverException
        ):

            return (
                "WebDriver error occurred."
            )

        return (
            f"Unexpected error: "
            f"{type(exception).__name__}"
        )