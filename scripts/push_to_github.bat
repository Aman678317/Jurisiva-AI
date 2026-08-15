@echo off
echo ===============================================================================
echo Pushing Jurisiva-AI Test Suite Fixes to GitHub (Aman678317/Jurisiva-AI)
echo ===============================================================================

git status
git add .
git commit -m "fix(tests): resolve model router tier, token parser, entity aliases, sub-routing, and voice assistant checks"
git branch -M main
git push origin main

echo ===============================================================================
echo Code successfully pushed to https://github.com/Aman678317/Jurisiva-AI
echo ===============================================================================
pause
