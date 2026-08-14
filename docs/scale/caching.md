# Tenant-Safe Caching Strategy & Invalidation Rules

## Cache Key Isolation Principle
Every cached entry in Redis MUST contain `org_id` and `user_id` scope in its key prefix:

```text
cache_key = "cache:v1:org_{org_id}:matter_{matter_id}:doc_{doc_id}"
```

Caching private customer document text or derived AI findings without `org_id` scope is strictly forbidden.
