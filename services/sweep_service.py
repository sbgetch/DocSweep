from automation.vertiv import VertivSite

from utils.logger import get_logger

logger = get_logger(__name__)


class SweepService:

    def __init__(self, driver):

        self.vertiv = VertivSite(driver)

    def sweep(self, documents):

        logger.info(
            f"Starting sweep for {len(documents)} document(s)."
        )

        self.vertiv.attach()

        for document in documents:

            logger.info(
                f"Sweeping {document.control_number}"
            )

            result = self.vertiv.search(
                document.control_number
            )

            document.vertiv = result.message

        logger.info("Sweep complete.")