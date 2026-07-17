from openpyxl import load_workbook

from config import MASW_COLUMN, VERTIV_COLUMN, ASSET_LIBRARY_COLUMN, PD_CLOUD_COLUMN

from utils.logger import get_logger

logger = get_logger(__name__)


class ExcelWriter:

    def save(self, file_path, documents):

        logger.info(f"Saving workbook: {file_path}")

        workbook = load_workbook(file_path)

        worksheet = workbook.worksheets[0]

        for document in documents:

            row = document.row

            worksheet[f"{MASW_COLUMN}{row}"] = document.masw
            worksheet[f"{VERTIV_COLUMN}{row}"] = document.vertiv
            worksheet[f"{ASSET_LIBRARY_COLUMN}{row}"] = document.asset_library
            worksheet[f"{PD_CLOUD_COLUMN}{row}"] = document.pd_cloud

        workbook.save(file_path)

        logger.info("Workbook saved successfully.")
