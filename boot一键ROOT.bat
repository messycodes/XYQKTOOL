@echo off
cd xyqk

TITLE 星雨晴空开放脚本
color a
echo.
echo. 制作：星雨晴空
echo.
echo. 联系方式：3442681588
echo. 
echo. 任意键继续...
pause >nul
CLS
echo. ###############################
echo.
echo  如有疑问请咨询QQ
echo.
echo. ################################
adb reboot fastboot
echo. 任意键继续...
pause >nul
CLS
echo.
echo  开始连接设备...
echo.
fastboot.exe devices
echo.
echo. 即将刷人boot...任意键继续...
pause >nul
CLS
echo.
fastboot flash boot .\boot.img
fastboot flash boot_a .\boota.img
fastboot flash boot_b .\bootb.img
echo. 任意键重启手机...
pause >nul
CLS
echo.
echo. ROOT成功，手机重启...
echo.
echo.
echo.
fastboot reboot
echo.
echo.
echo.
pause >nul
