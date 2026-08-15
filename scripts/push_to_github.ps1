Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Vercel Build & Live Production Fixes to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(vercel): resolve static build command and set default live Render API url"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
