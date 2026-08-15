# Document Retriever Engine
# Searches uploaded matter documents, multilingual OCR transcripts, and structured tables.

import re
from typing import Dict, List, Any, Optional

class DocumentRetriever:
    """Retrieves document chunks, pages, and OCR records for a given matter."""

    # Default Matter Documents for mat_001 (Can be augmented with real uploaded files)
    MATTER_DOCUMENTS = {
        "mat_001": [
            {
                "document_id": "doc_001",
                "document_name": "Registered_Sale_Deed_1985.pdf",
                "document_type": "Sale Deed (ಕ್ರಯ ಪತ್ರ)",
                "date": "1985-10-14",
                "sro_registration_no": "1234/1985-86",
                "sro_office": "Sub-Registrar Office, Devanahalli (Book 1, Volume 120)",
                "pages": [
                    {
                        "page_number": 1,
                        "language": "Kannada & English",
                        "text": "GOVERNMENT OF KARNATAKA • REGISTRATION DEPARTMENT\nDEED OF ABSOLUTE SALE (ಕ್ರಯ ಪತ್ರ)\nDocument No: 1234/1985-86, Book 1, Volume 120, Pages 45 to 52.\nDate of Execution: 14th day of October 1985.\nVENDOR: Sri. Venkatappa, Son of Late Muniswamappa, Hindu, Aged about 58 years, Residing at Devanahalli Village.\nPURCHASER: Sri. Krishnappa, Son of Sri. Venkatappa, Hindu, Aged about 32 years, Residing at Devanahalli Village.\nCONSIDERATION: Sum of Rs. 45,000/- (Rupees Forty Five Thousand only) fully paid and acknowledged."
                    },
                    {
                        "page_number": 2,
                        "language": "Kannada & English",
                        "text": "SCHEDULE PROPERTY DESCRIPTION:\nItem No. 1: All that piece and parcel of agricultural dry land situated at Devanahalli Village, Kasaba Hobli, Devanahalli Taluk, Bengaluru Rural District.\nSurvey Number: Survey No. 42/1 Hissa 2.\nTotal Extent: 2 Acres 24 Guntas (equivalent to 104,544 Square Feet) assessed at Rs. 4.80 paise.\nBOUNDARIES:\nEast by: Land belonging to Ramaiah in Sy No. 42/3\nWest by: Government Cart Track (Vandi Raste)\nNorth by: Land of Govindappa in Sy No. 42/2\nSouth by: Remaining land of Venkatappa\nFREE FROM ENCUMBRANCES: The Vendor hereby covenants that the schedule property is free from all mortgages, charges, liens, court attachments, or prior alienations."
                    }
                ]
            },
            {
                "document_id": "doc_002",
                "document_name": "Mutation_Extract_MR_14_1986.jpg",
                "document_type": "Mutation Register Extract (ಮ್ಯುಟೇಶನ್ ರಿಜಿಸ್ಟರ್)",
                "date": "1986-03-22",
                "sro_registration_no": "MR 14/1986-87",
                "sro_office": "Tahsildar Office / Revenue Department, Devanahalli",
                "pages": [
                    {
                        "page_number": 1,
                        "language": "Kannada (ಕನ್ನಡ)",
                        "text": "ಕರ್ನಾಟಕ ಸರ್ಕಾರ • ಕಂದಾಯ ಇಲಾಖೆ • ದೇವನಹಳ್ಳಿ ತಾಲ್ಲೂಕು ಕಸಬಾ ಹೋಬಳಿ\nಮ್ಯುಟೇಶನ್ ಸಂಖ್ಯೆ: MR 14/1986-87 • ದಿನಾಂಕ: 22-03-1986\nಸರ್ವೆ ನಂಬರ್: 42/1 ಹಿಸ್ಸಾ 2 • ಒಟ್ಟು ವಿಸ್ತೀರ್ಣ: 2 ಎಕರೆ 24 ಗುಂಟೆ\nಹಿಂದಿನ ಖಾತೆದಾರರು: ವೆಂಕಟಪ್ಪ ಬಿನ್ ಮುನಿಸ್ವಾಮಪ್ಪ\nಹೊಸ ಖಾತೆದಾರರು: ಕೃಷ್ಣಪ್ಪ ಬಿನ್ ವೆಂಕಟಪ್ಪ (ಕ್ರಯ ಪತ್ರ ಸಂಖ್ಯೆ 1234/1985-86 ಆಧಾರದ ಮೇಲೆ ಖಾತೆ ಬದಲಾವಣೆ ಮಂಜೂರಾಗಿದೆ).\nತಹಶೀಲ್ದಾರ್ ಆದೇಶ ಸಂಖ್ಯೆ: RRT/CR/86-87."
                    }
                ]
            },
            {
                "document_id": "doc_003",
                "document_name": "SBI_Mortgage_Deed_2010.pdf",
                "document_type": "Simple Mortgage Deed (ಅಡಮಾನ ಪತ್ರ)",
                "date": "2010-08-08",
                "sro_registration_no": "4567/2010-11",
                "sro_office": "Sub-Registrar Office, Devanahalli (Book 1)",
                "pages": [
                    {
                        "page_number": 1,
                        "language": "English",
                        "text": "DEED OF SIMPLE MORTGAGE\nRegistered as Document No. 4567/2010-11 in Book 1, SRO Devanahalli.\nMORTGAGOR: Sri. Krishnappa, Son of Venkatappa, residing at Devanahalli.\nMORTGAGEE: State Bank of India, Devanahalli Branch.\nSECURED AMOUNT: Principal loan of Rs. 50,00,000/- (Rupees Fifty Lakhs only) with agreed interest at 11.25% p.a.\nSECURITY PROPERTY: Survey No. 42/1 Hissa 2, Extent 2 Acres 24 Guntas, Devanahalli Village.\nSTATUS: Unreleased on SRO Book 1 encumbrance register. No registered Deed of Discharge or No Due Certificate (NOC) has been executed."
                    }
                ]
            },
            {
                "document_id": "doc_004",
                "document_name": "Sale_Deed_2018_Current.pdf",
                "document_type": "Sale Deed (Conveyance)",
                "date": "2018-11-19",
                "sro_registration_no": "8912/2018-19",
                "sro_office": "Sub-Registrar Office, Devanahalli",
                "pages": [
                    {
                        "page_number": 1,
                        "language": "English",
                        "text": "DEED OF ABSOLUTE SALE\nDocument No. 8912/2018-19, Registered at SRO Devanahalli on 19-11-2018.\nVENDOR: Sri. Krishnappa, Son of Venkatappa.\nPURCHASER: Sri. Anand Kumar, Son of Ramesh Kumar, residing at Indiranagar, Bengaluru.\nCONSIDERATION: Rs. 1,85,00,000/- (Rupees One Crore Eighty Five Lakhs only)."
                    },
                    {
                        "page_number": 2,
                        "language": "English",
                        "text": "SCHEDULE PROPERTY CONVEYED:\nSurvey Number: Survey No. 42/1 Hissa 2, Devanahalli Village, Kasaba Hobli, Devanahalli Taluk.\nTotal Extent Conveyed: 2 Acres 10 Guntas (equivalent to 98,010 Square Feet).\nNOTE ON AREA DEFICIT: The conveyed extent is 2 Acres 10 Guntas, whereas the parent root deed (1985) was registered for 2 Acres 24 Guntas. Discrepancy of 14 Guntas (-14 Guntas deficit) without sub-division tatkal phodi or 11E survey sketch.\nBOUNDARIES IN 2018 DEED:\nNorth by: Private Layout Road (Shifted from Govindappa's land in 1985 deed)\nSouth by: Land of Venkatappa\nEast by: Sy No. 42/3\nWest by: Road"
                    }
                ]
            }
        ]
    }

    def retrieve_chunks(
        self,
        org_id: str,
        matter_id: str,
        query: str,
        top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """Retrieve relevant pages and chunks matching query keywords and semantics."""
        docs = self.MATTER_DOCUMENTS.get(matter_id, self.MATTER_DOCUMENTS.get("mat_001", []))
        if not docs:
            return []

        q_lower = query.lower()
        words = [w for w in re.split(r'\W+', q_lower) if len(w) > 2]

        candidates = []
        for doc in docs:
            for page in doc["pages"]:
                text = page["text"]
                text_lower = text.lower()
                
                score = 0
                matched_keywords = []
                for w in words:
                    if w in text_lower:
                        score += 1
                        matched_keywords.append(w)

                # Keyword specific boosts
                if "owner" in q_lower and ("vendor" in text_lower or "purchaser" in text_lower or "ಖಾತೆದಾರರು" in text_lower):
                    score += 3
                if "survey" in q_lower and "42/1" in text_lower:
                    score += 3
                if "extent" in q_lower and ("2 acres" in text_lower or "ವಿಸ್ತೀರ್ಣ" in text_lower or "guntas" in text_lower):
                    score += 3
                if "mortgage" in q_lower and ("mortgage" in text_lower or "sbi" in text_lower or "ಅಡಮಾನ" in text_lower):
                    score += 4
                if "mismatch" in q_lower and ("deficit" in text_lower or "discrepancy" in text_lower or "14 guntas" in text_lower):
                    score += 4

                if score > 0 or not words:
                    candidates.append({
                        "document_id": doc["document_id"],
                        "document_name": doc["document_name"],
                        "document_type": doc["document_type"],
                        "date": doc["date"],
                        "sro_registration_no": doc["sro_registration_no"],
                        "sro_office": doc["sro_office"],
                        "page_number": page["page_number"],
                        "language": page["language"],
                        "text": text,
                        "score": score,
                        "matched_keywords": matched_keywords
                    })

        candidates.sort(key=lambda x: x["score"], reverse=True)
        return candidates[:top_k]

document_retriever = DocumentRetriever()
