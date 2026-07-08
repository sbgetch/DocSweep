from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from config import TIMEOUT


class WaitHelper:

    DEFAULT_TIMEOUT = TIMEOUT

    @staticmethod
    def clickable(driver, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        )

    @staticmethod
    def visible(driver, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(driver, timeout).until(
            EC.visibility_of_element_located(locator)
        )

    @staticmethod
    def present(driver, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(driver, timeout).until(
            EC.presence_of_element_located(locator)
        )

    @staticmethod
    def invisible(driver, locator, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(driver, timeout).until(
            EC.invisibility_of_element_located(locator)
        )
    
    @staticmethod
    def until(driver, condition, timeout=DEFAULT_TIMEOUT):
        return WebDriverWait(driver, timeout).until(condition)
    
    @staticmethod
    def exists(driver, locator, timeout=DEFAULT_TIMEOUT):
        """
        Returns True if the element exists within the timeout,
        otherwise returns False.
        """

        try:
            WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located(locator)
            )
            return True

        except TimeoutException:
            return False