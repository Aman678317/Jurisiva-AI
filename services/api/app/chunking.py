# Structure-Aware Semantic Chunking Engine

import hashlib
from typing import List, Dict, Any

class StructureAwareChunker:
    """Chunks text while preserving page boundaries, headings, and legal clause structure."""

    @staticmethod
    def chunk_document(
        org_id: str,
        matter_id: str,
        doc_id: str,
        version_id: str,
        pages: List[Dict[str, Any]]
    ) -> List[Dict[str, Any]]:
        chunks = []
        chunk_idx = 0

        for page in pages:
            page_num = page.get("page_number", 1)
            raw_text = page.get("raw_ocr_text", "")
            
            # Split page text into structural sections/paragraphs
            paragraphs = [p.strip() for p in raw_text.split("\n\n") if p.strip()]
            
            for p_text in paragraphs:
                chunk_idx += 1
                # Stable Content Hash calculation for Idempotency
                content_hash = hashlib.sha256(
                    f"{version_id}_{page_num}_{chunk_idx}_{p_text}".encode('utf-8')
                ).hexdigest()

                chunks.append({
                    "id": f"chk_{doc_id}_{page_num}_{chunk_idx}",
                    "organization_id": org_id,
                    "matter_id": matter_id,
                    "document_id": doc_id,
                    "document_version_id": version_id,
                    "page_number": page_num,
                    "chunk_index": chunk_idx,
                    "text": p_text,
                    "normalized_text": p_text.replace("\r", "").strip(),
                    "content_hash": content_hash,
                    "token_count": len(p_text.split()),
                    "embedding_ref": f"emb_{content_hash[:16]}"
                })

        return chunks

chunker = StructureAwareChunker()
