# Production Rollback Procedure

This document provides immediate, step-by-step instructions for rolling back Jurisiva-AI components in the event of an incident or deployment regression.

---

## 🛑 1. Frontend Rollback (Vercel)

If a breaking bug or UI regression is detected on the frontend:

1. Open **Vercel Dashboard > Jurisiva Project > Deployments**.
2. Locate the previous healthy deployment.
3. Click the three dots menu `...` > **Instant Rollback**.
4. Vercel will instantly point `app.jurisiva.ai` and `www.jurisiva.ai` back to the previous deployment in `< 10 seconds`.

---

## 🛑 2. Backend & Worker Rollback (Render)

If the FastAPI API or Background Worker encounters fatal errors or health probe failures:

1. Open **Render Dashboard > `jurisiva-api` / `jurisiva-worker` > Deploys**.
2. Click **Rollback to this deploy** on the last stable commit.
3. Render automatically reinstates the previous container image with zero downtime.
4. Verify `/health` and `/ready` endpoints:
   ```bash
   curl -i https://api.jurisiva.ai/ready
   ```

---

## 🛑 3. Database Migration Rollback (Supabase)

If a database migration caused issues:

1. Review the destructive change (ensure you follow the Expand $\rightarrow$ Migrate $\rightarrow$ Contract pattern so old code remains compatible).
2. Execute the corresponding `DOWN` migration script in the Supabase SQL Editor.
3. If necessary, restore the database from the automated daily point-in-time backup via **Supabase Dashboard > Settings > Database > Backups**.

---

## 🚨 Incident Communication & Post-Mortem

1. Notify the engineering team and on-call lead.
2. Log the rollback event in the internal incident tracker.
3. Conduct a post-mortem to analyze root causes, test gaps, and prevent recurrence.
