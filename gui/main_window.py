import tkinter as tk
from tkinter import filedialog, messagebox, ttk

from services.browser_service import BrowserService
from version import __version__


class MainWindow:

    WINDOW_WIDTH = 850
    WINDOW_HEIGHT = 700

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

        self.build_ui()

    def run(self):

        self.root.mainloop()

    # --------------------------------------------------

    def build_ui(self):

        container = ttk.Frame(self.root, padding=15)

        container.pack(fill="both", expand=True)

        self.build_preparation_frame(container)

        self.build_site_status_frame(container)

        self.build_input_frame(container)

        self.build_progress_frame(container)

        self.build_summary_frame(container)

        self.build_buttons(container)

    # --------------------------------------------------

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

    # --------------------------------------------------

    def build_site_status_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Site Status", padding=10)

        frame.pack(fill="x", pady=(0, 10))

        self.site_table = ttk.Treeview(
            frame, columns=("site", "status"), show="headings", height=4
        )

        self.site_table.heading("site", text="Site")

        self.site_table.heading("status", text="Status")

        self.site_table.column("site", width=220, anchor="w")

        self.site_table.column("status", width=500, anchor="w")

        self.site_table.pack(fill="x")

        for site in ("Vertiv", "Asset Library", "PD Cloud", "MASW"):

            self.site_table.insert("", "end", values=(site, "Not Checked"))

    # --------------------------------------------------

    def build_input_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Input / Output", padding=10)

        frame.pack(fill="x", pady=(0, 10))

        frame.columnconfigure(1, weight=1)

        ttk.Label(frame, text="Excel File").grid(row=0, column=0, sticky="w")

        ttk.Entry(frame, textvariable=self.excel_path).grid(
            row=0, column=1, sticky="ew", padx=5
        )

        ttk.Button(frame, text="Browse", command=self.browse_excel).grid(
            row=0, column=2
        )

        ttk.Label(frame, text="Output Folder").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

        ttk.Entry(frame, textvariable=self.output_folder).grid(
            row=1, column=1, sticky="ew", padx=5, pady=(10, 0)
        )

        ttk.Button(frame, text="Browse", command=self.browse_output).grid(
            row=1, column=2, pady=(10, 0)
        )

    # --------------------------------------------------

    def build_progress_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Progress", padding=10)

        frame.pack(fill="x", pady=(0, 10))

        ttk.Label(frame, text="Status:").grid(row=0, column=0, sticky="w")

        ttk.Label(frame, textvariable=self.status).grid(row=0, column=1, sticky="w")

        ttk.Label(frame, text="Progress:").grid(
            row=1, column=0, sticky="w", pady=(10, 0)
        )

        ttk.Label(frame, textvariable=self.progress).grid(
            row=1, column=1, sticky="w", pady=(10, 0)
        )

        ttk.Label(frame, text="Current:").grid(
            row=2, column=0, sticky="w", pady=(10, 0)
        )

        ttk.Label(frame, textvariable=self.current).grid(
            row=2, column=1, sticky="w", pady=(10, 0)
        )

        self.progress_bar = ttk.Progressbar(frame, mode="determinate")

        self.progress_bar.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(15, 0))

        frame.columnconfigure(1, weight=1)

    # --------------------------------------------------

    def build_summary_frame(self, parent):

        frame = ttk.LabelFrame(parent, text="Summary", padding=10)

        frame.pack(fill="both", expand=True, pady=(0, 10))

        self.summary = tk.Text(frame, height=10, state="disabled")

        self.summary.pack(fill="both", expand=True)

    # --------------------------------------------------

    def build_buttons(self, parent):

        frame = ttk.Frame(parent)

        frame.pack(fill="x")

        self.start_button = ttk.Button(frame, text="Start Sweep", state="disabled")

        self.start_button.pack(side="right")

    # --------------------------------------------------

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

    # --------------------------------------------------

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

    # --------------------------------------------------

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
