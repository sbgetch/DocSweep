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

    WINDOW_BG = "#F4F6F9"
    CARD_BG = "#FFFFFF"

    # ==========================================================================
    # Text Colors
    # ==========================================================================

    TEXT = "#1F2937"
    MUTED = "#6B7280"

    # ==========================================================================
    # Border Colors
    # ==========================================================================

    BORDER = "#D9DDE3"

    # ==========================================================================
    # Status Colors
    # ==========================================================================

    SUCCESS = "#16A34A"
    WARNING = "#D97706"
    ERROR = "#DC2626"
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

    TITLE_FONT = ("Segoe UI", 24, "bold")
    SUBTITLE_FONT = ("Segoe UI", 10)

    HEADING_FONT = ("Segoe UI", 10, "bold")

    BODY_FONT = ("Segoe UI", 10)
    BODY_BOLD_FONT = ("Segoe UI", 10, "bold")

    SMALL_FONT = ("Segoe UI", 9)
    FOOTER_FONT = ("Segoe UI", 9)

    @staticmethod
    def configure(root):

        style = ttk.Style(root)

        style.theme_use("clam")

        # ======================================================================
        # Window
        # ======================================================================

        root.configure(
            background=Theme.WINDOW_BG,
        )

        # ======================================================================
        # General
        # ======================================================================

        style.configure(
            ".",
            font=Theme.BODY_FONT,
        )

        style.configure(
            "TFrame",
            background=Theme.CARD_BG,
        )

        style.configure(
            "TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT,
            font=Theme.BODY_FONT,
        )

        # ======================================================================
        # Label Styles
        # ======================================================================

        style.configure(
            "Heading.TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT,
            font=Theme.HEADING_FONT,
        )

        style.configure(
            "Muted.TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.MUTED,
            font=Theme.SUBTITLE_FONT,
        )

        style.configure(
            "Value.TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.PRIMARY,
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "Version.TLabel",
            background=Theme.WINDOW_BG,
            foreground=Theme.PRIMARY,
            font=("Segoe UI", 11, "bold"),
        )

        style.configure(
            "Success.TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.SUCCESS,
        )

        style.configure(
            "Warning.TLabel",
            background=Theme.CARD_BG,
            foreground=Theme.WARNING,
        )

        style.configure(
            "Error.TLabel",
            background=Theme.CARD_BG,
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
            bordercolor=Theme.BORDER,
        )

        style.configure(
            "Card.TLabelframe.Label",
            background=Theme.CARD_BG,
            foreground=Theme.TEXT,
            font=("Segoe UI", 10, "bold"),
        )

        # ======================================================================
        # Buttons
        # ======================================================================

        style.configure(
            "Primary.TButton",
            padding=(14, 8),
            font=("Segoe UI", 10, "bold"),
        )

        style.configure(
            "Secondary.TButton",
            padding=(12, 8),
            font=("Segoe UI", 10),
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
            background="white",
            fieldbackground="white",
            foreground=Theme.TEXT,
            rowheight=30,
            borderwidth=0,
            font=Theme.BODY_FONT,
        )

        style.configure(
            "Treeview.Heading",
            background=Theme.PRIMARY,
            foreground="white",
            font=("Segoe UI", 10, "bold"),
            relief="flat",
        )

        style.map(
            "Treeview.Heading",
            background=[
                ("active", Theme.PRIMARY_HOVER),
            ],
        )

        # ======================================================================
        # Progress Bar
        # ======================================================================

        style.configure(
            "Horizontal.TProgressbar",
            thickness=16,
            background=Theme.PRIMARY,
            troughcolor="#E5E7EB",
            borderwidth=0,
        )

        return style