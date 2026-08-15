# Automated Test Suite for Multi-LLM Router, Key Rotation, and Failover Mesh
# Verifies NVIDIA, DeepSeek, GLM, KeyPool, ModelRouter, and Seamless Failover

import pytest
import time
from app.models.llm_provider import KeyPool, NvidiaProvider, DeepSeekProvider, GLMProvider, OpenAIProvider
from app.models.model_router import model_router, ModelRouter
from app.provider_settings_service import provider_settings_service

def test_key_pool_rotation_and_cooldown():
    pool = KeyPool("test_provider", "TEST_KEY", "TEST_KEYS")
    pool.keys = ["key_alpha", "key_beta", "key_gamma"]

    # Initial key
    k1 = pool.get_active_key()
    assert k1 == "key_alpha"

    # Simulate rate-limit (429) on key_alpha
    pool.mark_rate_limited("key_alpha", cooldown_seconds=10)

    # Must rotate to key_beta
    k2 = pool.get_active_key()
    assert k2 == "key_beta"

    # Simulate rate-limit on key_beta
    pool.mark_rate_limited("key_beta", cooldown_seconds=10)

    # Must rotate to key_gamma
    k3 = pool.get_active_key()
    assert k3 == "key_gamma"

def test_nvidia_nim_provider():
    nv = NvidiaProvider()
    res = nv.generate(
        prompt="Analyze survey number boundary clause",
        system_policy="Strict Statutory Legal Analysis",
        model="nvidia/llama-3.1-nemotron-70b-instruct"
    )
    assert res["provider"] == "nvidia"
    assert "nemotron" in res["model"]
    assert "content" in res
    assert res["usage"]["total_tokens"] > 0

    struct = nv.structured_output("Deed text", {}, "Policy", "nvidia/llama-3.1-nemotron-70b-instruct")
    assert struct["data"]["deficit_detected"] is True

def test_deepseek_r1_reasoner_provider():
    ds = DeepSeekProvider()
    res = ds.generate(
        prompt="Evaluate 14 guntas discrepancy under Section 106 KLR Act",
        system_policy="Title Diligence",
        model="deepseek-reasoner"
    )
    assert res["provider"] == "deepseek"
    assert res["model"] == "deepseek-reasoner"
    assert res["reasoning_content"] is not None
    assert "Akarband" in res["reasoning_content"] or "1985" in res["reasoning_content"]
    assert "content" in res

def test_glm_and_glm2_provider():
    glm = GLMProvider()
    
    # Test GLM-4
    res_4 = glm.generate("Extract party names", "Legal Entity Policy", model="glm-4")
    assert res_4["provider"] == "glm"
    assert res_4["model"] == "glm-4"
    assert "content" in res_4

    # Test GLM-2
    res_2 = glm.generate("Fast classification", "Policy", model="glm-2")
    assert res_2["provider"] == "glm"
    assert res_2["model"] == "glm-2"

def test_model_router_intelligent_routing():
    # 1. Deep Legal Reasoning should route to DeepSeek R1 or NVIDIA
    deep_route = model_router.route_task("COMPLEX_LEGAL_ANALYSIS")
    assert deep_route["provider_name"] == "deepseek"
    assert deep_route["model"] == "deepseek-reasoner"
    assert len(deep_route["fallback_chain"]) >= 3

    # 2. Fast Classification should route to GLM
    fast_route = model_router.route_task("FAST_QUERY")
    assert fast_route["provider_name"] == "glm"
    assert "glm" in fast_route["model"]

    # 3. Court Pleading should route to Anthropic
    pleading_route = model_router.route_task("COURT_PLEADING", risk_level="HIGH")
    assert pleading_route["provider_name"] == "anthropic"
    assert "claude" in pleading_route["model"]

def test_seamless_llm_failover_execution():
    # Execute through execute_with_failover
    res = model_router.execute_with_failover(
        task_type="COMPLEX_LEGAL_ANALYSIS",
        prompt="Verify Akarband reconciliation for 2 Acres 24 Guntas",
        system_policy="Indian Property Jurisprudence"
    )
    assert "content" in res
    assert "routing_metadata" in res
    assert res["routing_metadata"]["task_type"] == "COMPLEX_LEGAL_ANALYSIS"
    assert res["routing_metadata"]["provider_selected"] in ["deepseek", "nvidia", "openai", "anthropic", "glm", "local"]

def test_provider_settings_health_and_privacy():
    status = provider_settings_service.get_provider_statuses()
    assert status["all_healthy"] is True
    assert status["total_providers"] >= 5
    
    # Verify no raw secret keys leaked
    text_dump = str(status)
    assert "sk-" not in text_dump
    assert "nvapi-" not in text_dump
    assert "AIza" not in text_dump
