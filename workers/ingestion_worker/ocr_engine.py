# Indic Multilingual OCR Engine Abstraction & Quality Evaluation

from typing import Dict, List, Any

class OCRPageResult:
    def __init__(
        self,
        raw_text: str,
        normalized_text: str,
        detected_languages: List[str],
        quality_score: float,
        layout_blocks: List[Dict[str, Any]],
        words: List[Dict[str, Any]]
    ):
        self.raw_text = raw_text
        self.normalized_text = normalized_text
        self.detected_languages = detected_languages
        self.quality_score = quality_score
        self.layout_blocks = layout_blocks
        self.words = words

class OCRGateway:
    """Replaceable OCR Provider Gateway supporting English & Indic Scripts (Devanagari/Hindi/Marathi)."""

    def __init__(self, provider_name: str = "TesseractIndicLocal"):
        self.provider_name = provider_name
        self.supported_scripts = {"latin", "devanagari", "kannada", "tamil", "telugu"}

    def supports_language(self, script: str) -> bool:
        return script.lower() in self.supported_scripts

    def process_page_image(self, page_number: int, is_scanned: bool = True) -> OCRPageResult:
        """Processes scanned page image, extracts text, bounding boxes, and quality signals."""
        
        # Synthetic Indic Legal Scan Content (English + Devanagari)
        raw_text = (
            "REGISTERED NO: 1234/1985\n"
            "THIS DEED OF ABSOLUTE SALE executed on 14-08-1985.\n"
            "विक्रेता: श्री व्यंकप्पा (Venkatappa S/o Ramaiah)\n"
            "क्रेता: श्री कृष्णप्पा (Krishnappa S/o Govindappa)\n"
            "SCHEDULE PROPERTY: Survey No. 42/1 Hissa 2, Extent: 2 Acres 24 Guntas (104,544 Sq.Ft), Devanahalli."
        )

        # Conservative Text Normalization (Preserving raw legal identifiers intact)
        normalized_text = raw_text.replace("\r", "").strip()

        # Layout Block Segmentation
        layout_blocks = [
            {
                "id": f"blk_hdr_{page_number}",
                "block_type": "header",
                "bbox": {"xmin": 50, "ymin": 20, "xmax": 500, "ymax": 50},
                "text": "REGISTERED NO: 1234/1985"
            },
            {
                "id": f"blk_body_{page_number}",
                "block_type": "paragraph",
                "bbox": {"xmin": 50, "ymin": 60, "xmax": 550, "ymax": 300},
                "text": normalized_text
            },
            {
                "id": f"blk_stamp_{page_number}",
                "block_type": "stamp_region",
                "bbox": {"xmin": 400, "ymin": 10, "xmax": 580, "ymax": 90},
                "text": "SUB-REGISTRAR SEAL DEVANAHALLI"
            }
        ]

        # Detailed Word Bounding Boxes
        words = [
            {"text": "Survey", "bbox": {"xmin": 50, "ymin": 200, "xmax": 100, "ymax": 220}, "confidence": 0.98},
            {"text": "No.", "bbox": {"xmin": 105, "ymin": 200, "xmax": 130, "ymax": 220}, "confidence": 0.99},
            {"text": "42/1", "bbox": {"xmin": 135, "ymin": 200, "xmax": 180, "ymax": 220}, "confidence": 0.99},
            {"text": "Devanahalli", "bbox": {"xmin": 190, "ymin": 200, "xmax": 270, "ymax": 220}, "confidence": 0.95}
        ]

        # Quality Evaluation Signals
        quality_score = 0.965  # 96.5% OCR Accuracy
        detected_languages = ["en", "mr", "hi"]

        return OCRPageResult(
            raw_text=raw_text,
            normalized_text=normalized_text,
            detected_languages=detected_languages,
            quality_score=quality_score,
            layout_blocks=layout_blocks,
            words=words
        )

ocr_gateway = OCRGateway()
