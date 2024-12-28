import tkinter as tk
from tkinter import simpledialog, messagebox
from sitecopy import ExtractUrls, SaveSinglePage

def download():
    url = simpledialog.askstring("输入URL", "请输入要下载的URL:")
    if not url:
        messagebox.showwarning("警告", "URL不能为空")
        return

    depth = simpledialog.askinteger("输入深度", "请输入下载深度:", initialvalue=200)
    if depth is None:
        messagebox.showwarning("警告", "深度不能为空")
        return

    threads = simpledialog.askinteger("输入线程数", "请输入线程数:", initialvalue=30)
    if threads is None:
        messagebox.showwarning("警告", "线程数不能为空")
        return

    entire = messagebox.askyesno("下载整个网站", "是否下载整个网站?")

    if entire:
        ExtractUrls(url, depth, threads)
    else:
        SaveSinglePage(url)
    messagebox.showinfo("完成", "所有资源已下载")

root = tk.Tk()
root.title("SiteCopy GUI")

download_button = tk.Button(root, text="开始下载", command=download)
download_button.pack(padx=20, pady=20)

root.mainloop()
