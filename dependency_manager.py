import configparser
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed
import threading
from pathlib import Path
import sys

def check_dependency_installed(config_path):
    """
    检查配置文件中的依赖是否已安装

    返回:
        bool: 如果依赖已安装，则返回True；否则返回False。
    """
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        return config.getboolean('dependencies', 'installed', fallback=False)
    except Exception as e:
        print(f"读取配置文件时出错: {e}", file=sys.stderr)
        return False

def install_dependency(dependency):
    """
    安装单个依赖
    """
    try:
        subprocess.run(['pip', 'install', dependency], check=True)
        return dependency
    except subprocess.CalledProcessError as e:
        print(f"安装依赖 {dependency} 时出错: {e}", file=sys.stderr)
        return None

def install_dependencies(progress_bar, progress_label, install_window, use_multithreading, config_path):
    """
    使用pip安装依赖，并更新进度条
    """
    dependencies = ['scapy', 'ttkthemes', 'ttkbootstrap', 'rich']

    if use_multithreading:
        with ThreadPoolExecutor(max_workers=4) as executor:
            future_to_dependency = {executor.submit(install_dependency, dep): dep for dep in dependencies}
            for i, future in enumerate(as_completed(future_to_dependency), 1):
                dep = future_to_dependency[future]
                try:
                    if future.result():
                        print(f"{dep} 安装成功")
                    else:
                        print(f"{dep} 安装失败")
                except Exception as exc:
                    print(f"{dep} 安装失败: {exc}")
                progress_bar['value'] = i * (100 / len(dependencies))
                progress_label.config(text=f"正在安装 {dep} ({i}/{len(dependencies)})")
    else:
        for i, dependency in enumerate(dependencies, 1):
            install_dependency(dependency)
            progress_bar['value'] = i * (100 / len(dependencies))
            progress_label.config(text=f"正在安装 {dependency} ({i}/{len(dependencies)})")

    install_window.after(0, install_window.destroy)

def update_config(config_path):
    """
    更新配置文件中的依赖安装状态为已安装
    """
    try:
        config = configparser.ConfigParser()
        config.read(config_path)
        config.set('dependencies', 'installed', 'True')
        with open(config_path, 'w') as configfile:
            config.write(configfile)
    except Exception as e:
        print(f"更新配置文件时出错: {e}", file=sys.stderr)
