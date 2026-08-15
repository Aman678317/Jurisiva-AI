@echo off
echo ===============================================================================
echo Resetting to Remote origin/main and Pushing Clean Commit (No Secrets in History)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(deploy): complete deployment configuration, port binding, and test fixes"
git push origin main

echo ===============================================================================
echo Push Completed Successfully!
echo ===============================================================================
pause
