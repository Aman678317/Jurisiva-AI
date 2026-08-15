@echo off
echo ===============================================================================
echo Pushing Vercel Schema Fix (Removed 'public' property) to GitHub
echo ===============================================================================

git status
git add .
git commit -m "fix(vercel): remove invalid 'public' key in vercel.json"
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
