@echo off
TITLE 星雨晴空开放脚本
color a
echo.
echo. 制作：星雨晴空
echo. 星雨晴空开放脚本 AB分区通用专版 A分区
echo. 联系方式：3442681588
echo. 
echo. 任意键继续...
pause >nul
CLS
echo. ###############################
echo.
echo  如有疑问请咨询QQ,AB分区专用
echo.
echo. 可能需要的操作:
echo.
echo. 1.把手机关机
echo.
echo. 2.关机状态按住音量下+开机键开机
echo.
echo  3.屏幕留在fastbootd界面
echo.
echo. 4.手机连接电脑
echo.
echo. ################################
echo.
echo. 任意键继续...
pause >nul
CLS
echo.
echo  开始连接设备...
echo.
adb reboot fastboot
echo.
fastboot.exe devices
echo.
echo. 即将清除厂商my分区...任意键继续...
pause >nul
CLS
echo.
fastboot delete-logical-partition my_stock_a
fastboot delete-logical-partition my_version_a
fastboot delete-logical-partition my_region_a
fastboot delete-logical-partition my_product_a
fastboot delete-logical-partition my_preload_a
fastboot delete-logical-partition my_manifest_a
fastboot delete-logical-partition my_manifest_a
fastboot delete-logical-partition my_heytap_a
fastboot delete-logical-partition my_engineering_a
fastboot delete-logical-partition my_company_a
fastboot delete-logical-partition my_carrier_a
fastboot delete-logical-partition my_bigball_a
echo. 任意键开始刷入GSI...
echo. 任意键继续...
pause >nul
CLS
echo.
echo  开始刷入GSI...
echo.
fastboot flash system_a system.img
fastboot format userdata
echo. 任意键继续...
pause >nul
CLS
echo.
echo  需要重启到rec,进入rec请手动清除data数据...
echo.
adb reboot recovery
echo.
echo.
echo.
pause >nul
