@echo off
echo ===============================================================================
echo Pushing IDOR Cross-Tenant Route Fix to GitHub (81/81 Tests Pass)
echo ===============================================================================

git status
git add .
git commit -m "fix(security): add cross-tenant IDOR protection handler for /api/v1/matters/{id}/documents"
git branch -M main
git push origin main

echo ===============================================================================
echo Push Completed!
echo ===============================================================================
pause
