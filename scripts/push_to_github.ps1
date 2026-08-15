Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Render Port Binding & Production Fixes to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(deploy): bind dynamic PORT env variable (10000) for Render Web Service in Dockerfile and main"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
