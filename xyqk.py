import os
import configparser
import subprocess
import threading
import time
from rich import traceback
from PyQt5 import QtCore, QtGui, QtWidgets
import sys
import tkinter as tk
from tkinter import ttk
import ttkbootstrap as tb
from PIL import Image, ImageTk

traceback.install(show_locals=True)

class LoadingProgress(QtWidgets.QDialog):
    update_signal = QtCore.pyqtSignal(bool)

    def __init__(self, parent=None):
        super(LoadingProgress, self).__init__(parent)
        self.setStyleSheet("background-color: white;")
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowTitleHint | QtCore.Qt.CustomizeWindowHint | QtCore.Qt.WindowStaysOnTopHint)
        self.setFixedSize(200, 150)  # Set a fixed size for the dialog to make it non-resizable
        self.setWindowTitle("安装依赖中")  # Set the window title
        self.value = 0
        self.update_signal.connect(self.update_progress)
        vbox = QtWidgets.QVBoxLayout(self)
        self.steps = ["可能需要几分钟",
                      "即将完成",
                      "快了快了",
                      "依赖安装中..."]
        self.movie_label = QtWidgets.QLabel()
        self.movie = QtGui.QMovie("loading.gif")
        self.movie_label.setMovie(self.movie)
        self.movie.start()
        self.progress_label = QtWidgets.QLabel()
        # Load the custom font
        font_id = QtGui.QFontDatabase.addApplicationFont("HarmonyOS_Sans_Regular.ttf")
        if font_id != -1:
            font_family = QtGui.QFontDatabase.applicationFontFamilies(font_id)[0]
            custom_font = QtGui.QFont(font_family)
            self.progress_label.setFont(custom_font)
        self.label_update()

        vbox.addWidget(self.movie_label)
        vbox.addWidget(self.progress_label)
        self.setLayout(vbox)
        
    def label_update(self):
        self.progress_label.setText(self.steps[self.value])
        self.progress_label.setAlignment(QtCore.Qt.AlignCenter)

    def update_progress(self, boolean: bool) -> None:
        self.value += 1
        if boolean and self.value < len(self.steps):
            self.label_update()
        else:
            self.close()

def check_dependency_installed():
    config = configparser.ConfigParser()
    config.read('config.ini')
    dependency_installed = config.getboolean('dependencies', 'installed')
    return dependency_installed

def install_dependencies(progress_dialog):
    dependencies = ['scapy', 'ttkthemes', 'ttkbootstrap', 'PyQt-Fluent-Widgets']
    for i, dependency in enumerate(dependencies):
        subprocess.run(['pip', 'install', dependency])
        progress_dialog.update_signal.emit(i < len(dependencies) - 1)

def update_config():
    config = configparser.ConfigParser()
    config.read('config.ini')
    config.set('dependencies', 'installed', 'True')
    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def run_installation(update_after_install):
    app = QtWidgets.QApplication(sys.argv)
    progress_dialog = LoadingProgress()
    progress_dialog.show()
    
    installation_thread = threading.Thread(target=install_dependencies, args=(progress_dialog,))
    installation_thread.start()
    
    app.exec_()
    installation_thread.join()
    
    if update_after_install:
        update_config()

if __name__ == "__main__":
    if not check_dependency_installed():
        print("Dependencies not installed. Installing...")
        config = configparser.ConfigParser()
        config.read('config.ini')
        update_after_install = config.getboolean('dependencies', 'update_after_install')
        run_installation(update_after_install)
    else:
        print("已经初始化过了，即将启动程序")

def run_program(command):
    subprocess.Popen(command, shell=True)

def run_program1():
    print("Running ROOT")
    os.system("cmd /c start boot一键ROOT.bat")

def run_program2():
    print("Running GSI")

def run_program3():
    print("Running cmd")
    os.system("cmd /c start cd xyqk")

def run_program4():
    print("Running DM")
    os.system("cmd /c start dm.bat")

def run_program5():
    print("Running drivers")
    os.system("cmd /c start install-driver.bat")

def run_program6():
    print("Running install 7-zip")
    run_program("7-zip.exe")

def run_program7():
    print("Running Pay")
    run_program("python pay.py")

app = tb.Window(themename='darkly')
app.title('XYQK TOOL 1.2')
app.geometry("600x400")
app.resizable(False, False)
app.iconbitmap('favicon.ico')

background_image = Image.open("background.jpg")
background_photo = ImageTk.PhotoImage(background_image)

background_label = ttk.Label(app, image=background_photo)
background_label.place(x=0, y=0, relwidth=1, relheight=1)

center_label = ttk.Label(app, text="星雨晴空工具箱", font=("Helvetica", 24), borderwidth=2, relief="solid", foreground="white")
center_label.place(relx=0.5, rely=0.4, anchor=tk.CENTER)

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