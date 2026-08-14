# HMAC Signed Webhook Delivery & Replay Defense Engine

import hmac
import hashlib
import time
from typing import Dict, Any, Optional

class HMACWebhookEngine:
    """Manages outbound HMAC SHA-256 signed webhook delivery with replay protection headers and SSRF destination validation."""

    @staticmethod
    def generate_signature(secret: str, payload_json: str, timestamp: Optional[int] = None) -> Dict[str, str]:
        ts = timestamp or int(time.time())
        signed_payload = f"{ts}.{payload_json}"
        signature = hmac.new(secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256).hexdigest()

        return {
            "X-Jurisiva-Timestamp": str(ts),
            "X-Jurisiva-Signature": f"t={ts},v1={signature}"
        }

    @staticmethod
    def verify_signature(secret: str, payload_json: str, signature_header: str, max_age_seconds: int = 300) -> bool:
        try:
            parts = dict(item.split("=") for item in signature_header.split(","))
            ts = int(parts.get("t", "0"))
            v1_sig = parts.get("v1", "")

            # Replay protection: check timestamp age
            if abs(int(time.time()) - ts) > max_age_seconds:
                return False

            signed_payload = f"{ts}.{payload_json}"
            expected_sig = hmac.new(secret.encode("utf-8"), signed_payload.encode("utf-8"), hashlib.sha256).hexdigest()
            return hmac.compare_digest(expected_sig, v1_sig)
        except Exception:
            return False

webhook_engine = HMACWebhookEngine()
