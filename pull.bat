@echo off
setlocal EnableExtensions
cd /d "%~dp0"
for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
if not defined BRANCH goto failed
git pull --ff-only origin "%BRANCH%"
if errorlevel 1 goto failed
echo Pull complete: tjdbsdn0115/2026-2DGP
pause
exit /b 0
:failed
echo Pull failed. Check the Git message above.
pause
exit /b 1
