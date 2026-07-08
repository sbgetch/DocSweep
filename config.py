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

EXCEL_SHEET = "Drawing Sweep"

CONTROL_NUMBER_COLUMN = "A"

FIRST_DATA_ROW = 2