import time
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from gui.theme import Theme

from services.sweep_runner import SweepRunner
from services.browser_service import BrowserService

from utils.logger import get_logger
from utils.constants import SITES
from utils.events import (
    EVENT_PROGRESS,
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
    WINDOW_HEIGHT = 750

    # =========================================================================
    # Initialization
    # =========================================================================

    def __init__(self):

        self.cancel_event = threading.Event()

        self.sweep_running = False

        self.exit_after_cancel = False

        self.root = tk.Tk()

        self.root.protocol(
            "WM_DELETE_WINDOW",
            self.on_close,
        )

        Theme.configure(self.root)

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

        self.build_upper_section(container)

        self.build_middle_section(container)

        self.build_lower_section(container)

        self.build_footer(container)

    def build_header(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            pady=(0, 15),
        )

        frame.columnconfigure(0, weight=1)

        title_frame = ttk.Frame(frame)
        title_frame.grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.create_label(
            title_frame,
            text="DocSweep",
            style="Header.TLabel",
        ).pack(anchor="w")

        self.create_label(
            title_frame,
            text="Search multiple documentation repositories automatically.",
            style="Subtitle.TLabel",
        ).pack(anchor="w", pady=(2, 0))

        version_frame = ttk.Frame(frame)

        version_frame.grid(
            row=0,
            column=1,
            sticky="e",
        )

        self.create_label(
            version_frame,
            text=f"v{__version__}",
            style="Subtitle.TLabel",
        ).pack(anchor="e")

    def build_upper_section(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(
            fill="x",
            pady=(0, 10),
        )

        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=1)

        self.build_configuration_card(frame)

        self.build_connected_sites_card(frame)

    def build_middle_section(self, parent):

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

    def build_lower_section(self, parent):

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

        frame = self.create_labelFrame(
            parent,
            text="Configuration",
            padding=10,
            style="Card.TLabelframe",
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
        )

        frame.columnconfigure(1, weight=1)

        # Excel File

        self.create_label(
            frame,
            text="Excel File",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        self.create_entry(
            frame,
            textvariable=self.excel_path,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
        )

        self.browse_excel_button = self.create_button(
            frame,
            text="Browse",
            command=self.browse_excel,
            style="Secondary.TButton",
        )

        self.browse_excel_button.grid(
            row=0,
            column=2,
        )

        # Output Folder

        self.create_label(
            frame,
            text="Output Folder",
        ).grid(
            row=1,
            column=0,
            sticky="w",
            pady=(10, 0),
        )

        self.create_entry(
            frame,
            textvariable=self.output_folder,
        ).grid(
            row=1,
            column=1,
            sticky="ew",
            padx=5,
            pady=(10, 0),
        )

        self.browse_output_button = self.create_button(
            frame,
            text="Browse",
            command=self.browse_output,
            style="Secondary.TButton",
        )

        self.browse_output_button.grid(
            row=1,
            column=2,
            pady=(10, 0),
        )

        ttk.Separator(
            frame,
            orient="horizontal",
        ).grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=15,
        )

        button_frame = ttk.Frame(frame)

        button_frame.grid(
            row=3,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.verify_button = self.create_button(
            button_frame,
            text="Verify Sites",
            command=self.verify_sites,
            state="disabled",
            style="Secondary.TButton",
        )

        self.verify_button.grid(
            row=0,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        self.start_button = self.create_button(
            button_frame,
            text="Start Sweep",
            command=self.start_sweep,
            state="disabled",
            style="Primary.TButton",
        )

        self.start_button.grid(
            row=0,
            column=1,
            sticky="ew",
            padx=(5, 0),
        )

        self.cancel_button = self.create_button(
            button_frame,
            text="Cancel Sweep",
            command=self.cancel_sweep,
            state="disabled",
        )

        self.cancel_button.pack(
            side="left",
            padx=(10, 0),
        )

    def build_connected_sites_card(self, parent):

        frame = self.create_labelFrame(
            parent,
            text="Connected Sites",
            padding=10,
            style="Card.TLabelframe",
        )

        frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
        )

        frame.columnconfigure(1, weight=1)

        self.site_status_labels = {}

        for row, site in enumerate(SITES):

            self.create_label(
                frame,
                text=site,
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=6,
            )

            status = self.create_label(
                frame,
                text="● Not Checked",
            )

            status.grid(
                row=row,
                column=1,
                sticky="e",
                pady=6,
            )

            self.site_status_labels[site] = status

    def build_progress_card(self, parent):

        frame = self.create_labelFrame(
            parent,
            text="Sweep Progress",
            padding=10,
            style="Card.TLabelframe",
        )

        frame.grid(
            row=0,
            column=0,
            sticky="nsew",
            padx=(0, 5),
        )

        frame.columnconfigure(1, weight=1)

        labels = (
            ("Status", self.status),
            ("Progress", self.progress),
            ("Control Number", self.current),
            ("Elapsed", self.elapsed),
        )

        for row, (title, variable) in enumerate(labels):

            self.create_label(
                frame,
                text=f"{title}:",
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=5,
            )

            self.create_label(
                frame,
                textvariable=variable,
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=(10, 0),
                pady=5,
            )

        self.progress_bar = ttk.Progressbar(
            frame,
            mode="determinate",
        )

        self.progress_bar.grid(
            row=len(labels),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 0),
        )

    def build_logs_card(self, parent):

        frame = self.create_labelFrame(
            parent,
            text="Logs",
            padding=10,
            style="Card.TLabelframe",
        )

        frame.grid(
            row=0,
            column=1,
            sticky="nsew",
            padx=(5, 0),
        )

        self.log_text = tk.Text(
            frame,
            height=10,
            state="disabled",
            wrap="word",
        )

        scrollbar = ttk.Scrollbar(
            frame,
            orient="vertical",
            command=self.log_text.yview,
        )

        self.log_text.configure(
            yscrollcommand=scrollbar.set,
        )

        self.log_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

    def build_summary_card(self, parent):

        frame = self.create_labelFrame(
            parent,
            text="Summary",
            padding=10,
            style="Card.TLabelframe",
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
            "status",
        )

        self.summary_table = ttk.Treeview(
            frame,
            columns=columns,
            show="headings",
        )

        headings = {
            "site": "Site",
            "found": "Found",
            "not_found": "Not Found",
            "errors": "Errors",
            "elapsed": "Elapsed",
            "status": "Status",
        }

        widths = {
            "site": 220,
            "found": 70,
            "not_found": 90,
            "errors": 70,
            "elapsed": 110,
            "status": 120,
        }

        for column in columns:

            self.summary_table.heading(
                column,
                text=headings[column],
            )

            self.summary_table.column(
                column,
                width=widths[column],
                anchor="center" if column != "site" else "w",
            )

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
                    "-",
                    "Pending",
                ),
            )

            self.summary_rows[site] = item

    # =========================================================================
    # Widget Factory
    # =========================================================================

    def create_label(
        self,
        parent,
        text=None,
        textvariable=None,
        row=0,
        column=0,
        **kwargs,
    ):

        label = ttk.Label(
            parent,
            text=text,
            textvariable=textvariable,
            **kwargs,
        )

        label.grid(
            row=row,
            column=column,
            sticky="w",
            padx=5,
            pady=5,
        )

        return label

    def create_entry(
        self,
        parent,
        variable,
        row,
    ):

        entry = ttk.Entry(
            parent,
            textvariable=variable,
        )

        entry.grid(
            row=row,
            column=1,
            sticky="ew",
            padx=5,
            pady=5,
        )

        return entry

    def create_button(
        self,
        parent,
        text,
        command,
        row,
        column,
        style="Secondary.TButton",
        **kwargs,
    ):

        button = ttk.Button(
            parent,
            text=text,
            command=command,
            style=style,
            **kwargs,
        )

        button.grid(
            row=row,
            column=column,
            padx=5,
            pady=5,
            sticky="ew",
        )

        return button

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

        results = self.browser_service.verify_sites()

        all_ready = True

        for site, status in results:

            label = self.site_status_labels[site]

            label.config(
                text=f"● {status}",
            )

            if status != "Ready":
                all_ready = False

        if all_ready:

            self.set_status("All sites are ready.")

            self.start_button.config(state="normal")

        else:

            self.set_status("One or more sites are not ready.")

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
                    "-",
                    "Pending",
                ),
            )

        self.clear_summary()

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

        self.append_log("Cancellation requested by user...")

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
                        "Running",
                    ),
                )

            return

        if event_type == EVENT_PROGRESS:

            self.progress.set(
                f'{event["current"]} / {event["total"]}'
            )

            self.current.set(
                event["control_number"]
            )

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

        status = "Completed"

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

        self.set_status("Completed")

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

    def append_log(self, message):

        timestamp = time.strftime("%H:%M:%S")

        self.log_text.configure(state="normal")

        self.log_text.insert(
            "end",
            f"[{timestamp}] {message}\n",
        )

        self.log_text.see("end")

        self.log_text.configure(state="disabled")

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
