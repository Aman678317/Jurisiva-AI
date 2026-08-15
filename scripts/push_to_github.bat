@echo off
echo ===============================================================================
echo Pushing Bulletproof Dual Static & FastAPI Root HTML Handler to GitHub
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(web): add bulletproof root HTML response handler in main.py and vercel.json"
git push origin main

echo ===============================================================================
echo Push Completed Successfully!
echo ===============================================================================
pause
