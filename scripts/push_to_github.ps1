Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Pushing Jurisiva-AI Production Codebase to GitHub (Aman678317/Jurisiva-AI)" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan

git status
git add .
git commit -m "feat(core): production architecture with multi-model AI router, NVIDIA NIM, DeepSeek-R1, GLM-2/4 failover, and Vercel/Render/Supabase deployment"
git branch -M main
git push origin main

Write-Host "===============================================================================" -ForegroundColor Cyan
Write-Host "Push Completed! Repository: https://github.com/Aman678317/Jurisiva-AI" -ForegroundColor Green
Write-Host "===============================================================================" -ForegroundColor Cyan
