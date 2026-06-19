@echo off
setlocal

set "REPO_ZIP=https://github.com/SeedOfAnarky/NviteAuto/archive/refs/heads/main.zip"
set "OUT_DIR=%~dp0"
set "ZIP_PATH=%OUT_DIR%NviteAuto.zip"
set "EXTRACT_PATH=%OUT_DIR%NviteAuto-main"
set "FINAL_PATH=%OUT_DIR%NviteAuto"

echo ============================================================
echo  NviteAuto Downloader
echo ============================================================
echo.
echo Downloading from GitHub...

powershell -NoProfile -Command "Invoke-WebRequest -Uri '%REPO_ZIP%' -OutFile '%ZIP_PATH%'"

if not exist "%ZIP_PATH%" (
    echo.
    echo ERROR: Download failed. Check your internet connection.
    pause
    exit /b 1
)

echo Done. Extracting...

powershell -NoProfile -Command "Expand-Archive -Path '%ZIP_PATH%' -DestinationPath '%OUT_DIR%' -Force"

if not exist "%EXTRACT_PATH%" (
    echo.
    echo ERROR: Extraction failed.
    pause
    exit /b 1
)

rem Remove old NviteAuto folder if it exists
if exist "%FINAL_PATH%" (
    echo Removing old NviteAuto folder...
    rmdir /s /q "%FINAL_PATH%"
)

rem The zip extracts to NviteAuto-main\NviteAuto\ — move the inner folder up
move "%EXTRACT_PATH%\NviteAuto" "%FINAL_PATH%"

rem Clean up the leftover NviteAuto-main shell and zip
rmdir /s /q "%EXTRACT_PATH%"
del "%ZIP_PATH%"

echo.
echo ============================================================
echo  Done! NviteAuto folder is ready at:
echo  %FINAL_PATH%
echo ============================================================
pause
