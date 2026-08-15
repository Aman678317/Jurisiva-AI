# Vercel Frontend Production Deployment Guide

This guide covers deploying the Jurisiva-AI client interface to Vercel with zero client secret exposure, custom domains, and edge routing.

---

## 1. Prerequisites

- Vercel account connected to GitHub repository `github.com/Aman678317/Jurisiva-AI`.
- Custom domain configured (`app.jurisiva.ai` and `www.jurisiva.ai`).

---

## 2. Vercel Project Settings

- **Framework Preset**: `Other` / Static HTML
- **Root Directory**: `.` (Repository root)
- **Output Directory**: `apps/web`
- **Build Command**: `None` (or `npm run build` if bundling)
- **Development Command**: `npm run dev`

---

## 3. Environment Variables (Browser-Safe Only)

Configure these in **Vercel Dashboard > Project > Settings > Environment Variables**:

| Variable Name | Production Value | Description |
| :--- | :--- | :--- |
| `NEXT_PUBLIC_API_URL` | `https://api.jurisiva.ai` | Base URL of the Render FastAPI backend |
| `NEXT_PUBLIC_SUPABASE_URL` | `https://<your-project>.supabase.co` | Supabase instance URL |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | `<your-public-anon-key>` | Browser-safe public anonymous key |

> [!CAUTION]
> **NEVER** add `SUPABASE_SERVICE_ROLE_KEY`, `OPENAI_API_KEY`, `ANTHROPIC_API_KEY`, or `DATABASE_URL` to Vercel environment variables. All secrets must remain exclusively on the Render backend.

---

## 4. Edge Routing & Security Headers (`vercel.json`)

Vercel reads the root `vercel.json` to enforce strict security headers:
- `X-Frame-Options: DENY` (prevents clickjacking)
- `X-Content-Type-Options: nosniff` (prevents MIME sniffing)
- `Content-Security-Policy` (locks script sources and API connections)
- `Permissions-Policy: microphone=(self)` (enables Voice Legal Assistant)

---

## 5. Deployment Verification

After deployment, test:
1. Load `https://app.jurisiva.ai` in browser.
2. Verify browser network tab sends API requests to `https://api.jurisiva.ai/api/v1/...`.
3. Verify Voice Assistant microphone permissions prompt.
