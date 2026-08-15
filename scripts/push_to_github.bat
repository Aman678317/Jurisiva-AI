@echo off
echo ===============================================================================
echo Pushing Complete Next.js Configuration to GitHub (Aman678317/Jurisiva-AI)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "feat(nextjs): configure native next.js build, pages, and proxy rewrites"
git push origin main

echo ===============================================================================
echo Push Completed Successfully!
echo ===============================================================================
pause
