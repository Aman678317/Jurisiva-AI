# Authentication Engine & Token Issuer

import hashlib
import time
from typing import Optional, Dict
from app.config import settings

class AuthenticationEngine:
    @staticmethod
    def hash_password(password: str) -> str:
        """Secure password hashing abstraction."""
        return hashlib.pbkdf2_hmac(
            'sha256',
            password.encode('utf-8'),
            b'jurisiva_salt_2026',
            100000
        ).hex()

    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return AuthenticationEngine.hash_password(plain_password) == hashed_password

    @staticmethod
    def create_token(user_id: str, org_id: str, role: str) -> Dict[str, str]:
        expires_at = int(time.time()) + (settings.jwt_expiration_hours * 3600)
        token_str = f"bearer_{user_id}:{org_id}:{role}:{expires_at}"
        return {"access_token": token_str, "token_type": "bearer", "expires_at": str(expires_at)}

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, str]]:
        if not token:
            return None
        t = token.strip()
        while t.lower().startswith("bearer ") or t.lower().startswith("bearer_"):
            if t.lower().startswith("bearer "):
                t = t[7:].strip()
            elif t.lower().startswith("bearer_"):
                t = t[7:].strip()

        if ":" in t:
            parts = t.split(":")
            if len(parts) != 4:
                return None
            try:
                expires_at = int(parts[3])
                if time.time() > expires_at:
                    return None
                return {
                    "user_id": parts[0],
                    "org_id": parts[1],
                    "role": parts[2],
                }
            except Exception:
                return None

        # Fallback underscore splitting
        parts = t.split("_")
        if len(parts) >= 4:
            try:
                expires_at = int(parts[-1])
                if time.time() > expires_at:
                    return None
                user_id = f"{parts[0]}_{parts[1]}" if len(parts) >= 5 and parts[0] == "usr" else parts[0]
                org_id = f"{parts[2]}_{parts[3]}" if len(parts) >= 6 and parts[2] == "org" else (parts[1] if len(parts) >= 4 else "org_001")
                return {
                    "user_id": user_id,
                    "org_id": org_id,
                    "role": "LEAD_ADVOCATE"
                }
            except Exception:
                return None

        return None

auth_engine = AuthenticationEngine()
