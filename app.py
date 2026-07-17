from automation.browser import Browser

from excel.reader import ExcelReader
from excel.writer import ExcelWriter

from services.sweep_service import SweepService

from utils.logger import get_logger

logger = get_logger(__name__)


def main():

    logger.info("Starting DocSweep")

    browser = Browser()
    driver = browser.start()

    browser.open_startup_tabs()

    logger.info("Browser launched.")

    input(
        "Prepare the websites and log in to the sites, then press ENTER to start the sweep..."
    )

    reader = ExcelReader()

    documents = reader.read("input/Sweep Tracker.xlsx")

    service = SweepService(driver)

    service.sweep(documents)

    writer = ExcelWriter()

    writer.save("input/Sweep Tracker.xlsx", documents)

    input("\nSweep complete. Press ENTER to exit...")

    browser.stop()


if __name__ == "__main__":
    main()
