import tkinter as tk
from tkinter import filedialog
from i18n.i18n_manager import I18N
# 文件查找
import os
import shutil
import xml.etree.ElementTree as ET
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
        # buider输出灰色
        self.log_text.tag_config("civ5projexcept", foreground="gray")

        self.refresh_text()

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
            # 查找该目录下的 .civ5proj 文件
            proj_files = [f for f in files if f.lower().endswith(".civ5proj")]
            allowed_files = set()
            for proj_file in proj_files:
                proj_path = os.path.join(root, proj_file)
                try:
                    tree = ET.parse(proj_path)
                    root_elem = tree.getroot()
                    # 注意 xmlns 可能影响查找，需要加上命名空间
                    ns = {'msb': 'http://schemas.microsoft.com/developer/msbuild/2003'}
                    for file_elem in root_elem.findall(".//msb:FileName", ns):
                        file_rel = file_elem.text.replace("\\", os.sep)
                        allowed_files.add(os.path.join(root, file_rel))
                except Exception as e:
                    self.log(f"Failed to parse {proj_path}: {e}")

            for file in files:
                if not file.lower().endswith((".xml", ".sql")):
                    continue

                src_path = os.path.join(root, file)

                # 先检查是否有 Language_en_US
                if not self._contains_language_en_us(src_path):
                    continue

                # 如果存在 .civ5proj，则只收集在 allowed_files 中的文件
                if proj_files and src_path not in allowed_files:
                    rel_path = os.path.relpath(src_path, mod_path)
                    self.log(f"Skipped by .civ5proj: {rel_path}", tag="civ5projexcept")
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
    def log(self, message: str, tag: str | None = None):
        self.log_text.config(state="normal")
        if tag:
            self.log_text.insert("end", message + "\n", tag)
        else:
            self.log_text.insert("end", message + "\n")
        self.log_text.see("end")
        self.log_text.config(state="disabled")

    # ===== 语言刷新 =====
    def refresh_text(self):
        self.path_label.config(text=I18N.t("path.mod_path"))
        self.browse_button.config(text=I18N.t("path.browse"))
        self.generate_button.config(text=I18N.t("translate.generate"))