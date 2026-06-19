@echo off
setlocal

rem %~dp0 = the folder this .bat file is running from, automatically
set "SCRIPT_DIR=%~dp0"
set "SCRIPT_PATH=%SCRIPT_DIR%MyGameTool.py"

echo Installing "Run Game Tool" using script at:
echo %SCRIPT_PATH%
echo.

if not exist "%SCRIPT_PATH%" (
    echo ERROR: MyGameTool.py was not found next to this installer.
    echo Make sure install.bat and MyGameTool.py are in the same folder.
    pause
    exit /b 1
)

reg add "HKCR\exefile\shell\MyGameTool" /ve /d "Run Game Tool" /f >nul
reg add "HKCR\exefile\shell\MyGameTool" /v "Icon" /d "cmd.exe" /f >nul
reg add "HKCR\exefile\shell\MyGameTool\command" /ve /d "cmd /k py \"%SCRIPT_PATH%\" \"%%1\"" /f >nul

echo.
echo Done! Right-click any .exe file and choose "Run Game Tool".
echo (If you move this folder later, just run install.bat again.)
pause
