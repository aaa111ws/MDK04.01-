@echo off
title Biblioteka - BUILD
cd /d "%~dp0..\pr5"
set DB_ENGINE=sqlite
set PYTHONIOENCODING=utf-8

set PY=
py -3 --version >nul 2>nul && set PY=py -3
if not defined PY python --version >nul 2>nul && set PY=python
if not defined PY (
    echo Python not found. Install Python 3.10+ from python.org and run BUILD.bat again.
    pause
    exit /b 1
)

echo [1/4] Installing libraries...
%PY% -m pip install --user --disable-pip-version-check Django==5.1.4 djangorestframework==3.14.0 djangorestframework-simplejwt==5.3.1 django-cors-headers==4.3.1 django-filter==23.5 python-dotenv==1.0.1
if errorlevel 1 (
    echo pip install failed. Check the internet connection.
    pause
    exit /b 1
)

echo [2/4] Creating database...
%PY% manage.py migrate
if errorlevel 1 ( pause & exit /b 1 )

echo [3/4] Demo data...
%PY% "%~dp0seed.py"

echo [4/4] Opening VS Code and browser...
set CODE=
where code >nul 2>nul && set CODE=code
if not defined CODE if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd" set CODE="%LOCALAPPDATA%\Programs\Microsoft VS Code\bin\code.cmd"
if not defined CODE if exist "%ProgramFiles%\Microsoft VS Code\bin\code.cmd" set CODE="%ProgramFiles%\Microsoft VS Code\bin\code.cmd"
if defined CODE (call %CODE% "%~dp0..") else (echo VS Code not found, skipping.)
start "" cmd /c "timeout /t 5 >nul & start http://127.0.0.1:8000/admin/"

echo.
echo Login: admin / Admin12345
echo Do not close this window while working. Ctrl+C - stop server.
echo.
%PY% manage.py runserver 127.0.0.1:8000
pause
