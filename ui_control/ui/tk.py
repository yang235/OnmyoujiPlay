import ctypes
import logging
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from anasis.utils.excel_analysis import count_info, restart_mark, excel_analysis


class TkinterLogHandler(logging.Handler):
    """将 logging 日志输出到 tkinter Text 控件"""

    def __init__(self, text_widget):
        super().__init__()
        self.text_widget = text_widget

    def emit(self, record):
        try:
            msg = record.getMessage()
        except (TypeError, IndexError):
            msg = str(record.msg)
        def _write():
            self.text_widget.configure(state=tk.NORMAL)
            self.text_widget.insert(tk.END, msg + "\n")
            self.text_widget.see(tk.END)
            self.text_widget.configure(state=tk.DISABLED)
        self.text_widget.after(0, _write)


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("阴阳师 自动化")
        self.root.geometry("500x640")

        # 账号列表
        ttk.Label(root, text="账号列表").pack(pady=(10, 0))
        self.count_listbox = tk.Listbox(root, height=6, width=35)
        self.count_listbox.pack(pady=5)
        self.count_listbox.bind("<<ListboxSelect>>", self.on_count_select)

        ttk.Button(root, text="刷新账号列表", command=self.refresh_counts).pack()

        # 分区列表 (单击切换选中/取消)
        ttk.Label(root, text="分区").pack(pady=(15, 0))
        self.part_listbox = tk.Listbox(root, height=10, width=35, selectmode=tk.MULTIPLE)
        self.part_listbox.pack(pady=5)
        self.part_listbox.bind("<Button-1>", self._on_part_click)

        # 操作按钮
        btn_frame = ttk.Frame(root)
        btn_frame.pack(pady=15)
        ttk.Button(btn_frame, text="标记已完成", command=self.mark_done).pack(side=tk.LEFT, padx=5)
        ttk.Button(btn_frame, text="重置所有标记", command=self.reset_marks).pack(side=tk.LEFT, padx=5)
        self.login_btn = ttk.Button(btn_frame, text="启动登录", command=self.start_login)
        self.login_btn.pack(side=tk.LEFT, padx=5)
        self.stop_btn = ttk.Button(btn_frame, text="停止", command=self.stop_login, state=tk.DISABLED)
        self.stop_btn.pack(side=tk.LEFT, padx=5)

        # 信息框
        info_frame = ttk.LabelFrame(root, text="操作日志", padding=5)
        info_frame.pack(pady=(10, 0), fill=tk.BOTH, expand=True)
        self.info_text = tk.Text(info_frame, height=6, width=35, state=tk.DISABLED)
        scrollbar = ttk.Scrollbar(info_frame, command=self.info_text.yview)
        self.info_text.configure(yscrollcommand=scrollbar.set)
        self.info_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # 状态栏
        self.status = ttk.Label(root, text="就绪", relief=tk.SUNKEN, anchor=tk.W)
        self.status.pack(side=tk.BOTTOM, fill=tk.X)

        self._part_data = {}
        self._current_count = None

        # 配置 logging 输出到信息框
        handler = TkinterLogHandler(self.info_text)
        logging.root.addHandler(handler)
        logging.root.setLevel(logging.INFO)

        self.refresh_counts()
        self._preload_ocr()

    def _preload_ocr(self):
        logging.info("OCR插件加载中...")
        self.status.config(text="OCR插件加载中...")

        def _load():
            from anasis.utils.pp_ocr import init_ocr
            try:
                init_ocr()
                self.root.after(0, lambda: self.status.config(text="就绪"))
            except Exception as e:
                self.root.after(0, lambda err=e: logging.error(f"OCR插件加载失败: {err}"))

        threading.Thread(target=_load, daemon=True).start()

    def refresh_counts(self):
        self.count_listbox.delete(0, tk.END)
        self.part_listbox.delete(0, tk.END)
        for name in sorted(count_info()):
            self.count_listbox.insert(tk.END, name)

    def on_count_select(self, _event):
        count_name = self._get_selected_count()
        if count_name:
            self._current_count = count_name
            self._refresh_parts(count_name)

    def _on_part_click(self, event):
        idx = self.part_listbox.nearest(event.y)
        if idx < 0:
            return
        if idx in self.part_listbox.curselection():
            self.part_listbox.selection_clear(idx)
        else:
            self.part_listbox.selection_set(idx)
        return "break"

    def _refresh_parts(self, count_name):
        """保持账号选中状态，刷新分区列表"""
        _, df = excel_analysis()
        rows = df[df['count'] == count_name]
        self.part_listbox.delete(0, tk.END)
        self._part_data.clear()
        for _, row in rows.iterrows():
            part = str(row['part'])
            mark = int(row['mark']) if 'mark' in row and row['mark'] is not None else 0
            self._part_data[part] = mark
            prefix = "[已登录] " if mark == 1 else "[未登录] "
            self.part_listbox.insert(tk.END, prefix + part)

    def _get_selected_count(self):
        selection = self.count_listbox.curselection()
        if selection:
            return self.count_listbox.get(selection[0])
        if self._current_count:
            return self._current_count
        messagebox.showwarning("提示", "请先选择账号")
        return None

    def mark_done(self):
        count_name = self._get_selected_count()
        if not count_name:
            return
        selected_indices = self.part_listbox.curselection()
        if not selected_indices:
            messagebox.showwarning("提示", "请先选择分区")
            return
        done_parts = []
        for i in selected_indices:
            raw = self.part_listbox.get(i)
            part = raw.replace("[已登录] ", "").replace("[未登录] ", "")
            done_parts.append(part)
        file_path, df = excel_analysis()
        mask = (df['count'] == count_name) & (df['part'].isin(done_parts))
        df.loc[mask, 'mark'] = 1
        df.to_excel(file_path, sheet_name='Sheet1', index=False)
        self._refresh_parts(count_name)
        self.status.config(text=f"已标记 {count_name} 的 {len(done_parts)} 个分区")
        logging.info(f"标记完成 {count_name} 分区: {', '.join(done_parts)}")

    def reset_marks(self):
        if not messagebox.askyesno("确认", "确定要将所有 mark 重置为 0?"):
            return
        restart_mark()
        count_name = self._get_selected_count()
        if count_name:
            self._refresh_parts(count_name)
        self.status.config(text="已重置所有标记")
        logging.info("所有标记已重置为0")

    def start_login(self):
        self.login_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.status.config(text="开始执行登录流程...")
        logging.info("开始执行登录流程")

        def _run():
            from ui_control.creat_game import login
            try:
                login()
                self.root.after(0, self._on_login_done)
            except SystemExit:
                self.root.after(0, self._on_login_done)
            except Exception as e:
                self.root.after(0, lambda err=e: self._on_login_error(err))

        self._login_thread = threading.Thread(target=_run, daemon=True)
        self._login_thread.start()

    def stop_login(self):
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="正在停止...")
        logging.info("正在停止登录线程...")
        tid = self._login_thread.ident
        if tid:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(
                ctypes.c_ulong(tid), ctypes.py_object(SystemExit)
            )

    def _on_login_done(self):
        self.login_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text="登录流程执行完成")
        logging.info("登录流程已结束")

    def _on_login_error(self, e):
        self.login_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.status.config(text=f"错误: {e}")
        logging.error(f"登录流程出错: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    App(root)
    root.mainloop()