@echo off
setlocal EnableExtensions
cd /d "%~dp0"
for /f "delims=" %%B in ('git branch --show-current') do set "BRANCH=%%B"
if not "%BRANCH%"=="main" (
  echo Switch to main before syncing the course fork.
  pause
  exit /b 1
)
for /f "delims=" %%S in ('git status --porcelain') do (
  echo Commit your local changes before syncing.
  pause
  exit /b 1
)
git pull --ff-only origin main
if errorlevel 1 goto failed
git fetch upstream
if errorlevel 1 goto failed
git merge --no-edit upstream/main
if errorlevel 1 goto failed
git push origin main
if errorlevel 1 goto failed
echo Course updates synced to tjdbsdn0115/2026-2DGP.
pause
exit /b 0
:failed
echo Sync stopped. Check the Git message above; resolve any merge conflicts before pushing.
pause
exit /b 1
