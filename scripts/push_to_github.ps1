Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Vercel Schema Fix (Removed 'public' property) to GitHub" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "fix(vercel): remove invalid 'public' key in vercel.json"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
