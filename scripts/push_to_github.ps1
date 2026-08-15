Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Vercel Root UI Route Fix to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(web): serve complete frontend index.html on root route / in main.py and vercel"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
