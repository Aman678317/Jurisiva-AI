Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Next.js Dependency Fix for Vercel Build (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git reset origin/main
git add .
git commit -m "fix(vercel): add next dependency in package.json to resolve Vercel Next.js preset"
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
