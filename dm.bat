@echo off
cd xyqk
color a
echo. 任意键继续...
pause >nul
CLS
echo  开始连接设备...
echo.
adb reboot fastboot
echo.
fastboot.exe devices
echo.
fastboot oem disable_dm_verity
fastboot oem enable_dm_verity
fastboot oem disable_dm_verity
fastboot reboot