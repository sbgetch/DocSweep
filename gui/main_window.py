import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from gui.theme import Theme
from gui.components import Header
from gui.components import ConfigurationCard
from gui.components import ConnectedSitesCard
from gui.components import ProgressCard
from gui.components import LogsCard
from gui.components import SummaryCard

from services.sweep_runner import SweepRunner
from services.browser_service import BrowserService

from utils.logger import get_logger
from utils.constants import (
    LOG_INFO,
    LOG_ACTIVITY,
    LOG_SUCCESS,
    LOG_WARNING,
    LOG_ERROR,
    SITES,
    SITE_STATUS_NOT_CHECKED,
    SITE_STATUS_VERIFYING,
    SITE_STATUS_READY,
    SITE_STATUS_RUNNING,
    SITE_STATUS_COMPLETED,
    SITE_STATUS_ERROR,
)
from utils.events import (
    EVENT_PROGRESS,
    EVENT_SITE_PROGRESS,
    EVENT_SITE_COMPLETE,
    EVENT_SITE_START,
    EVENT_STAGE,
    EVENT_SWEEP_COMPLETE,
    EVENT_SWEEP_CANCELLED,
)

logger = get_logger(__name__)

from version import __version__


class MainWindow:

    WINDOW_WIDTH = 850
    WINDOW_HEIGHT = 800

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(self):

        self.cancel_event = threading.Event()

        self.sweep_running = False

        self.exit_after_cancel = False

        self.root = tk.Tk()

        self.root.title(f"DocSweep v{__version__}")

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

        Theme.configure(self.root)

        self.browser_service = BrowserService()

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

    # =============================================================================
    # UI BUILDERS
    # =============================================================================

    def build_ui(self):

        container = ttk.Frame(
            self.root,
            padding=15,
        )

        container.pack(
            fill="both",
            expand=True,
        )

        self.build_header(container)

        self.build_dashboard_top(container)

        self.build_dashboard_center(container)

        self.build_dashboard_bottom(container)

        self.build_footer(container)

    def build_header(self, parent):

        self.header = Header(parent)

        self.header.pack(
            fill="x",
            pady=(0, 15),
        )

    def build_dashboard_top(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.build_configuration_card(frame)

        self.build_connected_sites_card(frame)

    def build_dashboard_center(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="both",
            expand=True,
            pady=(0, 10),
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.build_progress_card(frame)

        self.build_logs_card(frame)

    def build_dashboard_bottom(self, parent):

        self.build_summary_card(parent)

    def build_footer(self, parent):

        separator = ttk.Separator(
            parent,
            orient="horizontal",
        )

        separator.pack(
            fill="x",
            pady=(5, 8),
        )

        frame = ttk.Frame(parent)

        frame.pack(fill="x")

        self.footer_status = tk.StringVar(value="Ready")

        self.create_label(
            frame,
            textvariable=self.footer_status,
        ).pack(
            side="left",
        )

        self.footer_time = tk.StringVar()

        self.create_label(
            frame,
            textvariable=self.footer_time,
        ).pack(
            side="right",
        )

        self.update_clock()

    # =============================================================================
    # UI BUILDERS - WRAPPERS
    # =============================================================================

    def build_configuration_card(self, parent):

        self.configuration_card = ConfigurationCard(
            parent,
            self,
        )

        self.configuration_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
        )

    def build_connected_sites_card(self, parent):

        self.connected_sites_card = ConnectedSitesCard(
            parent,
            self,
        )

        self.connected_sites_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
        )

    def build_progress_card(self, parent):

        self.progress_card = ProgressCard(
            parent,
            self,
        )

        self.progress_card.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
        )

    def build_logs_card(self, parent):

        self.logs_card = LogsCard(
            parent,
            self,
        )

        self.logs_card.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
        )

    def build_summary_card(self, parent):

        self.summary_card = SummaryCard(
            parent,
            self,
        )

        self.summary_card.pack(
            fill="both",
            expand=True,
            pady=(0, 10),
        )

    # =========================================================================
    # Widget Factory
    # =========================================================================

    def create_label(
        self,
        parent,
        text=None,
        textvariable=None,
        **kwargs,
    ):

        return ttk.Label(
            parent,
            text=text,
            textvariable=textvariable,
            **kwargs,
        )

    def create_entry(
        self,
        parent,
        textvariable,
        **kwargs,
    ):

        return ttk.Entry(
            parent,
            textvariable=textvariable,
            **kwargs,
        )

    def create_button(
        self,
        parent,
        text,
        command,
        style="Secondary.TButton",
        **kwargs,
    ):

        return ttk.Button(
            parent,
            text=text,
            command=command,
            style=style,
            **kwargs,
        )

    def create_labelFrame(
        self,
        parent,
        text,
        padding=10,
        **kwargs,
    ):

        return ttk.LabelFrame(
            parent,
            text=text,
            padding=padding,
            **kwargs,
        )

    # =========================================================================
    # User Actions
    # =========================================================================

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

            self.set_status("Launching Chrome for Testing...")

            self.root.update_idletasks()

            self.browser_service.launch()

            self.set_status("Browser ready. Please log in to each site.")

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

            self.set_status("Idle")

    def verify_sites(self):

        for site in SITES:

            self.update_site_status(
                site,
                SITE_STATUS_VERIFYING,
            )

        self.root.update_idletasks()

        results = self.browser_service.verify_sites()

        all_ready = True

        for site, status in results:

            self.update_site_status(
                site,
                status,
            )

            if status != SITE_STATUS_READY:

                all_ready = False

        if all_ready:

            self.set_status("All sites are ready.")

            self.start_button.config(
                state="normal",
            )

        else:

            self.set_status(
                "One or more sites are not ready.",
            )

            self.start_button.config(
                state="disabled",
            )

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

        self.clear_summary()

        for site in SITES:

            self.update_site_status(
                site,
                SITE_STATUS_READY,
            )

        self.set_status("Starting...")

        self.reset_progress()

        self.clear_logs()

        self.start_timer()

        self.disable_controls()

        self.sweep_running = True

        self.cancel_event.clear()

        threading.Thread(
            target=self.run_sweep,
            daemon=True,
        ).start()

    def run_sweep(self):

        try:

            runner = SweepRunner(
                self.browser_service.driver,
                progress_callback=self.progress_callback,
                log_callback=self.log_callback,
                cancel_event=self.cancel_event,
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

    def cancel_sweep(self, exit_after_cancel=False):

        if self.cancel_event.is_set():

            return

        confirmed = messagebox.askyesno(
            "Cancel Sweep",
            (
                "Are you sure you want to cancel the current sweep?\n\n"
                "The current document will finish processing.\n"
                "Partial results will be saved."
            ),
        )

        if not confirmed:

            return

        self.exit_after_cancel = exit_after_cancel

        self.cancel_event.set()

        self.cancel_button.config(state="disabled")

        self.set_status("Cancelling...")

        self.append_log(
            "Cancellation requested by user...",
            LOG_WARNING,
        )

    def on_close(self):

        if not self.sweep_running:

            self.root.destroy()

            return

        self.cancel_sweep(
            exit_after_cancel=True,
        )

    def log_callback(self, message: str):

        self.root.after(
            0,
            lambda: self.append_log(message),
        )

    # =========================================================================
    # Progress Events
    # =========================================================================

    def progress_callback(self, **kwargs):

        self.root.after(0, lambda: self.update_progress(kwargs))

    def update_progress(self, event):

        event_type = event["event"]

        if event_type == EVENT_STAGE:

            self.set_status(event["status"])

            return

        if event_type == EVENT_SITE_START:

            site = event["site"]

            self.update_site_status(
                site,
                SITE_STATUS_RUNNING,
            )

            self.set_status(f"Searching {site}...")

            item = self.summary_rows.get(site)

            if item is not None:

                self.summary_table.item(
                    item,
                    values=(
                        site,
                        "-",
                        "-",
                        "-",
                        "-",
                        SITE_STATUS_RUNNING,
                    ),
                )

            return

        if event_type == EVENT_PROGRESS:

            self.progress.set(f'{event["current"]} / {event["total"]}')

            self.current.set(event["control_number"])

            self.progress_bar["maximum"] = event["total"]

            self.progress_bar["value"] = event["current"]

            return

        if event_type == EVENT_SITE_PROGRESS:

            item = self.summary_rows.get(
                event["site"],
            )

            if item is not None:

                self.summary_table.item(
                    item,
                    values=(
                        event["site"],
                        event["found"],
                        event["not_found"],
                        event["errors"],
                        "-",
                        SITE_STATUS_RUNNING,
                    ),
                )

            return

        if event_type == EVENT_SITE_COMPLETE:

            status = SITE_STATUS_COMPLETED

            if event["errors"] > 0:

                status = SITE_STATUS_ERROR

            self.update_site_status(
                event["site"],
                status,
            )

            self.append_summary(
                site=event["site"],
                found=event["found"],
                not_found=event["not_found"],
                errors=event["errors"],
                elapsed=event["elapsed"],
            )

            return

        if event_type == EVENT_SWEEP_COMPLETE:

            self.sweep_completed(
                event["output_file"],
            )

            return

        if event_type == EVENT_SWEEP_CANCELLED:

            self.sweep_cancelled(
                event["output_file"],
            )

            return

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

        status = SITE_STATUS_COMPLETED

        if errors > 0:
            status = "Completed with Errors"

        self.summary_table.item(
            item,
            values=(
                site,
                found,
                not_found,
                errors,
                elapsed,
                status,
            ),
        )

    # =========================================================================
    # UI State
    # =========================================================================

    def disable_controls(self):

        self.launch_button.config(state="disabled")

        self.verify_button.config(state="disabled")

        self.start_button.config(state="disabled")

        self.cancel_button.config(state="normal")

        self.browse_excel_button.config(state="disabled")

        self.browse_output_button.config(state="disabled")

    def enable_controls(self):

        self.launch_button.config(state="normal")

        self.verify_button.config(state="normal")

        self.start_button.config(state="normal")

        self.cancel_button.config(state="normal")

        self.browse_excel_button.config(state="normal")

        self.browse_output_button.config(state="normal")

    def sweep_completed(self, output_file):

        self.sweep_running = False

        self.exit_after_cancel = False

        self.stop_timer()

        self.enable_controls()

        self.set_status(SITE_STATUS_COMPLETED)

        messagebox.showinfo(
            "Sweep Complete",
            f"Output saved to:\n\n{output_file}",
        )

    def sweep_cancelled(self, output_file):

        self.sweep_running = False

        self.exit_after_cancel = False

        self.stop_timer()

        self.enable_controls()

        self.set_status("Cancelled")

        messagebox.showinfo(
            "Sweep Cancelled",
            "The sweep was cancelled.\n\n"
            "Partial results were saved to:\n\n"
            f"{output_file}",
        )

        if self.exit_after_cancel:

            self.root.destroy()

    def sweep_failed(self, message):

        self.sweep_running = False

        self.exit_after_cancel = False

        self.stop_timer()

        self.enable_controls()

        self.set_status("Failed")

        messagebox.showerror(
            "Sweep Failed",
            message,
        )

    def append_log(
        self,
        message,
        level=LOG_INFO,
    ):

        timestamp = time.strftime("%H:%M:%S")

        self.log_text.configure(
            state="normal",
        )

        self.log_text.insert(
            "end",
            f"[{timestamp}] ",
            LOG_INFO,
        )

        self.log_text.insert(
            "end",
            f"{message}\n",
            level,
        )

        self.log_text.see("end")

        self.log_text.configure(
            state="disabled",
        )

    def finish_sweep(self):

        self.stop_timer()

        self.enable_controls()

    # =========================================================================
    # UI Helpers
    # =========================================================================

    def set_status(self, status: str):

        self.status.set(status)

        if hasattr(self, "footer_status"):
            self.footer_status.set(status)

        if hasattr(self, "log_text"):
            self.append_log(status)

    def reset_progress(self):

        self.progress.set("0 / 0")

        self.current.set("-")

        self.progress_bar["maximum"] = 1

        self.progress_bar["value"] = 0

        self.elapsed.set("00:00:00")

    def clear_summary(self):

        for site, item in self.summary_rows.items():

            self.summary_table.item(
                item,
                values=(
                    site,
                    "-",
                    "-",
                    "-",
                    "-",
                    "Pending",
                ),
            )

    def clear_logs(self):

        self.log_text.configure(state="normal")

        self.log_text.delete("1.0", tk.END)

        self.log_text.configure(state="disabled")

    def update_site_status(
        self,
        site,
        status,
    ):

        label = self.site_status_labels.get(site)

        if label is None:
            return

        color_map = {
            SITE_STATUS_NOT_CHECKED: "#808080",
            SITE_STATUS_VERIFYING: "#D97706",
            SITE_STATUS_READY: "#16A34A",
            SITE_STATUS_RUNNING: "#2563EB",
            SITE_STATUS_COMPLETED: "#15803D",
            SITE_STATUS_ERROR: "#DC2626",
        }

        label.configure(
            text=f"● {status}",
            foreground=color_map.get(
                status,
                "#808080",
            ),
        )

    # =========================================================================
    # Timer
    # =========================================================================

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

    def update_clock(self):

        current_time = time.strftime("%I:%M:%S %p")

        self.footer_time.set(current_time)

        self.root.after(
            1000,
            self.update_clock,
        )
