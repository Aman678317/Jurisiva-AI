@echo off
echo ===============================================================================
echo Pushing Static Generation Fix to GitHub (Aman678317/Jurisiva-AI)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(nextjs): add static paths, dedicated pages, and disable telemetry"
git push origin main

echo ===============================================================================
echo Push Completed Successfully!
echo ===============================================================================
pause
