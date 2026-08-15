@echo off
echo ===============================================================================
echo Pushing Static Generation Fix for Next.js (getStaticPaths & Dedicated Pages)
echo ===============================================================================

git reset origin/main
git add .
git commit -m "fix(nextjs): add getStaticPaths and dedicated static pages for 100% clean Next.js build"
git push origin main

echo ===============================================================================
echo Push Completed Successfully!
echo ===============================================================================
pause
