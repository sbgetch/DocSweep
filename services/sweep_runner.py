from pathlib import Path

from excel.reader import ExcelReader
from excel.writer import ExcelWriter

from services.sweep_service import SweepService

from utils.events import EVENT_STAGE, EVENT_SWEEP_COMPLETE, EVENT_SWEEP_CANCELLED
from utils.logger import get_logger

logger = get_logger(__name__)


class SweepRunner:

    def __init__(
        self,
        driver,
        progress_callback=None,
        log_callback=None,
        cancel_event=None,
    ):

        self.driver = driver
        self.progress_callback = progress_callback
        self.log_callback = log_callback
        self.cancel_event = cancel_event

    def report_progress(self, **kwargs):

        if self.progress_callback:

            self.progress_callback(**kwargs)

    def run(self, input_file: str, output_folder: str):

        self.log("Reading Excel...")

        self.report_progress(
            event=EVENT_STAGE,
            status="Reading Excel...",
        )

        reader = ExcelReader()

        documents = reader.read(input_file)

        self.log(f"Loaded {len(documents)} document(s).")

        self.log("Searching documents...")

        self.report_progress(
            event=EVENT_STAGE,
            status="Searching documents...",
        )

        sweep = SweepService(
            self.driver,
            progress_callback=self.progress_callback,
            log_callback=self.log_callback,
            cancel_event=self.cancel_event,
        )

        completed = sweep.sweep(documents)

        if not completed:

            self.log("Saving partial results...")

        self.log("Saving workbook...")

        self.report_progress(
            event=EVENT_STAGE,
            status="Writing Excel...",
        )

        output_file = str(
            Path(output_folder) / Path(input_file).name
        )

        writer = ExcelWriter()

        writer.save(
            output_file,
            documents,
        )

        self.log(f"Workbook saved: {output_file}")

        if completed:

            self.report_progress(
                event=EVENT_SWEEP_COMPLETE,
                output_file=output_file,
            )

        else:

            self.report_progress(
                event=EVENT_SWEEP_CANCELLED,
                output_file=output_file,
            )

        return output_file

    def log(self, message: str):

        logger.info(message)

        if self.log_callback:

            self.log_callback(message)
