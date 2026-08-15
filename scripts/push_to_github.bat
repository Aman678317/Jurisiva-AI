@echo off
echo ===============================================================================
echo Pushing Vercel Root UI Route Fix to GitHub
echo ===============================================================================

git status
git add .
git commit -m "fix(web): serve complete frontend index.html on root route / in main.py and vercel"
git branch -M main
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
