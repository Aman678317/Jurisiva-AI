# Custom Domains & DNS Architecture

This document describes the public DNS configuration, SSL/TLS certificates, and domain routing for Jurisiva-AI.

---

## 🌐 Production Domain Topology

| Hostname | Target Service | Provider | SSL Termination |
| :--- | :--- | :--- | :--- |
| `www.jurisiva.ai` | Marketing Landing & Trust Center | Vercel | Vercel Edge Let's Encrypt |
| `app.jurisiva.ai` | Authenticated Workspace Application | Vercel | Vercel Edge Let's Encrypt |
| `api.jurisiva.ai` | FastAPI REST Gateway | Render | Render Cloudflare TLS |

---

## 📡 DNS Records Configuration

Add the following DNS records to your domain registrar (e.g. Cloudflare / AWS Route53):

```text
# Vercel Frontend App
CNAME   app.jurisiva.ai    cname.vercel-dns.com.
CNAME   www.jurisiva.ai    cname.vercel-dns.com.
A       jurisiva.ai        76.76.21.21

# Render FastAPI Gateway
CNAME   api.jurisiva.ai    jurisiva-api.onrender.com.
```

---

## 🔒 CORS & TLS Rules

- **Allowed Origins**: `https://app.jurisiva.ai`, `https://www.jurisiva.ai`, `https://jurisiva-ai.vercel.app`
- **TLS Version**: Minimum TLS 1.3 enforced.
- **HSTS**: `Strict-Transport-Security: max-age=63072000; includeSubDomains; preload`
