@echo off
echo ===============================================================================
echo Pushing Next.js Dependency Fix for Vercel Build (Aman678317/Jurisiva-AI)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(vercel): add next dependency in package.json to resolve Vercel Next.js preset"
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
