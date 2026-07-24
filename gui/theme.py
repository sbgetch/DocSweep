from tkinter import ttk


class Theme:

    # Colors
    PRIMARY = "#FE5B1B"

    BACKGROUND = "#F5F6F8"

    CARD = "#FFFFFF"

    BORDER = "#D9D9D9"

    TEXT = "#222222"

    MUTED = "#6B7280"

    SUCCESS = "#2E9E44"

    WARNING = "#F4B400"

    ERROR = "#D93025"

    # Fonts
    TITLE_FONT = ("Calibri", 22, "bold")

    SUBTITLE_FONT = ("Calibri", 10)

    HEADING_FONT = ("Calibri", 11, "bold")

    BODY_FONT = ("Calibri", 10)

    FOOTER_FONT = ("Calibri", 9)

    @staticmethod
    def configure(root):

        style = ttk.Style(root)

        style.theme_use("clam")

        # -------------------------------------------------------------------------
        # General
        # -------------------------------------------------------------------------

        style.configure(
            ".",
            font=Theme.BODY_FONT,
        )

        style.configure(
            "TFrame",
            background=Theme.BACKGROUND,
        )

        style.configure(
            "TLabel",
            background=Theme.BACKGROUND,
            foreground=Theme.TEXT,
        )

        # -------------------------------------------------------------------------
        # Card
        # -------------------------------------------------------------------------

        style.configure(
            "Card.TLabelframe",
            padding=12,
        )

        style.configure(
            "Card.TLabelframe.Label",
            font=Theme.HEADING_FONT,
        )

        # -------------------------------------------------------------------------
        # Buttons
        # -------------------------------------------------------------------------

        style.configure(
            "Primary.TButton",
            padding=(14, 8),
            font=Theme.HEADING_FONT,
        )

        style.configure(
            "Secondary.TButton",
            padding=(12, 8),
        )

        # -------------------------------------------------------------------------
        # Treeview
        # -------------------------------------------------------------------------

        style.configure(
            "Treeview",
            rowheight=30,
        )

        style.configure(
            "Treeview.Heading",
            font=Theme.HEADING_FONT,
        )

        # -------------------------------------------------------------------------
        # Progressbar
        # -------------------------------------------------------------------------

        style.configure(
            "Horizontal.TProgressbar",
            thickness=14,
        )

        return style
