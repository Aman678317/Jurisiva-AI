# Automated Test Suite for Multilingual Property Document Reader & Voice Legal Assistant
# Tests Indic Language Engine, Page-by-Page Viewer, Deep Document Explanation, and Voice Tool Calling

import pytest
import os
import sys

api_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if api_dir not in sys.path:
    sys.path.insert(0, api_dir)

from app.multilingual_engine import multilingual_engine
from app.document_reader_service import document_reader_service
from app.voice_agent_service import jurisiva_voice_assistant, SpeechToTextProvider, TextToSpeechProvider
from app.provider_settings_service import provider_settings_service

# 1. Multilingual Indic Engine Tests
def test_multilingual_language_detection():
    # Kannada
    kn_text = "ದಿನಾಂಕ 14-11-1985 ರಂದು ನೋಂದಾಯಿಸಲಾದ ಕ್ರಯಪತ್ರ. ಸರ್ವೇ ನಂ 42/1 ಹಿಸ್ಸಾ 2."
    assert multilingual_engine.detect_language(kn_text) == "kn"

    # Hindi
    hi_text = "दिनांक 14-11-1985 को निष्पादित पंजीकृत विक्रय पत्र। खसरा क्रमांक 42/1."
    assert multilingual_engine.detect_language(hi_text) == "hi"

    # English
    en_text = "Registered Absolute Sale Deed executed on 14-11-1985 in Devanahalli SRO."
    assert multilingual_engine.detect_language(en_text) == "en"

def test_multilingual_translation_and_confidence():
    kn_text = "ಕ್ರಯಪತ್ರ ಸರ್ವೆ ನಂಬರ್ 42/1 ಹಿಸ್ಸಾ 2, ವಿಸ್ತೀರ್ಣ 2 ಎಕರೆ 24 ಗುಂಟೆ."
    res = multilingual_engine.process_multilingual_page(kn_text, target_lang="en", page_num=2, source_doc_id="doc_sale_1985")
    assert res["original_language"] == "kn"
    assert "Registered Sale Deed" in res["translated_text"]
    assert "Survey Number" in res["translated_text"]
    assert res["ocr_confidence"] >= 0.95

    # Faded Text Alert Test
    faded_text = "Vendor name: Venkat... [faded] ... [unclear] S/o Muniyappa."
    res_faded = multilingual_engine.process_multilingual_page(faded_text, target_lang="en")
    assert res_faded["is_faded_or_handwritten"] is True
    assert "Text may be unclear" in res_faded["verification_alert"]

# 2. Page-by-Page Document Reader & Multi-Page Tests
def test_document_reader_page_navigation():
    # Page 1
    p1 = document_reader_service.get_document_page("doc_sale_1985", page_number=1, target_language="en")
    assert p1["current_page"] == 1
    assert p1["total_pages"] == 4
    assert "STAMP DUTY" in p1["original_ocr_text"]

    # Page 2 (Schedule & Consideration)
    p2 = document_reader_service.get_document_page("doc_sale_1985", page_number=2, target_language="en")
    assert p2["current_page"] == 2
    assert "2 Acres 24 Guntas" in p2["original_ocr_text"]
    assert p2["recovery_metrics"]["stamps_detected"] >= 1

    # Page 4 (Covenants & Title Indemnity)
    p4 = document_reader_service.get_document_page("doc_sale_1985", page_number=4, target_language="en")
    assert p4["current_page"] == 4
    assert "COVENANTS & INDEMNITY" in p4["original_ocr_text"]

# 3. Deep Document Explanation (Lawyer Breakdown) Tests
def test_explain_document_lawyer_breakdown():
    exp = document_reader_service.explain_document("doc_sale_1985")
    assert exp["document_id"] == "doc_sale_1985"
    assert "Section 54 of the Transfer of Property Act" in exp["lawyer_summary"]
    assert "Venkatappa" in exp["parties_involved"]["vendor"]
    assert "Krishnappa" in exp["parties_involved"]["purchaser"]
    assert exp["property_schedule"]["survey_number"] == "42/1"
    assert exp["property_schedule"]["total_extent"] == "2 Acres 24 Guntas (104,544 Sq.Ft)"
    assert "14 Guntas deficit" in exp["what_is_unclear_or_risk"]
    assert len(exp["missing_documents"]) >= 2

# 4. Speech Providers & Multilingual Voice Synthesis Tests
def test_speech_providers():
    stt = SpeechToTextProvider()
    transcription = stt.transcribe("Who was the previous owner?", "en-IN")
    assert "previous owner" in transcription

    tts = TextToSpeechProvider()
    synth_kn = tts.synthesize_speech("ನಮಸ್ಕಾರ, ಇದು ಕ್ರಯಪತ್ರವಾಗಿದೆ.", language_code="kn")
    assert synth_kn["language_code"] == "kn"
    assert synth_kn["voice_profile"]["voice_id"].startswith("kn-IN")

# 5. Jurisiva Voice Legal Assistant Turn & Shared Memory Tests
def test_voice_assistant_interaction_cycle():
    # Turn 1: Who was previous owner?
    turn1 = jurisiva_voice_assistant.process_voice_turn(
        user_spoken_text="Who was the previous owner?",
        case_id="mat_001",
        session_id="voice_test_001",
        language="en"
    )
    assert "Venkatappa" in turn1["spoken_text"]
    assert turn1["action"] == "SHOW_OWNER"
    assert turn1["navigation"]["page_number"] == 2

    # Turn 2: Which page says this? (Tests auto-jump to Page 4)
    turn2 = jurisiva_voice_assistant.process_voice_turn(
        user_spoken_text="Which page says this?",
        case_id="mat_001",
        session_id="voice_test_001",
        language="en"
    )
    assert "Page 4" in turn2["spoken_text"]
    assert turn2["action"] == "JUMP_PAGE"
    assert turn2["navigation"]["page_number"] == 4

    # Turn 3: Kannada Speech Query
    turn_kn = jurisiva_voice_assistant.process_voice_turn(
        user_spoken_text="ಕನ್ನಡದಲ್ಲಿ ವಿವರಿಸಿ",
        case_id="mat_001",
        session_id="voice_test_001",
        language="kn"
    )
    assert turn_kn["language"] == "kn"
    assert "ವೆಂಕಟಪ್ಪ" in turn_kn["spoken_text"]

    # Verify Shared Memory
    history = jurisiva_voice_assistant.get_conversation_history("voice_test_001")
    assert len(history) >= 6

# 6. Provider Settings Ledger Tests
def test_provider_settings_security():
    statuses = provider_settings_service.get_provider_statuses()
    assert statuses["all_healthy"] is True
    assert len(statuses["providers"]) >= 4

    # Verify Zero API Key Exposure
    raw_str = str(statuses)
    assert "sk-" not in raw_str
    assert "api_key" not in raw_str
    assert "secret" not in raw_str
