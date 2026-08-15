@echo off
echo ===============================================================================
echo Pushing Vercel OutputDirectory Fix to GitHub (apps/web/index.html)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(vercel): configure outputDirectory apps/web and /index.html rewrite"
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
