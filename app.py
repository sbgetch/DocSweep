from automation.browser import Browser
from automation.vertiv import VertivSite

from utils.logger import get_logger

logger = get_logger(__name__)


def main():

    logger.info("Starting DocSweep")

    browser = Browser()
    driver = browser.start()

    logger.info("Browser launched.")

    input(
        "\n"
        "Prepare the required websites:\n"
        "  • Vertiv\n"
        "  • Asset Library\n"
        "  • Oracle\n"
        "  • MASW\n\n"
        "Log in to the sites, then press ENTER to start the sweep..."
    )

    vertiv = VertivSite(driver)

    vertiv.attach()

    vertiv.prepare_search()

    result = vertiv.search("SL-71029")

    logger.info(result)

    input("\nSweep complete. Press ENTER to exit...")

    browser.stop()


if __name__ == "__main__":
    main()