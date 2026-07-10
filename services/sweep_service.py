from automation.vertiv import VertivSite
from automation.asset_library import AssetLibrarySite

from utils.logger import get_logger

logger = get_logger(__name__)


class SweepService:

    def __init__(self, driver):

        self.vertiv = VertivSite(driver)
        self.asset_library = AssetLibrarySite(driver)

    def sweep(self, documents):

        logger.info(
            f"Starting sweep for {len(documents)} document(s)."
        )

        # Vertiv

        logger.info("Starting Vertiv sweep.")

        self.vertiv.attach()

        for document in documents:

            logger.info(
                f"Vertiv: {document.control_number}"
            )

            try:

                result = self.vertiv.search(
                    document.control_number
                )

                document.vertiv = result.message

            except Exception:

                logger.exception(
                    f"Vertiv failed: {document.control_number}"
                )

                document.vertiv = "ERROR"

        logger.info("Vertiv sweep complete.")

        # Asset Library

        logger.info("Starting Asset Library sweep.")

        self.asset_library.attach()

        for document in documents:

            logger.info(
                f"Asset Library: {document.control_number}"
            )

            try:

                result = self.asset_library.search(
                    document.control_number
                )

                document.asset_library = result.message

            except Exception:

                logger.exception(
                    f"Asset Library failed: {document.control_number}"
                )

                document.asset_library = "ERROR"

        logger.info("Asset Library sweep complete.")

        logger.info("Sweep complete.")