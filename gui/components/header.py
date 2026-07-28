from tkinter import ttk

from gui.theme import Theme
from version import __version__


class Header(ttk.Frame):

    def __init__(self, parent):

        super().__init__(parent)

        self.configure(
            padding=(0, 0, 0, Theme.SPACE_LG),
        )

        self.columnconfigure(
            0,
            weight=1,
        )

        self.build_ui()

    def build_ui(self):

        # ------------------------------------------------------------------
        # Left
        # ------------------------------------------------------------------

        left = ttk.Frame(self)

        left.grid(
            row=0,
            column=0,
            sticky="w",
        )

        title = ttk.Label(
            left,
            text="DocSweep",
            font=Theme.TITLE_FONT,
        )

        title.pack(
            anchor="w",
        )

        subtitle = ttk.Label(
            left,
            text="Search multiple documentation repositories automatically.",
            style="Muted.TLabel",
        )

        subtitle.pack(
            anchor="w",
            pady=(2, 0),
        )

        # ------------------------------------------------------------------
        # Right
        # ------------------------------------------------------------------

        right = ttk.Frame(self)

        right.grid(
            row=0,
            column=1,
            sticky="e",
        )

        version = ttk.Label(
            right,
            text=f"v{__version__}",
            style="Heading.TLabel",
        )

        version.pack(
            anchor="e",
        )