from tkinter import ttk

from gui.components.card import Card
from utils.constants import SITES


class ConnectedSitesCard(Card):

    def __init__(
        self,
        parent,
        main_window,
    ):

        super().__init__(
            parent,
            title="Connected Sites",
        )

        self.main_window = main_window

        self.build_ui()

    def build_ui(self):

        self.columnconfigure(
            1,
            weight=1,
        )

        self.main_window.site_status_labels = {}

        for row, site in enumerate(SITES):

            ttk.Label(
                self,
                text=site,
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=6,
            )

            status = ttk.Label(
                self,
                text="● Not Checked",
            )

            status.grid(
                row=row,
                column=1,
                sticky="e",
                pady=6,
            )

            self.main_window.site_status_labels[site] = status