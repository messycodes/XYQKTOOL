@echo off
cd xyqk
color a
echo. ���������...
pause >nul
CLS
echo  ��ʼ�����豸...
echo.
adb reboot fastboot
echo.
fastboot.exe devices
echo.
fastboot oem disable_dm_verity
fastboot oem enable_dm_verity
fastboot oem disable_dm_verity
fastboot reboot