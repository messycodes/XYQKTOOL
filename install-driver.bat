@echo off
cd install-driver
color 2b &mode 50,7
title SAMTRIX Driver Installer
echo.&echo            SAMTRIX DRIVER INSTALLER
echo.&echo  Click YES and allow installation of all drivers
echo.&echo  Always click INSTALL THIS DRIVER SOFTWARE ANYWAY
reg Query "HKLM\Hardware\Description\System\CentralProcessor\0" | find /i "x86" > NUL && start /wait "" "drivers\UsbDk_1.0.22_x86.msi" || start /wait "" "drivers\UsbDk_1.0.22_x64.msi"
start /wait "" "drivers\QcomMtk_Driver_Setup_3.1.9.exe"
start fastbootD.exe
start MediaTek_Driver_Packages_5.14.53.00.exe
start vivo_usb.exe
start SAMSUNG_USB_Driver_v1.7.59.0.exe
start qualcomm.exe
start huaweinb.exe
start Install.bat
start adb1.4.3.exe
exit