import ttkbootstrap as ttk
from ttkbootstrap.constants import *
import subprocess
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText

class FastbootToolbox(ttk.Window):
    def __init__(self):
        # 初始化窗口
        super().__init__(title="Fastboot 工具箱", themename="darkly")
        self.geometry("800x700")

        # 自动刷新标志
        self.auto_refresh_enabled = False

        # 创建并放置控件
        self.create_widgets()

    def create_widgets(self):
        # 创建主框架
        self.main_frame = ttk.Frame(self, bootstyle="secondary", padding=10)
        self.main_frame.pack(pady=20, padx=20, fill=BOTH, expand=True)

        # 创建文件选择框架
        self.file_frame = ttk.Frame(self.main_frame)
        self.file_frame.pack(side=LEFT, fill=BOTH, expand=True, padx=(0, 10))

        # 标签和文本框用于选择文件
        self.label = ttk.Label(self.file_frame, text="选择要刷入的文件：", bootstyle="primary")
        self.label.pack(pady=10)

        self.file_path_entry = ttk.Entry(self.file_frame, width=50)
        self.file_path_entry.pack(pady=5)

        self.browse_button = ttk.Button(self.file_frame, text="浏览", command=self.browse_file)
        self.browse_button.pack(pady=5)

        # 下拉框用于选择分区
        self.partition_label = ttk.Label(self.file_frame, text="选择或输入要刷入的分区：", bootstyle="primary")
        self.partition_label.pack(pady=10)

        self.partition_options = ["boot", "system", "vendor", "recovery", "vbmeta"]
        self.partition_combobox = ttk.Combobox(self.file_frame, values=self.partition_options)
        self.partition_combobox.pack(pady=5)

        # 下拉框用于选择槽
        self.slot_label = ttk.Label(self.file_frame, text="选择分区 (_a, _b, 或留空)：", bootstyle="primary")
        self.slot_label.pack(pady=10)

        self.slot_combobox = ttk.Combobox(self.file_frame, values=["", "_a", "_b"], state="readonly")
        self.slot_combobox.pack(pady=5)

        # 刷入按钮
        self.flash_button = ttk.Button(self.file_frame, text="刷入", bootstyle="success", command=self.flash_file)
        self.flash_button.pack(pady=20)

        # 创建重启选择框架
        self.reboot_frame = ttk.Frame(self.main_frame)
        self.reboot_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.reboot_label = ttk.Label(self.reboot_frame, text="选择重启模式：", bootstyle="primary")
        self.reboot_label.pack(pady=10)

        self.reboot_options = ["adb 系统", "adb recovery", "adb fastboot", "adb fastbootd", "fastboot 系统", "fastboot recovery", "fastboot 9008"]
        self.reboot_combobox = ttk.Combobox(self.reboot_frame, values=self.reboot_options)
        self.reboot_combobox.pack(pady=5)

        self.reboot_button = ttk.Button(self.reboot_frame, text="重启", bootstyle="warning", command=self.reboot_device)
        self.reboot_button.pack(pady=20)

        # 创建设备列表框架
        self.device_frame = ttk.Frame(self.reboot_frame)
        self.device_frame.pack(fill=BOTH, expand=True, pady=(20, 10))

        self.device_label = ttk.Label(self.device_frame, text="连接的设备：", bootstyle="primary")
        self.device_label.pack(pady=5)

        self.device_info_label = ttk.Label(self.device_frame, text="", bootstyle="secondary")
        self.device_info_label.pack(pady=5, fill=BOTH, expand=True)

        self.refresh_button = ttk.Button(self.device_frame, text="刷新", bootstyle="primary", command=self.refresh_devices)
        self.refresh_button.pack(pady=5)

        self.auto_refresh_checkbutton = ttk.Checkbutton(
            self.device_frame, 
            text="自动刷新设备", 
            bootstyle="round-toggle", 
            command=self.toggle_auto_refresh
        )
        self.auto_refresh_checkbutton.pack(pady=5)

        # 执行结果显示
        self.result_label = ttk.Label(self, text="执行结果：", bootstyle="primary")
        self.result_label.pack(pady=5)

        self.result_text = ScrolledText(self, height=10, state='disabled')
        self.result_text.pack(pady=5, padx=20, fill=BOTH, expand=True)

        self.clear_button = ttk.Button(self, text="清除", bootstyle="danger", command=self.clear_result)
        self.clear_button.pack(pady=5)

    def browse_file(self):
        # 打开文件选择对话框
        file_path = filedialog.askopenfilename(filetypes=[("所有文件", "*.*")])
        if file_path:
            self.file_path_entry.delete(0, ttk.END)
            self.file_path_entry.insert(0, file_path)

    def flash_file(self):
        # 获取文件路径、分区和槽
        file_path = self.file_path_entry.get()
        partition = self.partition_combobox.get()
        slot = self.slot_combobox.get()

        # 检查文件路径和分区是否为空
        if not file_path:
            messagebox.showerror("错误", "请选择要刷入的文件。")
            return
        if not partition:
            messagebox.showerror("错误", "请选择或输入要刷入的分区。")
            return

        # 构建命令
        partition_with_slot = f"{partition}{slot}"
        command = f"fastboot flash {partition_with_slot} {file_path}"

        # 执行命令并显示结果
        self.result_text.config(state='normal')
        self.result_text.insert(ttk.END, f"执行命令：{command}\n")
        self.result_text.see(ttk.END)
        self.result_text.config(state='disabled')
        
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.result_text.config(state='normal')
            self.result_text.insert(ttk.END, result.stdout)
            if result.returncode != 0:
                self.result_text.insert(ttk.END, result.stderr)
            self.result_text.see(ttk.END)
            self.result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：\n{str(e)}")

    def reboot_device(self):
        # 获取选择的重启模式
        reboot_mode = self.reboot_combobox.get()

        # 构建命令
        if reboot_mode == "adb 系统":
            command = "adb reboot"
        elif reboot_mode == "adb recovery":
            command = "adb reboot recovery"
        elif reboot_mode == "adb fastboot":
            command = "adb reboot bootloader"
        elif reboot_mode == "adb fastbootd":
            command = "adb reboot fastboot"
        elif reboot_mode == "fastboot 系统":
            command = "fastboot reboot"
        elif reboot_mode == "fastboot recovery":
            command = "fastboot reboot recovery"
        elif reboot_mode == "fastboot 9008":
            command = "fastboot oem edl"
        else:
            messagebox.showerror("错误", "请选择有效的重启模式。")
            return

        # 执行命令并显示结果
        self.result_text.config(state='normal')
        self.result_text.insert(ttk.END, f"执行命令：{command}\n")
        self.result_text.see(ttk.END)
        self.result_text.config(state='disabled')

        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            self.result_text.config(state='normal')
            self.result_text.insert(ttk.END, result.stdout)
            if result.returncode != 0:
                self.result_text.insert(ttk.END, result.stderr)
            self.result_text.see(ttk.END)
            self.result_text.config(state='disabled')
        except Exception as e:
            messagebox.showerror("错误", f"发生错误：\n{str(e)}")

    def refresh_devices(self):
        # 刷新设备列表
        adb_devices = self.check_adb_devices()
        fastboot_devices = self.check_fastboot_devices()

        all_devices = adb_devices + fastboot_devices

        if len(all_devices) > 1:
            messagebox.showerror("错误", "连接了两个及以上的设备。")
            return

        # 更新设备信息标签
        device_info_text = "\n".join(all_devices) if all_devices else "未检测到设备"
        self.device_info_label.config(text=device_info_text)

    def check_adb_devices(self):
        devices = []
        try:
            result = subprocess.run("adb devices", shell=True, capture_output=True, text=True)
            device_lines = result.stdout.strip().split("\n")[1:]  # 去掉标题行
            for device in device_lines:
                if device:
                    device_id = device.split()[0]
                    model = subprocess.run(f"adb -s {device_id} shell getprop ro.product.model", shell=True, capture_output=True, text=True)
                    devices.append(f"{device_id} - {model.stdout.strip()}")
        except Exception as e:
            messagebox.showerror("错误", f"检查 ADB 设备时出错：\n{str(e)}")
        return devices

    def check_fastboot_devices(self):
        devices = []
        try:
            result = subprocess.run("fastboot devices", shell=True, capture_output=True, text=True)
            device_lines = result.stdout.strip().split("\n")
            for device in device_lines:
                if device:
                    device_id = device.split()[0]
                    model = subprocess.run(f"fastboot -s {device_id} getvar product", shell=True, capture_output=True, text=True)
                    devices.append(f"{device_id} - {model.stdout.strip().split(':')[-1].strip()}")
        except Exception as e:
            messagebox.showerror("错误", f"检查 Fastboot 设备时出错：\n{str(e)}")
        return devices

    def auto_refresh_devices(self):
        if self.auto_refresh_enabled:
            self.refresh_devices()
            self.after(2000, self.auto_refresh_devices)

    def toggle_auto_refresh(self):
        self.auto_refresh_enabled = not self.auto_refresh_enabled
        if self.auto_refresh_enabled:
            self.auto_refresh_devices()

    def clear_result(self):
        # 确认清除结果
        if messagebox.askyesno("确认", "确定要清除执行结果吗？"):
            self.result_text.config(state='normal')
            self.result_text.delete(1.0, ttk.END)
            self.result_text.config(state='disabled')

if __name__ == "__main__":
    app = FastbootToolbox()
    app.mainloop()
