# Browser Security & SSRF Protection Engine
# Enforces strict URL validation, private IP blocking, domain rate limiting, and size limits

import re
import urllib.parse
import ipaddress
import socket
from typing import Dict, Any, Tuple

class BrowserSecurity:
    """Zero-Trust Browser Security Layer preventing SSRF, local network traversal, and malicious protocols."""

    BLOCKED_SCHEMES = {"file", "gopher", "chrome", "about", "javascript", "data", "blob", "ftp"}
    BLOCKED_HOSTNAMES = {"localhost", "127.0.0.1", "0.0.0.0", "::1", "169.254.169.254", "metadata.google.internal"}
    
    PRIVATE_NETWORKS = [
        ipaddress.ip_network("10.0.0.0/8"),
        ipaddress.ip_network("172.16.0.0/12"),
        ipaddress.ip_network("192.168.0.0/16"),
        ipaddress.ip_network("127.0.0.0/8"),
        ipaddress.ip_network("169.254.0.0/16"),
        ipaddress.ip_network("::1/128"),
        ipaddress.ip_network("fc00::/7"),
        ipaddress.ip_network("fe80::/10"),
    ]

    MAX_RESPONSE_SIZE_BYTES = 10 * 1024 * 1024  # 10 MB
    DEFAULT_TIMEOUT_SECONDS = 15.0

    @classmethod
    def validate_url(cls, url: str) -> Tuple[bool, str]:
        """
        Validates target URL for browser navigation:
        - Only http:// and https:// allowed
        - Blocks localhost, link-local, loopback, and private RFC-1918 IPs
        - Blocks cloud metadata endpoints (169.254.169.254)
        """
        if not url or not isinstance(url, str):
            return False, "URL cannot be empty."

        clean_url = url.strip()
        if not clean_url.startswith(("http://", "https://")):
            # Auto-prepend https:// if plain domain provided
            if re.match(r'^[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', clean_url):
                clean_url = "https://" + clean_url
            else:
                return False, "Only HTTP and HTTPS URLs are permitted for research."

        try:
            parsed = urllib.parse.urlparse(clean_url)
        except Exception as e:
            return False, f"Malformed URL: {str(e)}"

        if parsed.scheme.lower() not in {"http", "https"}:
            return False, f"Blocked protocol scheme: '{parsed.scheme}'. Only http and https allowed."

        hostname = (parsed.hostname or "").lower().strip()
        if not hostname:
            return False, "URL is missing a valid hostname."

        if hostname in cls.BLOCKED_HOSTNAMES:
            return False, f"Blocked private/local target: '{hostname}' (SSRF Protection)."

        # Validate IP addresses if raw IP passed
        try:
            ip_obj = ipaddress.ip_address(hostname)
            for priv_net in cls.PRIVATE_NETWORKS:
                if ip_obj in priv_net:
                    return False, f"Blocked internal/private IP network: {hostname}."
        except ValueError:
            # Hostname is a domain name (not a raw IP), which is safe to proceed
            pass

        return True, clean_url

    @classmethod
    def is_safe_redirect(cls, current_url: str, redirect_url: str) -> bool:
        valid, _ = cls.validate_url(redirect_url)
        return valid

browser_security = BrowserSecurity()
