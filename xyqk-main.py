from pathlib import Path
from itertools import cycle
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from PIL import Image, ImageTk, ImageSequence
import configparser
import subprocess
from rich import traceback
import os
import tkinter as tk
import threading
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from tkinter import ttk

traceback.install(show_locals=True)

class AnimatedGif(tb.Frame):
    def __init__(self, master):
        super().__init__(master, width=400, height=300)

        # 打开GIF并创建循环迭代器
        file_path = Path(__file__).parent / "resource/loading.gif"
        with Image.open(file_path) as im:
            # 创建序列
            sequence = ImageSequence.Iterator(im)
            images = [ImageTk.PhotoImage(s) for s in sequence]
            self.image_cycle = cycle(images)

            # 每帧的长度
            self.framerate = im.info["duration"]

        self.img_container = tb.Label(self, image=next(self.image_cycle))
        self.img_container.pack(fill="both", expand="yes")
        self.after(self.framerate, self.next_frame)

    def next_frame(self):
        """更新每帧的图像"""
        self.img_container.configure(image=next(self.image_cycle))
        self.after(self.framerate, self.next_frame)

def check_dependency_installed():
    """
    检查配置文件中的依赖是否已安装

    返回:
        bool: 如果依赖已安装，则返回True；否则返回False。
    """
    config = configparser.ConfigParser()  # 创建配置文件解析器对象
    config.read('config.ini')  # 读取配置文件
    dependency_installed = config.getboolean('dependencies', 'installed', fallback=False)  # 获取配置文件中的依赖安装状态
    return dependency_installed

def install_dependency(dependency):
    """
    安装单个依赖
    """
    subprocess.run(['pip', 'install', dependency])  # 使用pip命令安装依赖
    return dependency

def install_dependencies(progress_bar, progress_label, install_window, use_multithreading):
    """
    使用pip安装依赖，并更新进度条
    """
    dependencies = ['scapy', 'ttkthemes', 'ttkbootstrap', 'rich']  # 在列表中指定要安装的多个依赖

    if use_multithreading:
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_dependency = {executor.submit(install_dependency, dep): dep for dep in dependencies}
            for i, future in enumerate(as_completed(future_to_dependency), 1):
                dep = future_to_dependency[future]
                try:
                    future.result()
                    print(f"{dep} 安装成功")
                except Exception as exc:
                    print(f"{dep} 安装失败: {exc}")
                progress_bar['value'] = i * (100 / len(dependencies))  # 更新进度条
                progress_label.config(text=f"正在安装 {dep} ({i}/{len(dependencies)})")
    else:
        for i, dependency in enumerate(dependencies, 1):
            install_dependency(dependency)
            progress_bar['value'] = i * (100 / len(dependencies))  # 更新进度条
            progress_label.config(text=f"正在安装 {dependency} ({i}/{len(dependencies)})")

    # 在主线程中关闭窗口
    install_window.after(0, install_window.destroy)

def update_config():
    """
    更新配置文件中的依赖安装状态为已安装
    """
    config = configparser.ConfigParser()  # 创建配置文件解析器对象
    config.read('config.ini')  # 读取配置文件
    config.set('dependencies', 'installed', 'True')  # 更新配置文件中的依赖安装状态
    with open('config.ini', 'w') as configfile:
        config.write(configfile)  # 将更新后的配置写回配置文件

def run_program(command):
    """在新的子进程中运行指定的命令"""
    subprocess.Popen(command, shell=True)

def run_program1():
    print("运行ROOT")
    os.system("cmd/c start boot一键ROOT.bat")
    os.chdir('.')

def run_program3():
    print("运行cmd")
    os.system("cmd/c start cd xyqk")

def run_program4():
    print("运行DM")
    current_directory = os.getcwd()  # 保存当前工作目录
    os.chdir('xyqk')
    os.system("cmd/c start dm.bat")
    os.chdir(current_directory)
    
def run_program5():
    print("运行驱动程序")
    current_directory = os.getcwd()  # 保存当前工作目录
    os.chdir('install-driver')
    run_program("cmd/c start install-driver.bat")
    os.chdir(current_directory) # 将当前工作目录更改回原来的目录

def run_program6():
    print("运行安装7-zip")
    run_program("7-zip.exe")

def run_program7():
    print("运行收款")
    run_program("python pay.py")

def run_ADBtool():
    print("运行ADB Tool")
    current_directory = os.getcwd()  
    os.chdir('xyqk')
    run_program("fastbootdemo.py")
    os.chdir(current_directory)

def run_FASTBOOTtool():
    print("运行FASTBOOT Tool")
    current_directory = os.getcwd()  
    os.chdir('xyqk')
    run_program("fastbootdemo.py")
    os.chdir(current_directory)
    
def run_web():
     print("运行网页导航")

def run_a57():
     print("A57 5G专属功能")

def run_gsi():
     print("GSI下载")

def run_ftd():
     print("运行fastbootd刷机工具")
     current_directory = os.getcwd()
     os.chdir('fastboot2')
     run_program("FastbootEnhance.exe")
     os.chdir(current_directory)

def install_dependencies_with_animation(use_multithreading):
    """
    显示安装动画并安装依赖
    """
    install_window = tb.Toplevel()
    install_window.title("安装中")
    install_window.geometry("400x400")
    install_window.iconbitmap('resource/favicon.ico')
    install_window.resizable(False, False)
    install_window.wm_attributes('-topmost', 1)

    # 使用 Frame 布局来使组件居中对齐
    content_frame = tb.Frame(install_window)
    content_frame.pack(expand=True, fill=BOTH)

    gif = AnimatedGif(content_frame)
    gif.pack(pady=(20, 10))  # 适当调整间距以使其居中

    progress_label = tb.Label(content_frame, text="开始安装...", font=("Helvetica", 12))
    progress_label.pack(pady=(10, 10))

    progress_bar = ttk.Progressbar(content_frame, orient=HORIZONTAL, length=200, mode='determinate')
    progress_bar.pack(pady=(10, 20))

    threading.Thread(target=install_dependencies, args=(progress_bar, progress_label, install_window, use_multithreading)).start()

    install_window.mainloop()

# 创建应用程序窗口
app = tb.Window(themename='darkly')
app.title('XYQK TOOL 1.3data')
app.geometry("900x500")
app.resizable(False, False)  # 禁止改变窗口大小
app.iconbitmap('resource/favicon.ico')

# 按钮框架
button_frame = tb.Frame(app, height=50, width=512, bootstyle="dark")
button_frame.pack(side='top', fill='both', expand=1)

# 淡入效果
def fade_in(widget, duration=200):
    steps = 30
    interval = duration // steps
    for i in range(steps + 2):
        alpha = 0.2 + (0.8 * i / steps)
        widget.attributes('-alpha', alpha)
        widget.update()
        time.sleep(interval / 1000)

# 淡出效果
def fade_out(widget, duration=400):
    steps = 30
    interval = duration // steps
    for i in range(steps + 2):
        alpha = 0.8 - (0.6 * i / steps)
        widget.attributes('-alpha', alpha)
        widget.update()
        time.sleep(interval / 1000)


def switch_frame(new_frame_func):
    fade_out(app)
    new_frame_func()
    fade_in(app)

style = tb.Style()
theme_names = style.theme_names()#以列表的形式返回多个主题名
theme_selection = tb.Frame(app, padding=(10, 10, 10, 0))
theme_selection.pack(fill=X, expand=YES)
lbl = tb.Label(theme_selection, text="选择主题:")
theme_cbo = tb.Combobox(
        master=theme_selection,
        text=style.theme.name,
        values=theme_names,
)
theme_cbo.pack(padx=10, side=RIGHT)
theme_cbo.current(theme_names.index(style.theme.name))
lbl.pack(side=RIGHT)
def change_theme(event):
    theme_cbo_value = theme_cbo.get()
    style.theme_use(theme_cbo_value)
    theme_selected.configure(text=theme_cbo_value)
    theme_cbo.selection_clear()
theme_cbo.bind('<<ComboboxSelected>>', change_theme)
theme_selected = ttk.Label(
        master=theme_selection,
        text="litera",
        font="-size 24 -weight bold"
)
theme_selected.pack(side=LEFT)

def create_frame1():
    global current_frame
    if current_frame:
        current_frame.destroy()
    current_frame = tb.Frame(app, height=600, width=1080, bootstyle="info")
    current_frame.pack(fill="both", expand=1)
    current_frame.pack_propagate(0)

    # 添加背景图片
    background_image = Image.open("resource/background.jpg")  # 替换为你的背景图片路径
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tb.Label(current_frame, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    # 添加原本主程序的按钮和布局
    center_label = tb.Label(current_frame, text="星雨晴空工具箱", font=("Helvetica", 24), borderwidth=2, relief="solid", bootstyle="lighe")
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

    # 添加背景图片
    background_image = Image.open("resource/background2.jpg")  # 替换为你的背景图片路径
    background_photo = ImageTk.PhotoImage(background_image)
    background_label = tb.Label(current_frame, image=background_photo)
    background_label.image = background_photo
    background_label.place(x=0, y=0, relwidth=1, relheight=1)

    center_label = tb.Label(current_frame, text="刷机工具", font=("Helvetica", 24), borderwidth=2, relief="solid", bootstyle="lighe")
    center_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)


    button_frame = tb.Frame(current_frame)
    button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

    buttons = [
        ("ADB TOOL", run_ADBtool),
        ("FASTBOOT TOOL", run_FASTBOOTtool),
        ("fastbootd tool", run_ftd),
        ("网站导航", run_web),
        ("GSI下载", run_gsi),
        ("A57 5G专区", run_a57)
    ]

    for i, (text, command) in enumerate(buttons):
        button = tb.Button(button_frame, text=text, command=command, bootstyle="success.Outline.TButton")
        button.grid(row=0, column=i, padx=5, pady=10)

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

    link_button1 = ttk.Button(right_frame, style="success-link", text="我的QQ", command=lambda: open_link("https://www.bilibili.com/video/BV1GJ411x7h7/?spm_id_from=333.337.search-card.all.click"))
    link_button1.pack(pady=10)

    link_button2 = ttk.Button(right_frame, style="success-link", text="github开源地址", command=lambda: open_link("https://github.com/messycodes/XYQKTOOL"))
    link_button2.pack(pady=10)

# 界面切换按钮
btn1 = tb.Button(button_frame, text='主页', command=lambda: switch_frame(create_frame1), bootstyle="info.Outline.TButton")
btn1.place(relx=0, rely=0, relwidth=0.3, relheight=1)

btn2 = tb.Button(button_frame, text='菜单', command=lambda: switch_frame(create_frame2), bootstyle="danger.Outline.TButton")
btn2.place(relx=0.3, rely=0, relwidth=0.3, relheight=1)

btn3 = tb.Button(button_frame, text='设置', command=lambda: switch_frame(create_frame3), bootstyle="success.Outline.TButton")
btn3.place(relx=0.6, rely=0, relwidth=0.4, relheight=1)

# 初始化显示第一个界面
current_frame = None
create_frame1()

# 窗口淡出
def end():
    for i in range(0, 105, 5)[::-1]:
        app.attributes('-alpha', i / 100)
        time.sleep(0.013)
        app.update()

# 绑定窗口关闭事件
def on_closing():
    end()
    app.destroy()

if __name__ == "__main__":
    config = configparser.ConfigParser()  # 创建配置文件解析器对象
    config.read('config.ini')  # 读取配置文件

    use_multithreading = config.getboolean('dependencies', 'use_multithreading', fallback=False)

    if not check_dependency_installed():
        print("依赖未安装。正在安装...")
        install_dependencies_with_animation(use_multithreading)  # 安装依赖并显示动画
        update_after_install = config.getboolean('dependencies', 'update_after_install', fallback=True)  # 检查是否需要在安装依赖后更新配置文件
        if update_after_install:
            print("更新配置...")
            update_config()  # 更新配置文件
    else:
        print("已经初始化过了，即将启动程序")

    # 运行淡入效果
    fade_in(app)

    # 绑定窗口关闭事件到函数
    app.protocol("WM_DELETE_WINDOW", on_closing)

    app.mainloop()

