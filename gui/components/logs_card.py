import tkinter as tk
from tkinter import ttk

from gui.components.card import Card
from utils.constants import (
    LOG_INFO,
    LOG_ACTIVITY,
    LOG_SUCCESS,
    LOG_WARNING,
    LOG_ERROR,
)


class LogsCard(Card):

    def __init__(
        self,
        parent,
        main_window,
    ):

        super().__init__(
            parent,
            title="Logs",
        )

        self.main_window = main_window

        self.build_ui()

    def build_ui(self):

        self.main_window.log_text = tk.Text(
            self,
            height=10,
            state="disabled",
            wrap="word",
        )

        self.main_window.log_text.tag_configure(
            LOG_INFO,
            foreground="#404040",
        )

        self.main_window.log_text.tag_configure(
            LOG_ACTIVITY,
            foreground="#2563EB",
        )

        self.main_window.log_text.tag_configure(
            LOG_SUCCESS,
            foreground="#16A34A",
        )

        self.main_window.log_text.tag_configure(
            LOG_WARNING,
            foreground="#D97706",
        )

        self.main_window.log_text.tag_configure(
            LOG_ERROR,
            foreground="#DC2626",
        )

        scrollbar = ttk.Scrollbar(
            self,
            orient="vertical",
            command=self.main_window.log_text.yview,
        )

        self.main_window.log_text.configure(
            yscrollcommand=scrollbar.set,
        )

        self.main_window.log_text.pack(
            side="left",
            fill="both",
            expand=True,
        )

        scrollbar.pack(
            side="right",
            fill="y",
        )