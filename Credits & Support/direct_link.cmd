@echo off
title Credits and Support
chcp 65001 >nul
mode con: cols=80 lines=25
goto cs 

:cs
cls
start https://github.com/Nu4g3
echo Github link was opened.
timeout /t 3 >nul
start https://discord.gg/RGv9YvH3Fq
echo Discord link was opened.
timeout /t 3 >nul
cls
exit /b