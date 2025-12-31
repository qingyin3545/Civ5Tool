import tkinter as tk
from tkinter import ttk

from pages.basic_page import BasicPage
from pages.translate_page import TranslationPage
from pages.modbuilder_page import ModBuilderPage
from i18n_manager import I18N


class CivToolApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.notebook = ttk.Notebook(self)
        self.notebook.pack(fill="both", expand=True)

        self.basic_page = BasicPage(self.notebook, self.refresh_ui_language)
        self.translate_page = TranslationPage(self.notebook)
        self.modbuilder_page = ModBuilderPage(self.notebook)

        self.notebook.add(self.basic_page, text=I18N.t("tab.basic"))
        self.notebook.add(self.translate_page, text=I18N.t("tab.translate"))
        self.notebook.add(self.modbuilder_page, text=I18N.t("tab.modbuilder_page"))

        self.refresh_ui_language()

    def refresh_ui_language(self):
        self.title(I18N.t("app.title"))

        self.notebook.tab(0, text=I18N.t("tab.basic"))
        self.notebook.tab(1, text=I18N.t("tab.translate"))

        self.basic_page.refresh_text()
        self.translate_page.refresh_text()
        self.modbuilder_page.refresh_text()


if __name__ == "__main__":
    app = CivToolApp()
    app.geometry("600x400")
    app.mainloop()