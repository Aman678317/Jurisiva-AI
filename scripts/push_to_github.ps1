Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Jurisiva-AI Fix to GitHub (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(syntax): resolve case_store unclosed dictionary and sync flake8 linting"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
