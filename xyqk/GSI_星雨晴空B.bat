@echo off
TITLE ������տ��Žű�
color a
echo.
echo. �������������
echo. ������տ��Žű� AB����ͨ��ר�� B����
echo. ��ϵ��ʽ��3442681588
echo. 
echo. ���������...
pause >nul
CLS
echo. ###############################
echo.
echo  ������������ѯQQ,AB����ר��
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
fastboot delete-logical-partition my_stock_b
fastboot delete-logical-partition my_version_b
fastboot delete-logical-partition my_region_b
fastboot delete-logical-partition my_product_b
fastboot delete-logical-partition my_preload_b
fastboot delete-logical-partition my_manifest_b
fastboot delete-logical-partition my_manifest_b
fastboot delete-logical-partition my_heytap_b
fastboot delete-logical-partition my_engineering_b
fastboot delete-logical-partition my_company_b
fastboot delete-logical-partition my_carrier_b
fastboot delete-logical-partition my_bigball_b
echo. �������ʼˢ��GSI...
echo. ���������...
pause >nul
CLS
echo.
echo  ��ʼˢ��GSI...
echo.
fastboot flash system_b system.img
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
