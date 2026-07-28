from tkinter import ttk


class Theme:

    # ==========================================================================
    # Brand Colors
    # ==========================================================================

    PRIMARY = "#FE5B1B"
    PRIMARY_HOVER = "#E65116"

    # ==========================================================================
    # Background Colors
    # ==========================================================================

    WINDOW_BG = "#F5F6F8"
    CARD_BG = "#FFFFFF"

    # ==========================================================================
    # Text Colors
    # ==========================================================================

    TEXT = "#222222"
    MUTED = "#6B7280"
    TEXT_SECONDARY = "#6B7280"
    TEXT_DISABLED = "#9CA3AF"

    # ==========================================================================
    # Border Colors
    # ==========================================================================

    BORDER = "#D9D9D9"
    DIVIDER = "#E5E7EB"

    # ==========================================================================
    # Status Colors
    # ==========================================================================

    SUCCESS = "#2E9E44"
    WARNING = "#F4B400"
    ERROR = "#D93025"
    INFO = "#2563EB"

    # ==========================================================================
    # Spacing
    # ==========================================================================

    SPACE_XS = 4
    SPACE_SM = 8
    SPACE_MD = 12
    SPACE_LG = 16
    SPACE_XL = 24
    SPACE_XXL = 32

    # ==========================================================================
    # Fonts
    # ==========================================================================

    TITLE_FONT = ("Calibri", 22, "bold")
    SUBTITLE_FONT = ("Calibri", 10)

    HEADING_FONT = ("Calibri", 11, "bold")

    BODY_FONT = ("Calibri", 10)
    BODY_BOLD_FONT = ("Calibri", 10, "bold")

    SMALL_FONT = ("Calibri", 9)
    FOOTER_FONT = ("Calibri", 8)

    @staticmethod
    def configure(root):

        style = ttk.Style(root)

        style.theme_use("clam")

        # ======================================================================
        # General
        # ======================================================================

        style.configure(
            ".",
            font=Theme.BODY_FONT,
        )

        style.configure(
            "TFrame",
            background=Theme.WINDOW_BG,
        )

        style.configure(
            "TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.TEXT,
        )

        # ======================================================================
        # Custom Label Styles
        # ======================================================================

        style.configure(
            "Heading.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.TEXT,
            font=Theme.HEADING_FONT,
        )

        style.configure(
            "Muted.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.MUTED,
        )

        style.configure(
            "Success.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.SUCCESS,
        )

        style.configure(
            "Warning.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.WARNING,
        )

        style.configure(
            "Error.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.ERROR,
        )

        # ======================================================================
        # Cards
        # ======================================================================

        style.configure(
            "Card.TLabelframe",
            background=Theme.CARD_BG,
            borderwidth=1,
            relief="solid",
            padding=Theme.SPACE_LG,
        )

        style.configure(
            "Card.TLabelframe.Label",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT,
            font=Theme.HEADING_FONT,
        )

        # ======================================================================
        # Buttons
        # ======================================================================

        style.configure(
            "Primary.TButton",
            padding=(14, 8),
            font=Theme.HEADING_FONT,
            foreground="white",
        )

        style.map(
            "Primary.TButton",
            background=[
                ("active", Theme.PRIMARY_HOVER),
                ("!disabled", Theme.PRIMARY),
            ],
        )

        style.configure(
            "Secondary.TButton",
            padding=(12, 8),
        )

        # ======================================================================
        # Entry
        # ======================================================================

        style.configure(
            "TEntry",
            padding=6,
        )

        # ======================================================================
        # Treeview
        # ======================================================================

        style.configure(
            "Treeview",
            rowheight=34,
            borderwidth=0,
        )

        style.configure(
            "Treeview.Heading",
            font=Theme.HEADING_FONT,
        )

        # ======================================================================
        # Progress Bar
        # ======================================================================

        style.configure(
            "Horizontal.TProgressbar",
            thickness=14,
        )

        return style