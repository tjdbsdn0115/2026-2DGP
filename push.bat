@echo off
setlocal EnableExtensions
cd /d "%~dp0"
for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
if not defined BRANCH goto failed
set "HAS_CHANGES="
for /f "delims=" %%S in ('git status --porcelain') do set "HAS_CHANGES=1"
if not defined HAS_CHANGES goto push
set /p "COMMIT_MESSAGE=Commit message: "
if not defined COMMIT_MESSAGE goto failed
git add -A
if errorlevel 1 goto failed
git commit -m "%COMMIT_MESSAGE%"
if errorlevel 1 goto failed
:push
git push -u origin "%BRANCH%"
if errorlevel 1 goto failed
echo Push complete: tjdbsdn0115/2026-2DGP
pause
exit /b 0
:failed
echo Operation failed. Check the Git message above.
pause
exit /b 1
