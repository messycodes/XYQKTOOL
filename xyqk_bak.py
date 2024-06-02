import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk
import os
import configparser
import subprocess
from rich import traceback
import threading
import time
from rich.progress import Progress, BarColumn, TimeRemainingColumn


traceback.install(show_locals=True)

def check_dependency_installed():
    """
    检查配置文件中的依赖是否已安装

    Returns:
        bool: 如果依赖已安装，则返回True；否则返回False。
    """
    config = configparser.ConfigParser()  # 创建配置文件解析器对象
    config.read('config.ini')  # 读取配置文件
    dependency_installed = config.getboolean('dependencies', 'installed')  # 获取配置文件中的依赖安装状态
    return dependency_installed

def install_dependencies():
    """
    使用pip安装依赖
    """
    dependencies = ['scapy', 'ttkthemes', 'ttkbootstrap','PyQt-Fluent-Widgets']  # 在列表中指定要安装的多个依赖
    with Progress() as progress:  # 创建进度条
        task = progress.add_task("[cyan]Installing dependencies...", total=len(dependencies))  # 添加任务到进度条
        for dependency in dependencies:
            subprocess.run(['pip', 'install', dependency])  # 使用pip命令安装依赖
            progress.advance(task)  # 更新进度条

def update_config():
    """
    更新配置文件中的依赖安装状态为已安装
    """
    config = configparser.ConfigParser()  # 创建配置文件解析器对象
    config.read('config.ini')  # 读取配置文件
    config.set('dependencies', 'installed', 'True')  # 更新配置文件中的依赖安装状态
    with open('config.ini', 'w') as configfile:
        config.write(configfile)  # 将更新后的配置写回配置文件

if __name__ == "__main__":
    if not check_dependency_installed():
        print("Dependencies not installed. Installing...")
        install_dependencies()  # 安装依赖
        config = configparser.ConfigParser()  # 创建配置文件解析器对象
        config.read('config.ini')  # 读取配置文件
        update_after_install = config.getboolean('dependencies', 'update_after_install')  # 检查是否需要在安装依赖后更新配置文件
        if update_after_install:
            print("Updating config...")
            update_config()  # 更新配置文件
    else:
        print("已经初始化过了，即将启动程序")

def run_program(command):
    """Run a specified command in a new subprocess."""
    subprocess.Popen(command, shell=True)

def run_program1():
    print("Running ROOT")
    os.system("cmd/c start boot一键ROOT.bat")
    os.chdir('.')

def run_program2():
    print("Running GSI")


def run_program3():
    print("Running cmd")
    os.system("cmd/c start cd xyqk")

def run_program4():
    print("Running DM")
    os.system("cmd/c start dm.bat")

def run_program5():
    print("Running drivers")
    os.system("cmd/c start install-driver.bat")

def run_program6():
    print("Running install 7-zip")
    run_program("7-zip.exe")

def run_program7():
    print("Running Pay")
    run_program("python pay.py")

# 创建应用程序窗口
app = tb.Window(themename='darkly')
app.title('XYQK TOOL 1.2')
app.geometry("600x400")
app.resizable(False, False)  # 禁止改变窗口大小
app.iconbitmap('favicon.ico')

# 加载背景图片
background_image = Image.open("background.jpg")  # 替换为你的背景图片路径
background_photo = ImageTk.PhotoImage(background_image)

# 创建背景标签
background_label = ttk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

# 创建一个居中的大标签
center_label = ttk.Label(app, text="星雨晴空工具箱", font=("Helvetica", 24), borderwidth=2, relief="solid", foreground="white")
center_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

# 创建按钮并设置命令
button_frame = ttk.Frame(app)
button_frame.place(relx=0.5, rely=0.6, anchor=tk.CENTER)

buttons = [
    ("root", run_program1),
    ("刷gsi", run_program2),
    ("cmd", run_program3),
    ("去dm校检", run_program4),
    ("驱动", run_program5),
    ("7-zip", run_program6),
    ("收款", run_program7)
]

for i, (text, command) in enumerate(buttons):
    button = tb.Button(button_frame, text=text, command=command, bootstyle="success.Outline.TButton")
    button.grid(row=0, column=i, padx=5, pady=10)

app.mainloop()