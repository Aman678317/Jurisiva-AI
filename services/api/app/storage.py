# Secure Object Storage & Path Generator

import hashlib

class SecureStorageAdapter:
    @staticmethod
    def generate_storage_key(org_id: str, matter_id: str, doc_id: str, version_id: str, filename: str) -> str:
        """Generates server-side storage path preventing path traversal and client filename tampering."""
        safe_filename = hashlib.sha256(filename.encode('utf-8')).hexdigest()[:16]
        return f"tenants/{org_id}/matters/{matter_id}/documents/{doc_id}/versions/{version_id}/original/{safe_filename}.pdf"

    @staticmethod
    def validate_file_metadata(filename: str, byte_size: int, mime_type: str) -> tuple[bool, str]:
        """Validates file upload limits and safe document extensions."""
        max_size = 100 * 1024 * 1024 # 100MB
        if byte_size > max_size:
            return False, "FILE_TOO_LARGE: File size exceeds 100MB maximum limit."

        allowed_mime = {"application/pdf", "image/png", "image/jpeg", "image/tiff"}
        if mime_type not in allowed_mime:
            return False, "UNSUPPORTED_FORMAT: Only PDF, PNG, JPEG, and TIFF documents are allowed."

        return True, "VALID"

storage_adapter = SecureStorageAdapter()
