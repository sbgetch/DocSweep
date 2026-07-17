from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BROWSER_DIR = BASE_DIR / "browser"

CHROME_BINARY = BROWSER_DIR / "chrome-win64" / "chrome.exe"

CHROMEDRIVER = BROWSER_DIR / "chromedriver-win64" / "chromedriver.exe"

TIMEOUT = 15

# SITES
VERTIV_URL = "https://www.vertiv.com/en-us/"

ASSET_LIBRARY_URL = "https://asset-library.vertiv.com/#/home?tabName=HOME"

ORACLE_URL = "https://egup.fa.us2.oraclecloud.com/"

MASW_URL = "https://amerplmpwiap01.int.vertivco.com/File_Display_MBD/faces/UserManualDisplay.xhtml"

# EXCEL
CONTROL_NUMBER_COLUMN = "A"
FIRST_DATA_ROW = 2
MASW_COLUMN = "E"
VERTIV_COLUMN = "F"
ASSET_LIBRARY_COLUMN = "G"
PD_CLOUD_COLUMN = "H"
