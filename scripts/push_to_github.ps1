Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Jurisiva-AI Test Suite Fixes to GitHub (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(tests): resolve model router tier, token parser, entity aliases, sub-routing, and voice assistant checks"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
