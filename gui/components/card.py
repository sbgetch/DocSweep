from tkinter import ttk

from gui.theme import Theme


class Card(ttk.LabelFrame):
    """
    Reusable dashboard card.

    Example:

        config_card = Card(
            parent,
            title="1. Configuration",
        )
    """

    def __init__(
        self,
        parent,
        title,
        padding=None,
        **kwargs,
    ):

        super().__init__(
            parent,
            text=title,
            style="Card.TLabelframe",
            padding=padding or Theme.SPACE_LG,
            **kwargs,
        )

        # Give every card a consistent internal layout
        self.columnconfigure(
            0,
            weight=1,
        )