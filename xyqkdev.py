from pathlib import Path
from itertools import cycle
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageSequence
from rich import traceback
import os
import tkinter as tk
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import ttk
import configparser  # 确保导入 configparser
from ttkbootstrap.dialogs import Messagebox
from dependency_manager import check_dependency_installed, install_dependencies, update_config
import subprocess
traceback.install(show_locals=True)

class AnimatedGif(tb.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=300)

        file_path = Path(__file__).parent / "loading.gif"
        with Image.open(file_path) as im:
            images = [ImageTk.PhotoImage(s) for s in ImageSequence.Iterator(im)]
            self.image_cycle = cycle(images)
            self.framerate = im.info["duration"]

        self.img_container = tb.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)

def install_dependencies_with_animation(use_multithreading, config_path):
    install_window = tb.Toplevel()
    install_window.title("安装中")
    install_window.geometry("400x400")
    install_window.iconbitmap('favicon.ico')
    install_window.resizable(False, False)

    content_frame = tb.Frame(install_window)
    content_frame.pack(expand=True, fill=BOTH)

    gif = AnimatedGif(content_frame)
    gif.pack(pady=(20, 10))

    progress_label = tb.Label(content_frame, text="开始安装...", font=("Helvetica", 12))
    progress_label.pack(pady=(10, 10))

    progress_bar = ttk.Progressbar(content_frame, orient=HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=(10, 20))

    threading.Thread(target=install_dependencies, args=(progress_bar, progress_label, install_window, use_multithreading, config_path)).start()

    install_window.mainloop()

def run_program(command):
    subprocess.Popen(command, shell=True)

def run_program1():
    print("运行ROOT")
    os.system("cmd /c start boot一键ROOT.bat")

def run_program3():
    print("运行cmd")
    os.system("cmd /c start cd xyqk")

def run_program4():
    print("运行DM")
    print("retrycancel: ",Messagebox.show_warning(message="慎重操作"))
    os.system("cmd /c start dm.bat")

def run_program5():
    print("运行驱动程序")
    os.system("cmd /c start install-driver.bat")

def run_program6():
    print("运行安装7-zip")
    run_program("7-zip.exe")

def run_program7():
    print("运行收款")
    run_program("python pay.py")

def create_frame1():

    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = tb.Frame(app, height=600, width=1080, bootstyle="info")
    current_frame.pack(fill="both", expand=1)
    current_frame.pack_propagate(0)

    background_image = Image.open("background.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tb.Label(current_frame, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    center_label = tb.Label(current_frame, text="星雨晴空工具箱", font=("Helvetica", 24), borderwidth=2, relief="solid", foreground="white", bootstyle="INFO")
    center_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

    button_frame = tb.Frame(current_frame)
    button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    buttons = [
        ("root", run_program1),
        ("cmd", run_program3),
        ("去dm校检", run_program4),
        ("驱动", run_program5),
        ("7-zip", run_program6),
        ("收款", run_program7)
    ]

    for i, (text, command) in enumerate(buttons):
        button = tb.Button(button_frame, text=text, command=command, bootstyle="success.Outline.TButton")
        button.grid(row=0, column=i, padx=5, pady=10)

def create_frame2():
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = tb.Frame(app, height=600, width=1080, bootstyle="primary")
    current_frame.pack(fill="both", expand=1)
    current_frame.pack_propagate(0)

    background_image = Image.open("background2.jpg")
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tb.Label(current_frame, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    center_label = tb.Label(current_frame, text="GSI刷写", font=("Helvetica", 24), borderwidth=2, relief="solid", foreground="white", bootstyle="INFO")
    center_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

def create_frame3():
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = tk.Frame(app, height=600, width=1080, bg="green")
    current_frame.pack(fill="both", expand=1)
    current_frame.pack_propagate(0)

    label = tk.Label(current_frame, text='设置', font=('Helvetica', 18))
    label.pack(pady=10)

    # 左侧按钮框架
    left_frame = tk.Frame(current_frame)
    left_frame.pack(side="left", padx=20, pady=20, fill="y")

    # 中间按钮框架
    center_frame = tk.Frame(current_frame)
    center_frame.pack(pady=20)

    switches = [
        ("功能1", "feature1"),
        ("功能2", "feature2"),
        ("功能3", "feature3"),
        ("功能4", "feature4"),
    ]

    config_path = Path(__file__).parent / 'config.ini'
    config = configparser.ConfigParser()
    if not config.has_section('features'):
        config.add_section('features')
    config.read(config_path)

    for i, (text, feature) in enumerate(switches):
        is_enabled = config.getboolean('features', feature, fallback=False)
        var = tk.BooleanVar(value=is_enabled)
        switch = ttk.Checkbutton(left_frame, text=text, variable=var, style="success-round-toggle")
        switch.grid(row=i, column=0, pady=10)

        def toggle_feature(feature=feature, var=var):
            config.set('features', feature, str(var.get()))
            with open(config_path, 'w') as configfile:
                config.write(configfile)

        switch.config(command=toggle_feature)

    # 添加控制 update_after_install 状态的按钮
    update_after_install = config.getboolean('dependencies', 'update_after_install', fallback=False)
    update_var = tk.BooleanVar(value=update_after_install)
    update_switch = ttk.Checkbutton(center_frame, text="更新配置", variable=update_var, style="success-round-toggle")
    update_switch.grid(row=0, column=0, pady=10)

    def toggle_update():
        config.set('dependencies', 'update_after_install', str(update_var.get()))
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    update_switch.config(command=toggle_update)

    # 添加控制 use_multithreading 状态的按钮
    use_multithreading = config.getboolean('dependencies', 'use_multithreading', fallback=False)
    threading_var = tk.BooleanVar(value=use_multithreading)
    threading_switch = ttk.Checkbutton(center_frame, text="多线程", variable=threading_var, style="success-round-toggle")
    threading_switch.grid(row=1, column=0, pady=10)

    def toggle_threading():
        config.set('dependencies', 'use_multithreading', str(threading_var.get()))
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    threading_switch.config(command=toggle_threading)

    # 添加控制 installed 状态的按钮
    installed = config.getboolean('dependencies', 'installed', fallback=False)
    installed_var = tk.BooleanVar(value=installed)
    installed_switch = ttk.Checkbutton(center_frame, text="已安装", variable=installed_var, style="success-round-toggle")
    installed_switch.grid(row=2, column=0, pady=10)

    def toggle_installed():
        config.set('dependencies', 'installed', str(installed_var.get()))
        with open(config_path, 'w') as configfile:
            config.write(configfile)

    installed_switch.config(command=toggle_installed)
    

    # 右侧按钮框架
    right_frame = tk.Frame(current_frame)
    right_frame.pack(side="right", padx=20, pady=20, fill="y")

    # 添加超链接按钮
    def open_link(url):
        os.system(f"start {url}")

    link_button1 = ttk.Button(right_frame, style="success-link" , text="我的QQ", command=lambda: open_link("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click"))
    link_button1.pack(pady=10)

    link_button2 = ttk.Button(right_frame, style="success-link" , text="github开源地址", command=lambda: open_link("https://example.com"))
    link_button2.pack(pady=10)

app = tb.Window(themename='darkly')
app.title('XYQK TOOL 1.3data')
app.geometry("600x400")
app.resizable(False, False)
app.iconbitmap('favicon.ico')

button_frame = tb.Frame(app, height=50, width=512, bootstyle="dark")
button_frame.pack(side='top', fill='both', expand=1)

btn1 = tb.Button(button_frame, text='主页', command=create_frame1, bootstyle="info.Outline.TButton")
btn1.place(relx=0, rely=0, relwidth=0.3, relheight=1)

btn2 = tb.Button(button_frame, text='菜单', command=create_frame2, bootstyle="danger.Outline.TButton" , state="disabled")
btn2.place(relx=0.3, rely=0, relwidth=0.3, relheight=1)

btn3 = tb.Button(button_frame, text='设置', command=create_frame3, bootstyle="success.Outline.TButton")
btn3.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

current_frame = None
create_frame1()

if __name__ == "__main__":
    config_path = Path(__file__).parent / 'config.ini'
    config = configparser.ConfigParser()
    config.read(config_path)

    use_multithreading = config.getboolean('dependencies', 'use_multithreading', fallback=False)

    if not check_dependency_installed(config_path):
        print("依赖未安装。正在安装...")
        install_dependencies_with_animation(use_multithreading, config_path)
        update_after_install = config.getboolean('dependencies', 'update_after_install', fallback=True)
        if update_after_install:
            print("更新配置...")
            update_config(config_path)
    else:
        print("已经初始化过了，即将启动程序")
    app.mainloop()
    
