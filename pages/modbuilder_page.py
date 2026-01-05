import tkinter as tk
from tkinter import filedialog
from i18n_manager import I18N
import os, sys
from civ5_mod_builder import Builder
from civ5_paths import CIV5_DIR
from utils.stdout_redirect import StdoutToLogger
import threading

class ModBuilderPage(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        # ===== 路径变量 =====
        self._input_path = tk.StringVar()
        self._output_path = tk.StringVar(value=os.path.join(CIV5_DIR, "MODS"))

        # ===== 输入文件路径 (.civ5proj) =====
        input_frame = tk.Frame(self)
        input_frame.pack(fill="x", padx=10, pady=(10, 5))

        self.input_label = tk.Label(input_frame)
        self.input_label.pack(side="left")

        self.input_entry = tk.Entry(
            input_frame,
            textvariable=self._input_path
        )
        self.input_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.input_browse_button = tk.Button(
            input_frame,
            command=self._browse_input_file
        )
        self.input_browse_button.pack(side="left")

        # ===== 输出目录路径 =====
        output_frame = tk.Frame(self)
        output_frame.pack(fill="x", padx=10, pady=(5, 5))

        self.output_label = tk.Label(output_frame)
        self.output_label.pack(side="left")

        self.output_entry = tk.Entry(
            output_frame,
            textvariable=self._output_path
        )
        self.output_entry.pack(side="left", fill="x", expand=True, padx=5)

        self.output_browse_button = tk.Button(
            output_frame,
            command=self._browse_output_dir
        )
        self.output_browse_button.pack(side="left")

        # ===== 生成按钮 =====
        action_frame = tk.Frame(self)
        action_frame.pack(fill="x", padx=10, pady=10)

        self.generate_button = tk.Button(
            action_frame,
            command=self._on_generate
        )
        self.generate_button.pack()

        # ===== log 输出 =====
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
        self.log_text.tag_config("builder", foreground="gray")

        # ===== 标签 =====
        thanks_label = tk.Label(
            self,
            text="Special thanks: catgrep",
            font=("Arial", 9),
            fg="gray"
        )
        thanks_label.pack(side="bottom", pady=(0, 5))

        self.refresh_text()

    # ===== 浏览输入文件（限定 .civ5proj） =====
    def _browse_input_file(self):
        path = filedialog.askopenfilename(
            title="Select Civ5 Project File",
            filetypes=[
                ("Civ5 Project (*.civ5proj)", "*.civ5proj"),
                ("All files", "*.*"),
            ]
        )
        if path:
            self._input_path.set(path)
            self.log(f"Selected project file: {path}")

    # ===== 浏览输出目录（只能是文件夹） =====
    def _browse_output_dir(self):
        path = filedialog.askdirectory(
            title="Select Output Directory"
        )
        if path:
            self._output_path.set(path)
            self.log(f"Selected output directory: {path}")

    # ===== 生成按钮逻辑 =====
    def _on_generate(self):
        input_path = self._input_path.get().strip()
        output_path = self._output_path.get().strip()

        # ---- 双重校验 ----
        if not input_path:
            self.log("Input project file is empty.")
            return

        if not input_path.lower().endswith(".civ5proj"):
            self.log("Input file must be a .civ5proj file.")
            return

        if not os.path.isfile(input_path):
            self.log("Input project file does not exist.")
            return

        if not output_path:
            self.log("Output directory is empty.")
            return

        if not os.path.isdir(output_path):
            self.log("Output path must be a directory.")
            return

        self.log("Generate action triggered.")
        self.log(f"Project: {input_path}")
        self.log(f"Output: {output_path}")

        # 禁用按钮防止重复点击
        self.generate_button.config(state="disabled")

        # 启动后台线程执行 Builder
        thread = threading.Thread(target=self._run_builder, args=(input_path, output_path,))
        thread.start()
    
    def _run_builder(self, input_path, output_path):
        # 临时重定向 stdout 到日志
        old_stdout = sys.stdout
        sys.stdout = StdoutToLogger(self._thread_safe_log, tag="builder")
        # 调用 civ5 mod builder 构建
        try:
            builder = Builder()
            result = builder.build(
                input_proj_file_path=input_path,
                output_mods_dir_path=output_path
            )

        except Exception as e:
            self.log(f"Build failed: {e}")
            return
        finally:
            # 恢复输出重定向
            sys.stdout = old_stdout

        # 任务结束，更新 UI
        self.after(0, lambda: self._on_builder_done(result.mod_dir))
    def _thread_safe_log(self, message, tag=None):
        # 调用主线程更新 log
        self.after(0, lambda: self.log(message, tag))
    def _on_builder_done(self, mod_dir):
        self.log(I18N.t("log.output_mod", mod_dir=mod_dir))
        self.generate_button.config(state="normal")

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
        self.input_label.config(text=I18N.t("path.project_file"))
        self.input_browse_button.config(text=I18N.t("path.browse"))

        self.output_label.config(text=I18N.t("path.output_dir"))
        self.output_browse_button.config(text=I18N.t("path.browse"))

        self.generate_button.config(text=I18N.t("build.generate"))