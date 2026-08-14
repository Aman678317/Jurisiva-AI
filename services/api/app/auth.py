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
        # Mock token payload encoding
        token_str = f"bearer_{user_id}_{org_id}_{role}_{expires_at}"
        return {"access_token": token_str, "token_type": "bearer", "expires_at": str(expires_at)}

    @staticmethod
    def verify_token(token: str) -> Optional[Dict[str, str]]:
        if not token or not token.startswith("bearer_"):
            return None
        parts = token.split("_")
        if len(parts) < 5:
            return None
        expires_at = int(parts[4])
        if time.time() > expires_at:
            return None  # Token Expired
        return {
            "user_id": parts[1],
            "org_id": parts[2],
            "role": parts[3],
        }

auth_engine = AuthenticationEngine()
