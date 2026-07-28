from tkinter import ttk

from gui.components.card import Card
from utils.constants import SITES


class SummaryCard(Card):

    def __init__(
        self,
        parent,
        main_window,
    ):

        super().__init__(
            parent,
            title="📋 Summary",
        )

        self.main_window = main_window

        self.build_ui()

    def build_ui(self):

        columns = (
            "site",
            "found",
            "not_found",
            "errors",
            "elapsed",
            "status",
        )

        self.main_window.summary_table = ttk.Treeview(
            self,
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

            self.main_window.summary_table.heading(
                column,
                text=headings[column],
            )

            self.main_window.summary_table.column(
                column,
                width=widths[column],
                anchor="center" if column != "site" else "w",
            )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.main_window.summary_table.yview,
        )

        self.main_window.summary_table.configure(
            yscrollcommand=scrollbar.set,
        )

        self.main_window.summary_table.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )

        self.main_window.summary_rows = {}

        for site in SITES:

            item = self.main_window.summary_table.insert(
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

            self.main_window.summary_rows[site] = item