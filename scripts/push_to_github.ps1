Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Vercel OutputDirectory Fix to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(vercel): configure outputDirectory apps/web and /index.html rewrite"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
