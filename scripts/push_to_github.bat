@echo off
echo ===============================================================================
echo Pushing Vercel Build & Live Production Fixes to GitHub
echo ===============================================================================

git status
git add .
git commit -m "fix(vercel): resolve static build command and set default live Render API url"
git branch -M main
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
