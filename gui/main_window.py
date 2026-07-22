import time
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

import threading

from services.sweep_runner import SweepRunner
from services.browser_service import BrowserService

from utils.logger import get_logger
from utils.constants import SITES
from utils.events import (
    EVENT_PROGRESS,
    EVENT_SITE_COMPLETE,
    EVENT_SITE_START,
    EVENT_STAGE,
)

logger = get_logger(__name__)

from version import __version__
class MainWindow:

    WINDOW_WIDTH = 850
    WINDOW_HEIGHT = 750

    def __init__(self):

        self.browser_service = BrowserService()

        self.root = tk.Tk()

        self.root.title(f"DocSweep v{__version__}")

        self.root.geometry(f"{self.WINDOW_WIDTH}x{self.WINDOW_HEIGHT}")

        self.root.minsize(800, 650)

        self.excel_path = tk.StringVar()

        self.output_folder = tk.StringVar()

        self.status = tk.StringVar(value="Idle")

        self.progress = tk.StringVar(value="0 / 0")

        self.current = tk.StringVar(value="-")

        self.elapsed = tk.StringVar(value="00:00:00")

        self.timer_running = False

        self.timer_start = None

        self.build_ui()

    def run(self):

        self.root.mainloop()

    def build_ui(self):

        container = ttk.Frame(self.root, padding=15)

        container.pack(fill="both", expand=True)

        self.build_preparation_frame(container)

        self.build_site_status_frame(container)

        self.build_input_frame(container)

        self.build_progress_frame(container)

        self.build_summary_frame(container)

        self.build_buttons(container)

    def build_preparation_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Preparation", padding=10)

        frame.pack(fill="x", pady=(0, 10))

        self.launch_button = ttk.Button(
            frame, text="Launch Browser", command=self.launch_browser
        )

        self.launch_button.grid(row=0, column=0, padx=(0, 10))

        self.verify_button = ttk.Button(
            frame, text="Verify Sites", command=self.verify_sites, state="disabled"
        )

        self.verify_button.grid(row=0, column=1)

    def build_site_status_frame(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Site Status",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        self.site_table = ttk.Treeview(
            frame,
            columns=("site", "status"),
            show="headings",
            height=len(SITES),
        )

        self.site_table.heading(
            "site",
            text="Site",
        )

        self.site_table.heading(
            "status",
            text="Status",
        )

        self.site_table.column(
            "site",
            width=220,
            anchor="w",
        )

        self.site_table.column(
            "status",
            width=500,
            anchor="w",
        )

        self.site_table.pack(
            fill="x",
        )

        for site in SITES:

            self.site_table.insert(
                "",
                "end",
                values=(
                    site,
                    "Not Checked",
                ),
            )

    def build_input_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Input / Output", padding=10)

        frame.pack(fill="x", pady=(0, 10))

        frame.columnconfigure(1, weight=1)

        # Excel File

        ttk.Label(frame, text="Excel File").grid(
            row=0,
            column=0,
            sticky="w",
        )

        ttk.Entry(
            frame,
            textvariable=self.excel_path,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
        )

        self.browse_excel_button = ttk.Button(
            frame,
            text="Browse",
            command=self.browse_excel,
        )

        self.browse_excel_button.grid(
            row=0,
            column=2,
        )

        # Output Folder

        ttk.Label(frame, text="Output Folder").grid(
            row=1,
            column=0,
            sticky="w",
            pady=(10, 0),
        )

        ttk.Entry(
            frame,
            textvariable=self.output_folder,
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=(10, 0),
        )

        self.browse_output_button = ttk.Button(
            frame,
            text="Browse",
            command=self.browse_output,
        )

        self.browse_output_button.grid(
            row=1,
            column=2,
            pady=(10, 0),
        )

    def build_progress_frame(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Progress",
            padding=10,
        )

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        ttk.Label(
            frame,
            text="Status:",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ttk.Label(
            frame,
            textvariable=self.status,
        ).grid(
            row=0,
            column=1,
            sticky="w",
        )

        ttk.Label(
            frame,
            text="Progress:",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        ttk.Label(
            frame,
            textvariable=self.progress,
        ).grid(
            row=1,
            column=1,
            sticky="w",
            pady=(8, 0),
        )

        ttk.Label(
            frame,
            text="Current:",
        ).grid(
            row=2,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        ttk.Label(
            frame,
            textvariable=self.current,
        ).grid(
            row=2,
            column=1,
            sticky="w",
            pady=(8, 0),
        )

        ttk.Label(
            frame,
            text="Elapsed:",
        ).grid(
            row=3,
            column=0,
            sticky="w",
            pady=(8, 0),
        )

        ttk.Label(
            frame,
            textvariable=self.elapsed,
        ).grid(
            row=3,
            column=1,
            sticky="w",
            pady=(8, 0),
        )

        self.progress_bar = ttk.Progressbar(
            frame,
            mode="determinate",
        )

        self.progress_bar.grid(
            row=4,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(15, 0),
        )

        frame.columnconfigure(
            1,
            weight=1,
        )

    def build_summary_frame(self, parent):

        frame = ttk.LabelFrame(
            parent,
            text="Summary",
            padding=10,
        )

        frame.pack(
            fill="both",
            expand=True,
            pady=(0, 10),
        )

        columns = (
            "site",
            "found",
            "not_found",
            "errors",
            "elapsed",
        )

        self.summary_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
            height=len(SITES),
        )

        self.summary_table.heading("site", text="Site")
        self.summary_table.heading("found", text="Found")
        self.summary_table.heading("not_found", text="Not Found")
        self.summary_table.heading("errors", text="Errors")
        self.summary_table.heading("elapsed", text="Elapsed")

        self.summary_table.column("site", width=220, anchor="w")
        self.summary_table.column("found", width=80, anchor="center")
        self.summary_table.column("not_found", width=90, anchor="center")
        self.summary_table.column("errors", width=80, anchor="center")
        self.summary_table.column("elapsed", width=120, anchor="center")

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.summary_table.yview,
        )

        self.summary_table.configure(
            yscrollcommand=scrollbar.set,
        )

        self.summary_table.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.summary_rows = {}

        for site in SITES:

            item = self.summary_table.insert(
                "",
                "end",
                values=(
                    site,
                    "-",
                    "-",
                    "-",
                    "Pending",
                ),
            )

            self.summary_rows[site] = item

    def build_buttons(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(fill="x")

        self.start_button = ttk.Button(
            frame, text="Start Sweep", command=self.start_sweep, state="disabled"
        )

        self.start_button.pack(side="right")

    def browse_excel(self):

        filename = filedialog.askopenfilename(
            title="Select Excel File", filetypes=[("Excel Workbook", "*.xlsx")]
        )

        if filename:

            self.excel_path.set(filename)

    def browse_output(self):

        folder = filedialog.askdirectory(title="Select Output Folder")

        if folder:

            self.output_folder.set(folder)

    def launch_browser(self):

        try:

            self.status.set("Launching Chrome for Testing...")

            self.root.update_idletasks()

            self.browser_service.launch()

            self.status.set("Browser ready. Please log in to each site.")

            self.verify_button.config(state="normal")

            messagebox.showinfo(
                "Browser Ready",
                (
                    "Chrome for Testing has been launched.\n\n"
                    "Please log in to all four sites,\n"
                    "then click 'Verify Sites'."
                ),
            )

        except Exception as ex:

            messagebox.showerror("Error", str(ex))

            self.status.set("Idle")

    def verify_sites(self):

        self.site_table.delete(*self.site_table.get_children())

        results = self.browser_service.verify_sites()

        all_ready = True

        for site, status in results:

            self.site_table.insert("", "end", values=(site, status))

            if status != "Ready":

                all_ready = False

        if all_ready:

            self.status.set("All sites are ready.")

            self.start_button.config(state="normal")

        else:

            self.status.set("One or more sites are not ready.")

            self.start_button.config(state="disabled")

    def start_sweep(self):

        excel_file = self.excel_path.get().strip()

        if not excel_file:
            messagebox.showwarning(
                "Missing Excel File",
                "Please select an Excel file.",
            )
            return

        output_folder = self.output_folder.get().strip()

        if not output_folder:
            messagebox.showwarning(
                "Missing Output Folder",
                "Please select an output folder.",
            )
            return

        for site, item in self.summary_rows.items():

            self.summary_table.item(
                item,
                values=(
                    site,
                    "-",
                    "-",
                    "-",
                    "Pending",
                ),
            )

        self.status.set("Starting...")
        self.progress.set("0 / 0")
        self.current.set("-")

        self.progress_bar["value"] = 0
        self.progress_bar["maximum"] = 1

        self.elapsed.set("00:00:00")

        self.start_timer()

        self.disable_controls()

        threading.Thread(
            target=self.run_sweep,
            daemon=True,
        ).start()

    def run_sweep(self):

        try:

            runner = SweepRunner(
                self.browser_service.driver,
                progress_callback=self.progress_callback,
            )

            runner.run(
                self.excel_path.get(),
                self.output_folder.get(),
            )

        except Exception as ex:

            logger.exception("Sweep failed.")

            error = str(ex)

            self.root.after(
                0,
                lambda: self.sweep_failed(error),
            )

    def progress_callback(self, **kwargs):

        self.root.after(0, lambda: self.update_progress(kwargs))

    def update_progress(self, event):

        event_type = event["event"]

        if event_type == EVENT_STAGE:

            self.status.set(event["status"])

            if event["status"] == "Completed":
                self.sweep_completed(event["output_file"])

            return

        if event_type == EVENT_SITE_START:

            site = event["site"]

            self.status.set(f"Searching {site}...")

            item = self.summary_rows.get(site)

            if item is not None:

                self.summary_table.item(
                    item,
                    values=(
                        site,
                        "-",
                        "-",
                        "-",
                        "Running...",
                    ),
                )

            return

        if event_type == EVENT_PROGRESS:

            self.progress.set(f'{event["current"]} / {event["total"]}')

            self.current.set(event["control_number"])

            self.progress_bar["maximum"] = event["total"]

            self.progress_bar["value"] = event["current"]

            return

        if event_type == EVENT_SITE_COMPLETE:

            self.append_summary(
                site=event["site"],
                found=event["found"],
                not_found=event["not_found"],
                errors=event["errors"],
                elapsed=event["elapsed"],
            )

    def append_summary(
        self,
        site: str,
        found: int,
        not_found: int,
        errors: int,
        elapsed: str,
    ):

        item = self.summary_rows.get(site)

        if item is None:
            return

        self.summary_table.item(
            item,
            values=(
                site,
                found,
                not_found,
                errors,
                elapsed,
            ),
        )

    def disable_controls(self):

        self.launch_button.config(state="disabled")

        self.verify_button.config(state="disabled")

        self.start_button.config(state="disabled")

        self.browse_excel_button.config(state="disabled")

        self.browse_output_button.config(state="disabled")

    def enable_controls(self):

        self.launch_button.config(state="normal")

        self.verify_button.config(state="normal")

        self.start_button.config(state="normal")

        self.browse_excel_button.config(state="normal")

        self.browse_output_button.config(state="normal")

    def sweep_completed(self, output_file):

        self.stop_timer()

        self.enable_controls()

        self.status.set("Completed")

        messagebox.showinfo(
            "Sweep Complete",
            f"Output saved to:\n\n{output_file}",
        )

    def sweep_failed(self, message):

        self.stop_timer()

        self.enable_controls()

        self.status.set("Failed")

        messagebox.showerror(
            "Sweep Failed",
            message,
        )

    def start_timer(self):

        self.timer_running = True
        self.timer_start = time.time()

        self.update_timer()

    def stop_timer(self):

        self.timer_running = False

    def update_timer(self):

        if not self.timer_running:
            return

        elapsed = int(time.time() - self.timer_start)

        hours, remainder = divmod(elapsed, 3600)
        minutes, seconds = divmod(remainder, 60)

        self.elapsed.set(f"{hours:02}:{minutes:02}:{seconds:02}")

        self.root.after(
            1000,
            self.update_timer,
        )
