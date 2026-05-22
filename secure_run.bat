@echo off
echo ========================================
echo 🔐 SECURE BOT LAUNCHER
echo ========================================
echo.
echo This launcher requires password authentication
echo to access encrypted bot files.
echo.
echo Files protected:
echo - main.py (read-only, encrypted)
echo - main2.py (read-only, encrypted)
echo - .env (read-only, encrypted)
echo.
python secure_launcher.py
pause