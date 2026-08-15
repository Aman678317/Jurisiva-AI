Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Static Generation Fix to GitHub (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(nextjs): add static paths, dedicated pages, and disable telemetry"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed Successfully! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
