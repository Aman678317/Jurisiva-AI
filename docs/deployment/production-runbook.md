# Production Release & Operations Runbook

This runbook defines the standard operating procedure for deploying, verifying, and monitoring Jurisiva-AI releases.

---

## 🚀 Pre-Deployment Checklist

- [ ] All feature PRs merged into `main` branch.
- [ ] GitHub Actions CI workflow passed (`.github/workflows/ci.yml`).
- [ ] No hardcoded secrets or `.env` files committed.
- [ ] Database schema migrations tested on staging Supabase.

---

## 📦 Deployment Sequence

1. **Step 1: Apply Supabase Migrations**
   Execute new SQL migrations in `supabase/migrations/` against production Supabase.
   
2. **Step 2: Deploy Render Backend & Worker**
   Trigger deployment via Render Dashboard or GitHub webhook.
   Verify `GET https://api.jurisiva.ai/ready` returns `{"ready": true}`.

3. **Step 3: Deploy Vercel Frontend**
   Trigger production build in Vercel. Ensure `NEXT_PUBLIC_API_URL` points to `https://api.jurisiva.ai`.

4. **Step 4: Execute Production Smoke Tests**
   Run the automated smoke test script against production:
   ```bash
   python scripts/smoke-test.py --api-url https://api.jurisiva.ai
   ```

5. **Step 5: Verify Critical Workflows**
   - User login & session creation
   - Case initialization
   - Document upload & 300 DPI Indic OCR extraction
   - Ownership devolution recalculation
   - Apex legal research investigation
   - Diligence opinion report compilation
   - Spoken Voice Assistant turn

---

## 📊 Monitoring & Alerts

- **Render Metrics**: CPU, Memory, HTTP 5xx error rate, and active worker job queue depth.
- **Supabase Metrics**: Connection pool saturation, query latency, and storage bandwidth.
- **Vercel Analytics**: Edge response time, page load speed, and core web vitals.
