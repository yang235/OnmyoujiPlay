@echo off
chcp 65001 >nul
set "PYTHONHOME=%~dp0runtime"
set "PYTHONPATH=%~dp0"
set "PATH=%~dp0runtime;%~dp0runtime\DLLs;%~dp0runtime\Lib;%PATH%"
set "TCL_LIBRARY=%~dp0runtime\tcl\tcl8.6"
set "TK_LIBRARY=%~dp0runtime\tcl\tk8.6"
if not exist "%~dp0output" mkdir "%~dp0output"
if not exist "%~dp0output\gouxie" mkdir "%~dp0output\gouxie"
"%~dp0runtime\python.exe" "%~dp0ui_control\ui\tk.py"
pause
