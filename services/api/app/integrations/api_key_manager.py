# Scoped API Key Manager & Least-Privilege Scoping Engine

import time
import secrets
import hashlib
from typing import Dict, List, Any

class ScopedAPIKeyManager:
    """Issues and verifies hashed, rotatable, least-privilege API keys scoped by organization and matter."""

    def __init__(self):
        self._api_keys: Dict[str, Dict[str, Any]] = {}

    def issue_api_key(self, org_id: str, name: str, scopes: List[str]) -> Dict[str, Any]:
        raw_key = f"jur_live_{secrets.token_hex(16)}"
        key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()

        key_record = {
            "key_id": f"KEY-{secrets.token_hex(4)}",
            "key_hash": key_hash,
            "org_id": org_id,
            "name": name,
            "scopes": scopes,
            "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "status": "ACTIVE"
        }
        self._api_keys[key_hash] = key_record

        return {
            "raw_key": raw_key,
            "key_id": key_record["key_id"],
            "org_id": org_id,
            "scopes": scopes
        }

    def verify_api_key(self, raw_key: str, required_scope: str) -> Dict[str, Any]:
        key_hash = hashlib.sha256(raw_key.encode("utf-8")).hexdigest()
        key = self._api_keys.get(key_hash)

        if not key or key["status"] != "ACTIVE":
            return {"status": "UNAUTHORIZED", "reason": "Invalid or revoked API key."}

        if required_scope not in key["scopes"] and "admin:everything" not in key["scopes"]:
            return {"status": "FORBIDDEN", "reason": f"API key missing required scope '{required_scope}'."}

        return {"status": "AUTHORIZED", "org_id": key["org_id"], "key_id": key["key_id"]}

api_key_manager = ScopedAPIKeyManager()
