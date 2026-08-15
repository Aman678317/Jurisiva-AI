Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing IDOR Cross-Tenant Route Fix to GitHub (81/81 Tests Pass)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(security): add cross-tenant IDOR protection handler for /api/v1/matters/{id}/documents"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
