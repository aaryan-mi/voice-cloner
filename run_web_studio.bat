@echo off
title Voice Cloner Studio
cd /d "%~dp0"
echo Starting Voice Cloner Studio...
call .venv\Scripts\activate.bat
python web_app.py
pause
