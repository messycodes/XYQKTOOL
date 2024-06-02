@echo off
cd driver_mtk_qualcomm
cd driver_mtk_qualcomm/d %~dp0

set dirSeachMark=1
if not exist "%systemroot%\system32\drivers\usbser.sys" goto NotHaveSysFiles

cls
echo *************************************
echo *************Information*************
echo *************************************
echo Dirver Installer v1.0

for /f %%i in ('ver^|%systemroot%\system32\find.exe "5.0."') do echo Win NT && set osrecognized=2
for /f %%i in ('ver^|%systemroot%\system32\find.exe "5.1."') do echo Win XP && set osrecognized=2
for /f %%i in ('ver^|%systemroot%\system32\find.exe "5.2."') do echo Win 2003 && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "6.0."') do echo Win Vista && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "6.1."') do echo Win 7 && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "6.2."') do echo Win 8 && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "6.3."') do echo Win 8 && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "6.4."') do echo Win 8 && set osrecognized=1
for /f %%i in ('ver^|%systemroot%\system32\find.exe "10.0."') do echo Win 10 && set osrecognized=1

if not defined osrecognized goto NotSupport

@set PLATFORM=x86
@if "%PROCESSOR_IDENTIFIER:~0,3%"=="x86" (set PLATFORM=/SmartPhoneDriver/x86) ^
else (set PLATFORM=/SmartPhoneDriver/x64)

@set PLATFORM=%cd%%PLATFORM%

echo %PLATFORM%
@echo.
@echo.

if %osrecognized% EQU 1 goto newSystem


if exist "%systemroot%\inf\wpdmtp.inf" (set NumCountSec=0) else set NumCountSec=6
if %osrecognized% EQU 6 goto slzRun
if exist "%systemroot%\system32\drivers\WUDFRd.sys" (set NumCountSec=0) else set NumCountSec=6
if %osrecognized% EQU 6 goto slzRun
if exist "%systemroot%\system32\drivers\wpdusb.sys" (set NumCountSec=0) else set NumCountSec=6
:slzRun

if %NumCountSec% equ 0 (goto:endCount) else set /a NumCountSec-=1
echo 未安装Media Player 11,%NumCountSec% 秒后自动执行安装，请在安装完后重启
echo Not installed Media Player 11,%NumCountSec% seconds to perform the installation, please reboot after installation
ping -n 2 127.0.1>nul 2>nul&cls
set osrecognizedCount=2

goto:slzRun
:endCount

if defined osrecognizedCount goto InstallMedia

echo *******************************************
echo **********Install mtp inf******************
echo *******************************************
"%PLATFORM%/dpinst.exe" /PATH "%cd%/SmartPhoneDriver/windowsXP" /F /LM /SW /A
echo Install complete!
@echo.
@echo.

:newSystem

echo *******************************************
echo **********Install adb inf******************
echo *******************************************
"%PLATFORM%/dpinst.exe" /PATH "%PLATFORM%\adb infs" /F /LM /SW /A
echo Install complete!
@echo.
@echo.


echo *******************************************
echo **********Install SP unsigned inf**********
echo *******************************************
"%PLATFORM%/dpinst.exe" /PATH "%PLATFORM%\Unsigned infs" /F /LM /SW /A
echo Install complete!
@echo.
@echo.


echo *****************************************
echo **********Install SP Qcom inf************
echo *****************************************
"%PLATFORM%/dpinst.exe" /PATH "%PLATFORM%\WindowsQcom" /F /LM /SW /A
echo Install complete!
@echo.
@echo.


echo *****************************************
echo **********Install Fastboot inf***********
echo *****************************************
"%PLATFORM%/dpinst.exe" /PATH "%PLATFORM%\fastboot_driver" /F /LM /SW /A
echo Install complete!
@echo.
@echo.

goto end

:InstallMedia
"%cd%/adbdriver.exe"
goto end

:NotHaveSysFiles
echo 此系统未含有系统文件,请按照目录下的帮助文档操作。
echo System file did not contain a directory, please follow the help document operation.
goto end

:NotSupport
echo Do Not support Win NT earlier version

:end
pause
