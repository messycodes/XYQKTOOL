@echo off
cd xyqk

TITLE ������տ��Žű�
color a
echo.
echo. �������������
echo.
echo. ��ϵ��ʽ��3442681588
echo. 
echo. ���������...
pause >nul
CLS
echo. ###############################
echo.
echo  ������������ѯQQ
echo.
echo. ################################
adb reboot fastboot
echo. ���������...
pause >nul
CLS
echo.
echo  ��ʼ�����豸...
echo.
fastboot.exe devices
echo.
echo. ����ˢ��boot...���������...
pause >nul
CLS
echo.
fastboot flash boot .\boot.img
fastboot flash boot_a .\boota.img
fastboot flash boot_b .\bootb.img
echo. ����������ֻ�...
pause >nul
CLS
echo.
echo. ROOT�ɹ����ֻ�����...
echo.
echo.
echo.
fastboot reboot
echo.
echo.
echo.
pause >nul
