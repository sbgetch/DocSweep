from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BROWSER_DIR = BASE_DIR / "browser"

CHROME_BINARY = (
    BROWSER_DIR /
    "chrome-win64" /
    "chrome.exe"
)

CHROMEDRIVER = (
    BROWSER_DIR /
    "chromedriver-win64" /
    "chromedriver.exe"
)

TIMEOUT = 15