import json
import time


def wait_for_request(driver, url_suffix, timeout=15):
    """
    Wait until a network request matching the given URL suffix
    has completed successfully.

    Args:
        driver: Selenium WebDriver.
        url_suffix: URL suffix to match (e.g. "/api-lang/en/searchResults/search").
        timeout: Maximum wait time in seconds.
    """

    deadline = time.time() + timeout

    while time.time() < deadline:

        logs = driver.get_log("performance")

        for entry in logs:

            try:
                message = json.loads(entry["message"])["message"]
            except (KeyError, json.JSONDecodeError):
                continue

            if message.get("method") != "Network.responseReceived":
                continue

            response = message.get("params", {}).get("response", {})

            if (
                response.get("url", "").endswith(url_suffix)
                and response.get("status") == 200
            ):
                return

        time.sleep(0.1)

    raise TimeoutError(
        f"Timed out waiting for request ending with '{url_suffix}'."
    )