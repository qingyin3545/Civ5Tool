import tkinter as tk
from tkinter import filedialog
from i18n_manager import I18N
# 文件查找
import os
import shutil
import re
# 模组生成
from utils.modinfo import generate_modinfo

class TranslationPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # ===== 路径选择区域 =====
        self._mod_path = tk.StringVar()

        path_frame = tk.Frame(self)
        path_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.path_label = tk.Label(
            path_frame,
        )
        self.path_label.pack(side="left")

        self.path_entry = tk.Entry(
            path_frame,
            textvariable=self._mod_path
        )
        self.path_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.browse_button = tk.Button(
            path_frame,
            command=self._browse_mod_path
        )
        self.browse_button.pack(side="left")

        # ===== 生成按钮 =====
        action_frame = tk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)

        self.generate_button = tk.Button(
            action_frame,
            command=self._on_generate
        )
        self.generate_button.pack()

        # ===== log输出 =====
        log_frame = tk.Frame(self)
        log_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        self.log_text = tk.Text(
            log_frame,
            height=10,
            state="disabled"
        )
        self.log_text.pack(fill="both", expand=True)

    # ===== 浏览路径 =====
    def _browse_mod_path(self):
        path = filedialog.askdirectory()
        if path:
            self._mod_path.set(path)
            self.log(f"Selected mod path: {path}")

    # ===== 生成翻译 =====
    def _on_generate(self):
        mod_path = self._mod_path.get().strip()

        if not mod_path or not os.path.isdir(mod_path):
            self.log("Invalid mod folder.")
            return

        output_dir = self._get_output_dir(mod_path)
        os.makedirs(output_dir, exist_ok=True)

        self.log(f"Scanning mod folder: {mod_path}")

        # TODO: 剔除无关的内容, 部分文件即包含翻译也包含DB
        # TODO: 对于有翻译文件的模组，需要增加依赖
        files = self._collect_translation_files(mod_path, output_dir)

        if not files:
            self.log("No translation files found.")
            return

        modinfo_path = generate_modinfo(output_dir, files)

        self.log(f"Collected {len(files)} file(s).")
        self.log(f"Generated modinfo: {modinfo_path}")
        self.log(f"Output directory: {output_dir}")
    
    def _get_output_dir(self, mod_path: str) -> str:
        parent = os.path.dirname(mod_path)
        name = os.path.basename(mod_path.rstrip(os.sep))
        return os.path.join(parent, f"{name}-Translation")

    def _collect_translation_files(self, mod_path: str, output_dir: str) -> list[str]:
        collected_files = []

        for root, _, files in os.walk(mod_path):
            for file in files:
                if not file.lower().endswith((".xml", ".sql")):
                    continue

                src_path = os.path.join(root, file)

                if not self._contains_language_en_us(src_path):
                    continue

                rel_path = os.path.relpath(src_path, mod_path)
                dst_path = os.path.join(output_dir, rel_path)

                os.makedirs(os.path.dirname(dst_path), exist_ok=True)
                shutil.copy2(src_path, dst_path)

                self.log(f"Collected: {rel_path}")
                collected_files.append(rel_path)

        return collected_files

    def _contains_language_en_us(self, path: str) -> bool:
        ext = os.path.splitext(path)[1].lower()

        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            content = f.read()

        if ext == ".xml":
            return "<language_en_us>" in content.lower()

        if ext == ".sql":
            text = content.lower()

            return (
                re.search(r"\bupdate\s+language_en_us\b", text) is not None
                or re.search(r"\binsert\b.*?\binto\s+language_en_us\b", text) is not None
            )

        return False

    # ===== 日志接口 =====
    def log(self, message: str):
        self.log_text.config(state="normal")
        self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    # ===== 语言刷新 =====
    def refresh_text(self):
        self.path_label.config(text=I18N.t("path.mod_path"))
        self.browse_button.config(text=I18N.t("path.browse"))
        self.generate_button.config(text=I18N.t("translate.generate"))