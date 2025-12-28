from tkinter import ttk
from i18n_manager import I18N


class TranslatePage(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        self.label = ttk.Label(self, font=("Segoe UI", 12))
        self.label.pack(pady=40)

        self.refresh_text()

    def refresh_text(self):
        self.label.config(text=I18N.t("translate.placeholder"))