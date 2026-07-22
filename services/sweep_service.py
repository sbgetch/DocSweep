import time
from datetime import timedelta

from selenium.common.exceptions import (
    NoSuchElementException,
    NoSuchWindowException,
    StaleElementReferenceException,
    TimeoutException,
    WebDriverException,
)

from automation.base_site import BaseSite
from automation.vertiv import VertivSite
from automation.asset_library import AssetLibrarySite
from automation.pd_cloud import PDCloudSite
from automation.masw import MASWSite

from models.site_config import SiteConfig

from utils.constants import (
    SITE_VERTIV,
    SITE_ASSET_LIBRARY,
    SITE_PD_CLOUD,
    SITE_MASW,
)
from utils.logger import get_logger
from utils.events import (
    EVENT_PROGRESS,
    EVENT_SITE_COMPLETE,
    EVENT_SITE_START,
)

logger = get_logger(__name__)

ERROR = "ERROR"


class SweepService:

    def __init__(self, driver, progress_callback=None):

        self.progress_callback = progress_callback

        self.sites: tuple[SiteConfig, ...] = (
            SiteConfig(
                name=SITE_VERTIV,
                result_attribute="vertiv",
                site=VertivSite(driver),
            ),
            SiteConfig(
                name=SITE_ASSET_LIBRARY,
                result_attribute="asset_library",
                site=AssetLibrarySite(driver),
            ),
            SiteConfig(
                name=SITE_PD_CLOUD,
                result_attribute="pd_cloud",
                site=PDCloudSite(driver),
            ),
            SiteConfig(
                name=SITE_MASW,
                result_attribute="masw",
                site=MASWSite(driver),
            ),
        )

    def report_progress(self, **kwargs):

        if self.progress_callback:

            self.progress_callback(**kwargs)

    def sweep(self, documents):

        overall_start = time.perf_counter()

        logger.info(f"Starting sweep for {len(documents)} document(s).")

        for config in self.sites:

            self.sweep_site(
                site=config.site,
                site_name=config.name,
                result_attribute=config.result_attribute,
                documents=documents,
            )

        elapsed_seconds = round(time.perf_counter() - overall_start)

        overall_elapsed = timedelta(
            seconds=elapsed_seconds,
        )

        logger.info(f"Overall elapsed: {overall_elapsed}")

        logger.info("Sweep complete.")

    def sweep_site(
        self,
        site: BaseSite,
        site_name: str,
        result_attribute: str,
        documents,
    ):

        logger.info(f"Starting {site_name} sweep.")

        self.report_progress(
            event=EVENT_SITE_START,
            site=site_name,
        )

        start_time = time.perf_counter()

        site.attach()

        total = len(documents)

        found = 0
        not_found = 0
        errors = 0

        for index, document in enumerate(documents, start=1):

            self.log_progress(
                site_name,
                index,
                total,
                document.control_number,
            )

            self.report_progress(
                event=EVENT_PROGRESS,
                site=site_name,
                current=index,
                total=total,
                control_number=document.control_number,
            )

            try:

                result = self.search_with_retry(
                    site,
                    document.control_number,
                )

                setattr(
                    document,
                    result_attribute,
                    result.message,
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
                    result_attribute,
                    ERROR,
                )

                errors += 1

        elapsed = timedelta(seconds=round(time.perf_counter() - start_time))

        logger.info(f"{site_name} sweep complete.")

        logger.info(f"{site_name} Summary")
        logger.info(f"  Found     : {found}")
        logger.info(f"  Not Found : {not_found}")
        logger.info(f"  Errors    : {errors}")
        logger.info(f"  Elapsed   : {elapsed}")

        self.report_progress(
            event=EVENT_SITE_COMPLETE,
            site=site_name,
            found=found,
            not_found=not_found,
            errors=errors,
            elapsed=str(elapsed),
        )

    def log_progress(
        self,
        site_name: str,
        current: int,
        total: int,
        control_number: str,
    ):

        logger.info(f"{site_name} ({current}/{total}): {control_number}")

    def get_error_reason(
        self,
        exception: Exception,
    ) -> str:

        if isinstance(exception, TimeoutException):

            return "Timed out waiting for search results."

        if isinstance(exception, StaleElementReferenceException):

            return "The page refreshed while searching."

        if isinstance(exception, NoSuchElementException):

            return "Expected page element was not found."

        if isinstance(exception, NoSuchWindowException):

            return "Browser tab was closed."

        if isinstance(exception, WebDriverException):

            return "WebDriver error occurred."

        return f"Unexpected error: " f"{type(exception).__name__}"

    def search_with_retry(
        self,
        site: BaseSite,
        control_number: str,
    ):

        try:

            return site.search(control_number)

        except (
            TimeoutException,
            StaleElementReferenceException,
        ):

            logger.warning(f"Retrying search for {control_number}")

            return site.search(control_number)
