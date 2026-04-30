@echo off
title Nu4g3 / Webhook Manager
chcp 65001 >nul
mode con: cols=50 lines=15
goto find_python

:find_python
echo [36mChecking for Python...[0m
timeout /t 1 >nul
where python >nul 2>&1
timeout /t 1 >nul
if %errorlevel% equ 0 (
    cls
    echo [36mPython found. Installing dependencies...[0m
    timeout /t 1 >nul
    pip install -r requirements.txt
    timeout /t 1 >nul
    if %errorlevel% equ 0 (
        cls
        echo [32mRequirements installed successfully.[0m
        echo.
        timeout /t 1 >nul
        start wehbook_manager.py
        timeout /t 2 >nul
        exit /b
    ) else (
        cls
        echo [31mFailed to install dependencies.[0m
        timeout /t 2 >nul
        exit /b
    )
) else (
    cls
    echo [31mPython not found. Please install Python 3.8 or higher.[0m
    timeout /t 2 >nul
    exit /b
)