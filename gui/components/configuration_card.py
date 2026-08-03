from tkinter import ttk

from gui.components.card import Card


class ConfigurationCard(Card):

    def __init__(
        self,
        parent,
        main_window,
    ):

        super().__init__(
            parent,
            title="📁 Configuration",
        )

        self.main_window = main_window

        self.build_ui()

    def build_ui(self):

        self.columnconfigure(1, weight=1)

        # ------------------------------------------------------------------
        # Excel File
        # ------------------------------------------------------------------

        ttk.Label(
            self,
            text="Excel File",
        ).grid(
            row=0,
            column=0,
            sticky="w",
        )

        ttk.Entry(
            self,
            textvariable=self.main_window.excel_path,
        ).grid(
            row=0,
            column=1,
            sticky="ew",
            padx=5,
        )

        self.main_window.browse_excel_button = ttk.Button(
            self,
            text="Browse",
            command=self.main_window.browse_excel,
            style="Secondary.TButton",
        )

        self.main_window.browse_excel_button.grid(
            row=0,
            column=2,
        )

        # ------------------------------------------------------------------
        # Separator
        # ------------------------------------------------------------------

        ttk.Separator(
            self,
            orient="horizontal",
        ).grid(
            row=1,
            column=0,
            columnspan=3,
            sticky="ew",
            pady=15,
        )

        # ------------------------------------------------------------------
        # Buttons
        # ------------------------------------------------------------------

        button_frame = ttk.Frame(self)

        button_frame.grid(
            row=2,
            column=0,
            columnspan=3,
            sticky="ew",
        )

        button_frame.columnconfigure(0, weight=1)
        button_frame.columnconfigure(1, weight=1)

        self.main_window.verify_button = ttk.Button(
            button_frame,
            text="Verify Sites",
            command=self.main_window.verify_sites,
            state="disabled",
            style="Secondary.TButton",
        )

        self.main_window.verify_button.grid(
            row=0,
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(0, 8),
        )

        self.main_window.start_button = ttk.Button(
            button_frame,
            text="Start Sweep",
            command=self.main_window.start_sweep,
            state="disabled",
            style="Primary.TButton",
        )

        self.main_window.start_button.grid(
            row=1,
            column=0,
            sticky="ew",
            padx=(0, 5),
        )

        self.main_window.cancel_button = ttk.Button(
            button_frame,
            text="Cancel Sweep",
            command=self.main_window.cancel_sweep,
            state="disabled",
        )

        self.main_window.cancel_button.grid(
            row=1,
            column=1,
            sticky="ew",
            padx=(5, 0),
        )
