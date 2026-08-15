@echo off
echo ===============================================================================
echo Pushing Jurisiva-AI Fix to GitHub (Aman678317/Jurisiva-AI)
echo ===============================================================================

git status
git add .
git commit -m "fix(syntax): resolve case_store unclosed dictionary and sync flake8 linting"
git branch -M main
git push origin main

echo ===============================================================================
echo Code successfully pushed to https://github.com/Aman678317/Jurisiva-AI
echo ===============================================================================
pause
