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


class SweepService:

    def __init__(self, driver):

        self.vertiv = VertivSite(driver)
        self.asset_library = AssetLibrarySite(driver)
        self.pd_cloud = PDCloudSite(driver)
        self.masw = MASWSite(driver)

    def sweep(self, documents):

        logger.info(
            f"Starting sweep for {len(documents)} document(s)."
        )

        #
        # Vertiv
        #

        logger.info("Starting Vertiv sweep.")

        self.vertiv.attach()

        for document in documents:

            logger.info(
                f"Vertiv: {document.control_number}"
            )

            self.execute_search(

                site=self.vertiv,

                document=document,

                attribute="vertiv"

            )

        logger.info("Vertiv sweep complete.")

        #
        # Asset Library
        #

        logger.info("Starting Asset Library sweep.")

        self.asset_library.attach()

        for document in documents:

            logger.info(
                f"Asset Library: {document.control_number}"
            )

            self.execute_search(

                site=self.asset_library,

                document=document,

                attribute="asset_library"

            )

        logger.info("Asset Library sweep complete.")

        #
        # PD Cloud
        #

        logger.info("Starting PD Cloud sweep.")

        self.pd_cloud.attach()

        for document in documents:

            logger.info(
                f"PD Cloud: {document.control_number}"
            )

            self.execute_search(

                site=self.pd_cloud,

                document=document,

                attribute="pd_cloud"

            )

        logger.info("PD Cloud sweep complete.")

        #
        # MASW
        #

        logger.info("Starting MASW sweep.")

        self.masw.attach()

        for document in documents:

            logger.info(
                f"MASW: {document.control_number}"
            )

            self.execute_search(

                site=self.masw,

                document=document,

                attribute="masw"

            )

        logger.info("MASW sweep complete.")

        logger.info("Sweep complete.")

    def execute_search(
        self,
        site,
        document,
        attribute: str
    ):

        try:

            result = site.search(
                document.control_number
            )

            setattr(
                document,
                attribute,
                result.message
            )

        except Exception as exception:

            logger.exception(

                f"{attribute.replace('_', ' ').title()} failed: "
                f"{document.control_number} "
                f"({self.get_error_reason(exception)})"

            )

            setattr(
                document,
                attribute,
                "ERROR"
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