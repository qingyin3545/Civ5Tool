import os
import shutil
import tkinter as tk
from tkinter import ttk, filedialog

from civ5_paths import CIV5_DIR
from i18n_manager import I18N


class BasicPage(ttk.Frame):
    
    def __init__(self, parent, on_ui_lang_change):
        super().__init__(parent)
        self.civ5_path = tk.StringVar(value=CIV5_DIR)
        self._on_ui_lang_change = on_ui_lang_change
        self._build_ui()

    def _build_ui(self):
        btn_frame = ttk.Frame(self)
        btn_frame.pack(pady=10)

        # ===== 路径选择区域 =====
        path_frame = tk.Frame(self)
        path_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.path_label = tk.Label(
            path_frame,
        )
        self.path_label.pack(side="left")

        self.path_entry = tk.Entry(
            path_frame,
            textvariable=self.civ5_path
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.browse_button = tk.Button(
            path_frame,
            command=self.browse_path
        )
        self.browse_button.pack(side="left")

        # ===== 游戏语言 =====
        self.btn_game_lang = ttk.Button(
            btn_frame,
            command=self.toggle_game_language
        )
        self.btn_game_lang.pack(side="left", padx=5)

        # ===== 清理缓存 =====
        self.btn_clear_cache = ttk.Button(
            btn_frame,
            command=self.clear_cache
        )
        self.btn_clear_cache.pack(side="left", padx=5)

        # ===== 程序语言 =====
        self.btn_ui_lang = ttk.Button(
            btn_frame,
            command=self.toggle_ui_language
        )
        self.btn_ui_lang.pack(side="left", padx=5)

        # ===== log输出 =====
        log_frame = tk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        scrollbar = tk.Scrollbar(log_frame)
        scrollbar.pack(side="right", fill="y")

        self.log_text = tk.Text(
            log_frame,
            height=10,
            state="disabled",
            yscrollcommand=scrollbar.set
        )
        self.log_text.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=self.log_text.yview)

        self.refresh_text()

    # ---------- UI ----------
    def browse_path(self):
        path = filedialog.askdirectory(
            initialdir=self.civ5_path.get()
        )
        if path:
            self.civ5_path.set(path)

    def refresh_text(self):
        self.path_label.config(text=I18N.t("path.civ5_path"))
        self.browse_button.config(text=I18N.t("path.browse"))
        self.btn_game_lang.config(text=I18N.t("btn.toggle_game_lang"))
        self.btn_clear_cache.config(text=I18N.t("btn.clear_cache"))
        self.btn_ui_lang.config(text=I18N.t("btn.toggle_ui_lang"))

    def log(self, msg):
        self.log_text.configure(state="normal")
        self.log_text.insert("end", msg + "\n")
        self.log_text.see("end")
        self.log_text.configure(state="disabled")

    # ---------- logic ----------
    def toggle_game_language(self):
        INI_PATH = os.path.join(self.civ5_path.get(), "config.ini")
        if not os.path.exists(INI_PATH):
            self.log(I18N.t("log.not_found"))
            return

        tmp_path = INI_PATH + ".tmp"

        with open(INI_PATH, "r", encoding="utf-8", errors="ignore") as fin, \
             open(tmp_path, "w", encoding="utf-8", errors="ignore") as fout:
            for line in fin:
                s = line.strip()
                if s == "Language = zh_CN":
                    fout.write("Language = en_US\n")
                    self.log("Language = en_US")
                elif s == "Language = en_US":
                    fout.write("Language = zh_CN\n")
                    self.log("Language = zh_CN")
                else:
                    fout.write(line)

        os.replace(tmp_path, INI_PATH)

    def clear_cache(self):
        CACHE_PATH = os.path.join(self.civ5_path.get(), "cache")
        MOD_FILE = os.path.join(
            self.civ5_path.get(),
            "ModUserData",
            "df3333a4-44be-4fc3-9143-21706ff451d5-1.db"
        )
        try:
            if os.path.exists(CACHE_PATH):
                shutil.rmtree(CACHE_PATH)

            if os.path.exists(MOD_FILE):
                os.remove(MOD_FILE)

            self.log(I18N.t("log.cache_ok"))
        except Exception:
            self.log(I18N.t("log.cache_fail"))

    def toggle_ui_language(self):
        I18N.toggle()
        self._on_ui_lang_change()