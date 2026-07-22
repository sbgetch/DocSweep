from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

BROWSER_DIR = BASE_DIR / "browser"

CHROME_BINARY = BROWSER_DIR / "chrome-win64" / "chrome.exe"

CHROMEDRIVER = BROWSER_DIR / "chromedriver-win64" / "chromedriver.exe"

TIMEOUT = 15

# SITES
VERTIV_URL = "https://www.vertiv.com/en-us/"

ASSET_LIBRARY_URL = "https://asset-library.vertiv.com/#/home?tabName=HOME"

ORACLE_URL = "https://egup.fa.us2.oraclecloud.com/fscmUI/faces/FndOverview?pageParams=fndGlobalItemNodeId%3DitemNode_product_management_product_development&fndGlobalItemNodeId=itemNode_product_management_product_development&_adf.ctrl-state=CTzs-5yoqQZV_1&_adf.no-new-window-redirect=true&_afrLoop=2780622838863036&_afrWindowMode=2&_afrWindowId=null&_afrFS=16&_afrMT=screen&_afrMFW=944&_afrMFH=882&_afrMFDW=1920&_afrMFDH=1080&_afrMFC=8&_afrMFCI=0&_afrMFM=0&_afrMFR=96&_afrMFG=0&_afrMFS=0&_afrMFO=0"

MASW_URL = "https://amerplmpwiap01.int.vertivco.com/File_Display_MBD/faces/UserManualDisplay.xhtml"

# EXCEL
CONTROL_NUMBER_COLUMN = "A"
FIRST_DATA_ROW = 2
MASW_COLUMN = "E"
VERTIV_COLUMN = "F"
ASSET_LIBRARY_COLUMN = "G"
PD_CLOUD_COLUMN = "H"
