Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Resetting to Remote origin/main and Pushing Clean Commit" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(deploy): complete deployment configuration, port binding, and test fixes"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed Successfully! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
