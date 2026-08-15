# Structured Page Reader & Content Extraction Engine
# Parses HTML/DOM into structured headings, paragraphs, tables, links, PDFs, and legal entities

import re
import html
from typing import Dict, List, Any, Optional

class PageReader:
    """Extracts structured text, headings, tables, links, downloadable PDFs, and citations from web content."""

    @classmethod
    def parse_html_content(cls, html_raw: str, page_url: str) -> Dict[str, Any]:
        """Parses raw HTML into structured readable representation."""
        if not html_raw:
            return cls._empty_page_structure(page_url)

        # 1. Extract Page Title
        title_match = re.search(r'<title[^>]*>(.*?)</title>', html_raw, re.IGNORECASE | re.DOTALL)
        title = html.unescape(title_match.group(1).strip()) if title_match else "Untitled Web Page"

        # 2. Extract Headings (H1 - H3)
        headings = []
        for h_match in re.finditer(r'<h([1-3])[^>]*>(.*?)</h\1>', html_raw, re.IGNORECASE | re.DOTALL):
            h_level = f"H{h_match.group(1)}"
            h_text = re.sub(r'<[^>]+>', '', h_match.group(2)).strip()
            if h_text:
                headings.append({"level": h_level, "text": html.unescape(h_text)})

        # 3. Extract Main Paragraphs
        paragraphs = []
        for p_match in re.finditer(r'<p[^>]*>(.*?)</p>', html_raw, re.IGNORECASE | re.DOTALL):
            p_text = re.sub(r'<[^>]+>', '', p_match.group(1)).strip()
            if len(p_text) > 20:
                paragraphs.append(html.unescape(p_text))

        # 4. Extract Outbound Links and PDFs
        links = []
        pdf_documents = []
        for a_match in re.finditer(r'<a\s+(?:[^>]*?\s+)?href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', html_raw, re.IGNORECASE | re.DOTALL):
            href = a_match.group(1).strip()
            anchor_text = re.sub(r'<[^>]+>', '', a_match.group(2)).strip()
            
            if href.lower().endswith(".pdf") or "pdf" in href.lower():
                pdf_documents.append({"url": href, "title": anchor_text or "Downloadable Legal PDF"})
            elif href.startswith(("http://", "https://", "/")):
                links.append({"url": href, "text": anchor_text or href})

        # 5. Extract Tables
        tables = []
        for tbl_match in re.finditer(r'<table[^>]*>(.*?)</table>', html_raw, re.IGNORECASE | re.DOTALL):
            rows = []
            for tr_match in re.finditer(r'<tr[^>]*>(.*?)</tr>', tbl_match.group(1), re.IGNORECASE | re.DOTALL):
                cells = [re.sub(r'<[^>]+>', '', cell).strip() for cell in re.findall(r'<t[dh][^>]*>(.*?)</t[dh]>', tr_match.group(1), re.IGNORECASE | re.DOTALL)]
                if cells:
                    rows.append(cells)
            if rows:
                tables.append({"row_count": len(rows), "data": rows[:10]})

        # 6. Extract Legal Citations & Survey Numbers
        full_text = " ".join(paragraphs)
        citations_found = re.findall(r'\b(?:20\d{2}\s+(?:INSC|SCC|KCCR|ILR)\s+\d+|\d+\s+SCC\s+\d+)\b', full_text, re.IGNORECASE)
        surveys_found = re.findall(r'\b(?:Sy\.?\s*No\.?\s*\d+/\d+|Survey\s+No\.?\s*\d+/\d+)\b', full_text, re.IGNORECASE)

        # 7. Language Detection (Indic & English)
        lang = "en"
        if re.search(r'[\u0C80-\u0CFF]', html_raw):
            lang = "kn"  # Kannada
        elif re.search(r'[\u0900-\u097F]', html_raw):
            lang = "hi"  # Hindi
        elif re.search(r'[\u0B80-\u0BFF]', html_raw):
            lang = "ta"  # Tamil

        return {
            "page_url": page_url,
            "title": title,
            "language": lang,
            "headings": headings[:15],
            "paragraphs": paragraphs[:25],
            "text_summary": "\n\n".join(paragraphs[:8]),
            "tables": tables[:5],
            "links": links[:30],
            "pdf_documents": pdf_documents[:10],
            "extracted_citations": list(set(citations_found)),
            "extracted_surveys": list(set(surveys_found)),
            "total_words": sum(len(p.split()) for p in paragraphs)
        }

    @classmethod
    def _empty_page_structure(cls, page_url: str) -> Dict[str, Any]:
        return {
            "page_url": page_url,
            "title": "Page Content Unavailable",
            "language": "en",
            "headings": [],
            "paragraphs": ["No readable text extracted from target source."],
            "text_summary": "Empty page",
            "tables": [],
            "links": [],
            "pdf_documents": [],
            "extracted_citations": [],
            "extracted_surveys": [],
            "total_words": 0
        }

page_reader = PageReader()
