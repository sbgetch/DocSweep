from tkinter import ttk

from gui.components.card import Card


class ProgressCard(Card):

    def __init__(
        self,
        parent,
        main_window,
    ):

        super().__init__(
            parent,
            title="Sweep Progress",
        )

        self.main_window = main_window

        self.build_ui()

    def build_ui(self):

        self.columnconfigure(
            1,
            weight=1,
        )

        labels = (
            ("Status", self.main_window.status),
            ("Progress", self.main_window.progress),
            ("Control Number", self.main_window.current),
            ("Elapsed", self.main_window.elapsed),
        )

        for row, (title, variable) in enumerate(labels):

            ttk.Label(
                self,
                text=f"{title}:",
            ).grid(
                row=row,
                column=0,
                sticky="w",
                pady=5,
            )

            ttk.Label(
                self,
                textvariable=variable,
            ).grid(
                row=row,
                column=1,
                sticky="w",
                padx=(10, 0),
                pady=5,
            )

        self.main_window.progress_bar = ttk.Progressbar(
            self,
            mode="determinate",
        )

        self.main_window.progress_bar.grid(
            row=len(labels),
            column=0,
            columnspan=2,
            sticky="ew",
            pady=(20, 0),
        )