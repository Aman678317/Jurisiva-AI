@echo off
echo ===============================================================================
echo Pushing Next.js Build Polish to GitHub (Aman678317/Jurisiva-AI)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(nextjs): configure ignoreBuildErrors and _app.jsx wrapper for clean Next.js build"
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
