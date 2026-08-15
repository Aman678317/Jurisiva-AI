@echo off
echo ===============================================================================
echo Pushing Render Port Binding & Production Fixes to GitHub
echo ===============================================================================

git status
git add .
git commit -m "fix(deploy): bind dynamic PORT env variable (10000) for Render Web Service in Dockerfile and main"
git branch -M main
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
