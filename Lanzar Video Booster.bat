@echo off
title PixarBoost - Video Booster Ultra
cd /d "%~dp0"
start "" pythonw app_video_booster.py
if %ERRORLEVEL% NEQ 0 (
    echo Iniciando con consola...
    python app_video_booster.py
    pause
)
