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

        # --------------------------------------------------
        # Vertiv
        # --------------------------------------------------

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

        # --------------------------------------------------
        # Asset Library
        # --------------------------------------------------

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

        # --------------------------------------------------
        # PD Cloud
        # --------------------------------------------------

        logger.info("Starting PD Cloud sweep.")

        self.pd_cloud.attach()

        for document in documents:

            logger.info(
                f"PD Cloud: {document.control_number}"
            )

            try:

                result = self.pd_cloud.search(
                    document.control_number
                )

                document.pd_cloud = result.message

            except Exception:

                logger.exception(
                    f"PD Cloud failed: {document.control_number}"
                )

                document.pd_cloud = "ERROR"

        logger.info("PD Cloud sweep complete.")

        # --------------------------------------------------
        # MASW
        # --------------------------------------------------

        logger.info("Starting MASW sweep.")

        self.masw.attach()

        for document in documents:

            logger.info(
                f"MASW: {document.control_number}"
            )

            try:

                result = self.masw.search(
                    document.control_number
                )

                document.masw = result.message

            except Exception:

                logger.exception(
                    f"MASW failed: {document.control_number}"
                )

                document.masw = "ERROR"

        logger.info("MASW sweep complete.")

        logger.info("Sweep complete.")