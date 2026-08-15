@echo off
echo ===============================================================================
echo Pushing Vercel Static Frontend Resolution Fix to GitHub
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(vercel): map rewrites directly to /apps/web/index.html to resolve 404"
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
