from pathlib import Path

from excel.reader import ExcelReader
from excel.writer import ExcelWriter

from services.sweep_service import SweepService

from utils.events import EVENT_STAGE


class SweepRunner:

    def __init__(self, driver, progress_callback=None):

        self.driver = driver
        self.progress_callback = progress_callback

    def report_progress(self, **kwargs):

        if self.progress_callback:

            self.progress_callback(**kwargs)

    def run(self, input_file: str, output_folder: str):

        self.report_progress(
            event=EVENT_STAGE,
            status="Reading Excel...",
        )

        reader = ExcelReader()

        documents = reader.read(input_file)

        self.report_progress(
            event=EVENT_STAGE,
            status="Searching documents...",
        )

        sweep = SweepService(
            self.driver,
            progress_callback=self.progress_callback,
        )

        sweep.sweep(documents)

        self.report_progress(
            event=EVENT_STAGE,
            status="Writing Excel...",
        )

        output_file = str(Path(output_folder) / Path(input_file).name)

        writer = ExcelWriter()

        writer.save(
            output_file,
            documents,
        )

        self.report_progress(
            event=EVENT_STAGE,
            status="Completed",
            output_file=output_file,
        )

        return output_file
