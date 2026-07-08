from automation.browser import Browser
from automation.vertiv import VertivSite

from utils.logger import get_logger

logger = get_logger("App")


def main():

    browser = Browser()

    driver = browser.start()

    vertiv = VertivSite(driver)

    vertiv.open()

    vertiv.prepare_search()

    result = vertiv.search("PS231000")

    logger.info(result)

    input("Press ENTER...")

    browser.stop()


if __name__ == "__main__":
    main()