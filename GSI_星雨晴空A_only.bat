@echo off
TITLE ������տ��Žű�
color a
echo.
echo. �������������
echo. ������տ��Žű� A Only����ͨ��ר��
echo. ��ϵ��ʽ��3442681588
echo. 
echo. ���������...
pause >nul
CLS
echo. ###############################
echo.
echo  ������������ѯQQ,A Only����ר��
echo.
echo. ������Ҫ�Ĳ���:
echo.
echo. 1.���ֻ��ػ�
echo.
echo. 2.�ػ�״̬��ס������+����������
echo.
echo  3.��Ļ����fastbootd����
echo.
echo. 4.�ֻ����ӵ���
echo.
echo. ################################
echo.
echo. ���������...
pause >nul
CLS
echo.
echo  ��ʼ�����豸...
echo.
adb reboot fastboot
echo.
fastboot.exe devices
echo.
echo. �����������my����...���������...
pause >nul
CLS
echo.
fastboot delete-logical-partition my_stock
fastboot delete-logical-partition my_version
fastboot delete-logical-partition my_region
fastboot delete-logical-partition my_product
fastboot delete-logical-partition my_preload
fastboot delete-logical-partition my_manifest
fastboot delete-logical-partition my_manifest
fastboot delete-logical-partition my_heytap
fastboot delete-logical-partition my_engineering
fastboot delete-logical-partition my_company
fastboot delete-logical-partition my_carrier
fastboot delete-logical-partition my_bigball
echo. �������ʼˢ��GSI...
echo. ���������...
pause >nul
CLS
echo.
echo  ��ʼˢ��GSI...
echo.
fastboot flash system system.img
fastboot format userdata
echo. ���������...
pause >nul
CLS
echo.
echo  ��Ҫ������rec,����rec���ֶ����data����...
echo.
adb reboot recovery
echo.
echo.
echo.
pause >nul
