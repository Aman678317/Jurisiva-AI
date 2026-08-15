Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Bulletproof Dual Static & FastAPI Root HTML Handler to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(web): add bulletproof root HTML response handler in main.py and vercel.json"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed Successfully! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
