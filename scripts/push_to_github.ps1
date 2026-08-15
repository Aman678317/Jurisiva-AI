Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Static Generation Fix for Next.js (getStaticPaths & Dedicated Pages)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(nextjs): add getStaticPaths and dedicated static pages for 100% clean Next.js build"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed Successfully! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
