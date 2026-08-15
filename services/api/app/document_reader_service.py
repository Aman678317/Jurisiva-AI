# Page-by-Page Document Reader & Full Legal Paper Explanation Service
# Handles multi-page navigation, evidence highlighting, lawyer-style explanations, and image recovery

import time
from typing import Dict, List, Any, Optional
from app.multilingual_engine import multilingual_engine

class DocumentReaderService:
    """Manages page-by-page document rendering, evidence coordinates, and deep legal paper explanations."""

    def __init__(self):
        # In-memory document repository with multi-page support and scanned image artifacts
        self._document_pages = {
            "doc_sale_1985": {
                "document_id": "doc_sale_1985",
                "title": "Registered Sale Deed 1985",
                "instrument_type": "CONVEYANCE_DEED",
                "registration_number": "1234/1985-86",
                "registration_date": "14-11-1985",
                "sro_office": "Sub-Registrar Devanahalli, Book 1, Vol 120",
                "total_pages": 4,
                "pages": [
                    {
                        "page_number": 1,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "STAMP DUTY: Rs. 500/-. REGISTERED SALE DEED executed on 14th day of November, 1985 at Devanahalli.",
                        "kannada_text": "ದಿನಾಂಕ 14-11-1985 ರಂದು ದೇವನಹಳ್ಳಿ ಉಪನೋಂದಣಾಧಿಕಾರಿ ಕಚೇರಿಯಲ್ಲಿ ನೋಂದಾಯಿಸಲಾದ ಕ್ರಯಪತ್ರ.",
                        "confidence": 0.98,
                        "recovery_status": {"deskew_deg": 0.4, "contrast_enhanced": True, "stamps_detected": 2, "signatures_detected": 1}
                    },
                    {
                        "page_number": 2,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "VENDOR: Venkatappa, S/o Late Muniyappa. PURCHASER: Krishnappa, S/o Late Venkataramanappa. Consideration: Rs. 45,000/- received in full. SCHEDULE: Survey No. 42/1 Hissa 2 measuring 2 Acres 24 Guntas situated at Devanahalli Village.",
                        "kannada_text": "ಮಾರಾಟಗಾರ: ವೆಂಕಟಪ್ಪ ಬಿನ್ ಮುನಿಯಪ್ಪ. ಕೊಳ್ಳುವವರು: ಕೃಷ್ಣಪ್ಪ ಬಿನ್ ವೆಂಕಟರಮಣಪ್ಪ. ಕ್ರಯಧನ: ರೂ 45,000/-. ಸ್ವತ್ತು: ಸರ್ವೇ ನಂ 42/1 ಹಿಸ್ಸಾ 2, ವಿಸ್ತೀರ್ಣ 2 ಎಕರೆ 24 ಗುಂಟೆ.",
                        "confidence": 0.99,
                        "recovery_status": {"deskew_deg": 0.0, "contrast_enhanced": True, "stamps_detected": 1, "signatures_detected": 2}
                    },
                    {
                        "page_number": 3,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "BOUNDARIES: North by: Land of Muniyappa; South by: Gramathana Road; East by: Survey No. 42/2; West by: Survey No. 41. Absolute peaceable possession handed over on spot.",
                        "kannada_text": "ಚಕ್ಕುಬಂದಿ: ಉತ್ತರಕ್ಕೆ: ಮುನಿಯಪ್ಪನ ಜಮೀನು, ದಕ್ಷಿಣಕ್ಕೆ: ಗ್ರಾಮಠಾಣ ರಸ್ತೆ, ಪೂರ್ವಕ್ಕೆ: ಸರ್ವೇ ನಂ 42/2, ಪಶ್ಚಿಮಕ್ಕೆ: ಸರ್ವೇ ನಂ 41.",
                        "confidence": 0.96,
                        "recovery_status": {"deskew_deg": -0.2, "contrast_enhanced": True, "stamps_detected": 0, "signatures_detected": 2}
                    },
                    {
                        "page_number": 4,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "COVENANTS & INDEMNITY: The Vendor covenants that the property is free from all encumbrances, attachments, and claims of coparceners or minors. Signed by Venkatappa before Witnesses.",
                        "kannada_text": "ಹಕ್ಕು ಖಾತರಿ: ಸದರಿ ಸ್ವತ್ತಿನ ಮೇಲೆ ಯಾವುದೇ ರೀತಿಯ ಸಾಲ, ಜಪ್ತಿ ಅಥವಾ ಇತರರ ಹಕ್ಕು ಇರುವುದಿಲ್ಲವೆಂದು ಮಾರಾಟಗಾರರು ಖಾತರಿಪಡಿಸಿರುತ್ತಾರೆ.",
                        "confidence": 0.94,
                        "recovery_status": {"deskew_deg": 0.1, "contrast_enhanced": True, "stamps_detected": 1, "signatures_detected": 3}
                    }
                ]
            },
            "doc_sale_2018": {
                "document_id": "doc_sale_2018",
                "title": "Registered Sale Deed 2018",
                "instrument_type": "CONVEYANCE_DEED",
                "registration_number": "4567/2018-19",
                "registration_date": "18-10-2018",
                "sro_office": "Sub-Registrar Devanahalli, Book 1",
                "total_pages": 4,
                "pages": [
                    {
                        "page_number": 1,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "REGISTERED ABSOLUTE SALE DEED dated 18-10-2018. Consideration: Rs. 62,00,000/-.",
                        "kannada_text": "ದಿನಾಂಕ 18-10-2018 ರಂದು ನೋಂದಾಯಿಸಲಾದ ಶುದ್ಧ ಕ್ರಯಪತ್ರ. ಪ್ರತಿಫಲ: ರೂ 62,00,000/-.",
                        "confidence": 0.99,
                        "recovery_status": {"deskew_deg": 0.0, "contrast_enhanced": False, "stamps_detected": 2, "signatures_detected": 2}
                    },
                    {
                        "page_number": 2,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "PARTIES: Vendor: Krishnappa, S/o Late Venkataramanappa. Purchaser: Ramesh Kumar, S/o Krishnappa.",
                        "kannada_text": "ಮಾರಾಟಗಾರ: ಕೃಷ್ಣಪ್ಪ. ಕೊಳ್ಳುವವರು: ರಮೇಶ್ ಕುಮಾರ್.",
                        "confidence": 0.98,
                        "recovery_status": {"deskew_deg": 0.0, "contrast_enhanced": False, "stamps_detected": 1, "signatures_detected": 2}
                    },
                    {
                        "page_number": 3,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "SCHEDULE: Survey No. 42/1 Hissa 2 measuring 2 Acres 10 Guntas. [Note: 14 Guntas difference from root deed unrectified on spot].",
                        "kannada_text": "ಸ್ವತ್ತಿನ ವಿವರ: ಸರ್ವೇ ನಂ 42/1 ಹಿಸ್ಸಾ 2, ವಿಸ್ತೀರ್ಣ 2 ಎಕರೆ 10 ಗುಂಟೆ.",
                        "confidence": 0.88,
                        "recovery_status": {"deskew_deg": 0.3, "contrast_enhanced": True, "stamps_detected": 1, "signatures_detected": 2}
                    },
                    {
                        "page_number": 4,
                        "image_url": "/api/v1/media/petition.jpg",
                        "ocr_text": "REGISTRATION ENDORSEMENT: Registered as Document No. 4567/2018-19 in CD No. DNHD120, SRO Devanahalli.",
                        "kannada_text": "ನೋಂದಣಿ ದೃಢೀಕರಣ: ದಸ್ತಾವೇಜು ಸಂಖ್ಯೆ 4567/2018-19 ರಂತೆ ನೋಂದಾಯಿಸಲಾಗಿದೆ.",
                        "confidence": 0.99,
                        "recovery_status": {"deskew_deg": 0.0, "contrast_enhanced": False, "stamps_detected": 3, "signatures_detected": 2}
                    }
                ]
            }
        }

    def get_document_page(
        self,
        document_id: str,
        page_number: int,
        target_language: str = "en"
    ) -> Dict[str, Any]:
        """Returns specific page scan, original text, translated text, and recovery metrics."""
        doc = self._document_pages.get(document_id, self._document_pages["doc_sale_1985"])
        pages = doc.get("pages", [])
        page_idx = max(0, min(len(pages) - 1, page_number - 1))
        page = pages[page_idx]

        # Process translation and recovery alert
        processed = multilingual_engine.process_multilingual_page(
            original_text=page["ocr_text"],
            target_lang=target_language,
            page_num=page["page_number"],
            source_doc_id=document_id
        )

        return {
            "document_id": document_id,
            "document_title": doc["title"],
            "registration_number": doc.get("registration_number"),
            "registration_date": doc.get("registration_date"),
            "current_page": page["page_number"],
            "total_pages": doc["total_pages"],
            "image_url": page["image_url"],
            "original_ocr_text": page["ocr_text"],
            "kannada_script_text": page.get("kannada_text", ""),
            "translated_text": processed["translated_text"],
            "target_language": target_language,
            "ocr_confidence": page["confidence"],
            "recovery_metrics": page.get("recovery_status", {}),
            "verification_alert": processed["verification_alert"],
            "is_faded": processed["is_faded_or_handwritten"]
        }

    def explain_document(self, document_id: str) -> Dict[str, Any]:
        """Generates comprehensive, lawyer-style explanation of the entire document."""
        doc = self._document_pages.get(document_id, self._document_pages["doc_sale_1985"])

        if document_id == "doc_sale_1985":
            return {
                "document_id": document_id,
                "document_title": "Registered Sale Deed dated 14-11-1985",
                "lawyer_summary": "This is a primary Root Conveyance Deed under Section 54 of the Transfer of Property Act, 1882, establishing clean title devolution for 2 Acres 24 Guntas in Survey No. 42/1 Hissa 2.",
                "what_this_document_is": "A Registered Absolute Sale Deed executed before Sub-Registrar Devanahalli in Book 1, Volume 120, Document No. 1234/1985-86.",
                "parties_involved": {
                    "vendor": "Venkatappa, S/o Late Muniyappa (Absolute lawful owner)",
                    "purchaser": "Krishnappa, S/o Late Venkataramanappa",
                    "relationship": "Arm's length commercial conveyance"
                },
                "property_schedule": {
                    "survey_number": "42/1",
                    "hissa_number": "2",
                    "village": "Devanahalli Village, Kasaba Hobli",
                    "total_extent": "2 Acres 24 Guntas (104,544 Sq.Ft)",
                    "boundaries": "North: Muniyappa Land; South: Gramathana Road; East: Sy 42/2; West: Sy 41"
                },
                "key_dates_and_money": {
                    "execution_date": "14-11-1985",
                    "consideration_paid": "₹ 45,000/- (Full consideration acknowledged)",
                    "stamp_duty_paid": "₹ 500/- (Adequately stamped)"
                },
                "rights_and_transactions": "Conveys absolute, marketable freehold ownership with physical possession and covenants of title indemnity against future claimants.",
                "what_evidence_is_present": "Contains official SRO registration endorsement, volume folio number, 2 witness attestations, and vendor thumb impression.",
                "what_is_unclear_or_risk": "The 2018 subsequent conveyance conveys only 2 Acres 10 Guntas, leaving a 14 Guntas gap that requires revenue durasti reconciliation.",
                "missing_documents": [
                    "Form 11E Mojini Tatkal Phodi Survey Sketch",
                    "1984 Settlement Akarband Extract"
                ],
                "recommended_lawyer_action": "File application under Section 106 of Karnataka Land Revenue Act, 1964 for Tatkal Phodi survey to reconcile spot boundaries."
            }

        return {
            "document_id": document_id,
            "document_title": doc["title"],
            "lawyer_summary": "Registered conveyance deed conveying property rights subject to revenue boundary verification.",
            "what_this_document_is": f"Registered Deed No. {doc.get('registration_number', '4567/2018')}.",
            "parties_involved": {"vendor": "Krishnappa", "purchaser": "Ramesh Kumar"},
            "property_schedule": {"survey_number": "42/1", "hissa_number": "2", "total_extent": "2 Acres 10 Guntas"},
            "recommended_lawyer_action": "Verify SRO discharge for SBI mortgage."
        }

document_reader_service = DocumentReaderService()
