import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import os
import threading
import sys
import shutil
import requests
import subprocess

class RedirectText(object):
    def __init__(self, widget):
        self.widget = widget

    def write(self, string):
        self.widget.config(state=tk.NORMAL)
        self.widget.insert(tk.END, string)
        self.widget.config(state=tk.DISABLED)
        self.widget.see(tk.END)

def check_sitecopy():
    if not os.path.exists("sitecopy.py") and not os.path.exists("sitecopy.exe"):
        if messagebox.askyesno("缺少文件", "当前文件夹没有 sitecopy.py 或 sitecopy.exe，是否下载？"):
            url = "https://github.com/0ee37004-7935-442b-8c90-b4a567092802"
            response = requests.get(url)
            with open("sitecopy.py", "wb") as f:
                f.write(response.content)
            messagebox.showinfo("下载完成", "sitecopy.py 已下载完成")

def download():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("警告", "URL不能为空")
        return

    try:
        depth = int(depth_entry.get())
    except ValueError:
        messagebox.showwarning("警告", "深度必须是整数")
        return

    try:
        threads = int(threads_entry.get())
    except ValueError:
        messagebox.showwarning("警告", "线程数必须是整数")
        return

    entire = entire_var.get()
    save_path = save_path_entry.get()
    if not save_path:
        messagebox.showwarning("警告", "保存路径不能为空")
        return

    def run_download():
        if os.path.exists("sitecopy.exe"):
            process = subprocess.Popen(
                ["sitecopy.exe", "-u", url, "-d", str(depth), "-t", str(threads), "-e" if entire else ""],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            for line in process.stdout:
                sys.stdout.write(line.decode())
            for line in process.stderr:
                sys.stderr.write(line.decode())
        else:
            from sitecopy import ExtractUrls, SaveSinglePage
            if entire:
                ExtractUrls(url, depth, threads)
            else:
                SaveSinglePage(url)
        shutil.move("website", save_path)
        messagebox.showinfo("完成", "所有资源已下载并保存到指定路径")

    threading.Thread(target=run_download).start()

def browse_save_path():
    save_path = filedialog.askdirectory(title="选择保存路径")
    if save_path:
        save_path_entry.delete(0, tk.END)
        save_path_entry.insert(0, save_path)

def download_from_file():
    file_path = filedialog.askopenfilename(title="选择site.txt文件", filetypes=[("Text files", "*.txt")])
    if not file_path:
        messagebox.showwarning("警告", "文件路径不能为空")
        return

    save_path = save_path_entry.get()
    if not save_path:
        messagebox.showwarning("警告", "保存路径不能为空")
        return

    def run_download():
        with open(file_path, "r", encoding="utf-8") as fobject:
            urls = fobject.read().split("\n")
        if os.path.exists("sitecopy.exe"):
            for url in urls:
                process = subprocess.Popen(
                    ["sitecopy.exe", "-u", url, "-d", depth_entry.get(), "-t", threads_entry.get(), "-e" if entire_var.get() else ""],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
                for line in process.stdout:
                    sys.stdout.write(line.decode())
                for line in process.stderr:
                    sys.stderr.write(line.decode())
        else:
            from sitecopy import ExtractUrls, SaveSinglePage
            for url in urls:
                if entire_var.get():
                    ExtractUrls(url, int(depth_entry.get()), int(threads_entry.get()))
                else:
                    SaveSinglePage(url)
        shutil.move("website", save_path)
        messagebox.showinfo("完成", "所有资源已下载并保存到指定路径")

    threading.Thread(target=run_download).start()

def create_context_menu(widget):
    menu = tk.Menu(widget, tearoff=0)
    menu.add_command(label="复制", command=lambda: widget.event_generate("<<Copy>>"))
    menu.add_command(label="粘贴", command=lambda: widget.event_generate("<<Paste>>"))
    menu.add_command(label="剪切", command=lambda: widget.event_generate("<<Cut>>"))

    def show_menu(event):
        menu.tk_popup(event.x_root, event.y_root)

    widget.bind("<Button-3>", show_menu)

root = tk.Tk()
root.title("SiteCopy GUI")

check_sitecopy()

frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

ttk.Label(frame, text="URL:").grid(column=0, row=0, padx=10, pady=10, sticky=tk.W)
url_entry = ttk.Entry(frame, width=50)
url_entry.grid(column=1, row=0, padx=10, pady=10, sticky=tk.E)
create_context_menu(url_entry)

ttk.Label(frame, text="深度:").grid(column=0, row=1, padx=10, pady=10, sticky=tk.W)
depth_entry = ttk.Entry(frame, width=10)
depth_entry.grid(column=1, row=1, padx=10, pady=10, sticky=tk.E)
depth_entry.insert(0, "200")
create_context_menu(depth_entry)

ttk.Label(frame, text="线程数:").grid(column=0, row=2, padx=10, pady=10, sticky=tk.W)
threads_entry = ttk.Entry(frame, width=10)
threads_entry.grid(column=1, row=2, padx=10, pady=10, sticky=tk.E)
threads_entry.insert(0, "30")
create_context_menu(threads_entry)

ttk.Label(frame, text="保存路径:").grid(column=0, row=3, padx=10, pady=10, sticky=tk.W)
save_path_entry = ttk.Entry(frame, width=50)
save_path_entry.grid(column=1, row=3, padx=10, pady=10, sticky=tk.E)
create_context_menu(save_path_entry)
browse_button = ttk.Button(frame, text="浏览", command=browse_save_path)
browse_button.grid(column=2, row=3, padx=10, pady=10, sticky=tk.E)

entire_var = tk.BooleanVar()
entire_check = ttk.Checkbutton(frame, text="下载整个网站", variable=entire_var)
entire_check.grid(column=1, row=4, padx=10, pady=10, sticky=tk.W)

download_button = ttk.Button(frame, text="开始下载", command=download)
download_button.grid(column=1, row=5, padx=10, pady=10, sticky=tk.E)

download_file_button = ttk.Button(frame, text="从文件下载", command=download_from_file)
download_file_button.grid(column=1, row=6, padx=10, pady=10, sticky=tk.E)

log_text = scrolledtext.ScrolledText(root, state=tk.DISABLED, width=80, height=20)
log_text.grid(row=1, column=0, padx=20, pady=20)
create_context_menu(log_text)

sys.stdout = RedirectText(log_text)
sys.stderr = RedirectText(log_text)

root.mainloop()
