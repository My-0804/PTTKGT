@echo off
title Music Playlist Manager
cd /d "%~dp0"
python -m pip install -r requirements.txt
python app.py
pause
