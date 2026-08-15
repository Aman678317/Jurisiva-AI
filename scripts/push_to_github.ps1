Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Vercel Static Frontend Resolution Fix to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(vercel): map rewrites directly to /apps/web/index.html to resolve 404"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
