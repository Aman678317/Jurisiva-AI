Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Complete Next.js Configuration to GitHub (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "feat(nextjs): configure native next.js build, pages, and proxy rewrites"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed Successfully! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
