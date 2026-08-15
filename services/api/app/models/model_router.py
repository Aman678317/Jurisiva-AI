# Governed Model Router with Multi-Provider Key Rotation & Automatic LLM Failover
# Routes tasks across NVIDIA, DeepSeek, GLM, OpenAI, Anthropic, Google, and Sovereign Local models.

import logging
from typing import Dict, List, Any, Optional
from app.models.llm_provider import (
    LLMProvider,
    NvidiaProvider,
    DeepSeekProvider,
    GLMProvider,
    OpenAIProvider,
    AnthropicProvider,
    GoogleProvider,
    LocalProvider
)

logger = logging.getLogger("JurisivaModelRouter")

class ModelRouter:
    """Intelligent router dispatching AI tasks across multi-model architecture with automatic failover."""

    def __init__(self):
        self._providers: Dict[str, LLMProvider] = {
            "nvidia": NvidiaProvider(),
            "deepseek": DeepSeekProvider(),
            "glm": GLMProvider(),
            "openai": OpenAIProvider(),
            "anthropic": AnthropicProvider(),
            "google": GoogleProvider(),
            "local": LocalProvider()
        }

    def route_task(
        self,
        task_type: str,
        risk_level: str = "MEDIUM",
        latency_requirement: str = "NORMAL",
        cost_budget: str = "BALANCED",
        data_policy: str = "CLOUD_ENTERPRISE",
        modality: str = "TEXT"
    ) -> Dict[str, Any]:
        """
        Determines the primary route and ordered fallback chain of providers & models.
        Task types:
          - COMPLEX_LEGAL_ANALYSIS / CONTRADICTION_AUDIT / DEEP_REASONING
          - FAST_QUERY / CLASSIFICATION / ENTITY_EXTRACTION
          - DOCUMENT_VISION / MAP_INSPECTION
          - EMBEDDING
          - COURT_PLEADING / HIGH_RISK_DRAFT
        """
        # Strict Sovereign / Local Data Policy
        if data_policy == "AIR_GAPPED_LOCAL":
            return {
                "provider_name": "local",
                "provider": self._providers["local"],
                "model": "local-llama3-legal-8b" if modality == "TEXT" else "local-florence-2",
                "fallback_chain": [
                    {"provider": "local", "model": "local-llama3-legal-8b"}
                ],
                "tier": "SOVEREIGN_LOCAL",
                "reason": "Air-gapped data residency policy enforced."
            }

        # Modality: Multimodal Vision & Deed Layouts
        if modality in ["VISION", "IMAGE", "MAP_SKETCH"]:
            return {
                "provider_name": "google",
                "provider": self._providers["google"],
                "model": "gemini-1.5-pro",
                "fallback_chain": [
                    {"provider": "google", "model": "gemini-1.5-pro"},
                    {"provider": "nvidia", "model": "meta/llama-3.2-11b-vision-instruct"},
                    {"provider": "glm", "model": "glm-4v"},
                    {"provider": "openai", "model": "gpt-4o"}
                ],
                "tier": "MULTIMODAL_VISION",
                "reason": "High-accuracy Indic document and map layout vision model selected."
            }

        # Modality: Embeddings
        if task_type == "EMBEDDING" or modality == "EMBEDDING":
            return {
                "provider_name": "openai",
                "provider": self._providers["openai"],
                "model": "text-embedding-3-large",
                "fallback_chain": [
                    {"provider": "openai", "model": "text-embedding-3-large"},
                    {"provider": "nvidia", "model": "nvidia/nv-embed-v1"},
                    {"provider": "glm", "model": "embedding-2"}
                ],
                "tier": "EMBEDDING",
                "reason": "Dense multilingual semantic embedding model selected."
            }

        # Deep Legal Reasoning / Complex Title Contradiction / Root Audit
        if task_type in ["COMPLEX_LEGAL_ANALYSIS", "CONTRADICTION_AUDIT", "DEEP_REASONING", "RESEARCH_SYNTHESIS"]:
            return {
                "provider_name": "deepseek",
                "provider": self._providers["deepseek"],
                "model": "deepseek-reasoner", # DeepSeek R1 with Chain of Thought
                "fallback_chain": [
                    {"provider": "deepseek", "model": "deepseek-reasoner"},
                    {"provider": "nvidia", "model": "nvidia/llama-3.1-nemotron-70b-instruct"},
                    {"provider": "openai", "model": "gpt-4o"},
                    {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
                    {"provider": "glm", "model": "glm-4-plus"}
                ],
                "tier": "DEEP_LEGAL_REASONING",
                "reason": "DeepSeek-R1 & NVIDIA Nemotron selected for deep statutory reasoning."
            }

        # High Risk Court Pleadings & Certified Diligence Opinions
        if risk_level == "HIGH" or task_type in ["HIGH_RISK_DRAFT", "COURT_PLEADING", "TITLE_OPINION"]:
            return {
                "provider_name": "anthropic",
                "provider": self._providers["anthropic"],
                "model": "claude-3-5-sonnet-20241022",
                "fallback_chain": [
                    {"provider": "anthropic", "model": "claude-3-5-sonnet-20241022"},
                    {"provider": "deepseek", "model": "deepseek-reasoner"},
                    {"provider": "nvidia", "model": "meta/llama-3.1-70b-instruct"},
                    {"provider": "openai", "model": "gpt-4o"},
                    {"provider": "glm", "model": "glm-4"}
                ],
                "tier": "ADVANCED_DRAFTING",
                "reason": "Claude 3.5 Sonnet / DeepSeek-R1 selected for court-grade drafting."
            }

        # Fast Query / Rapid Entity Extraction / Multilingual Classification
        if task_type in ["FAST_QUERY", "CLASSIFICATION", "ENTITY_EXTRACTION"] or latency_requirement == "LOW":
            return {
                "provider_name": "glm",
                "provider": self._providers["glm"],
                "model": "glm-4-flash",
                "fallback_chain": [
                    {"provider": "glm", "model": "glm-4-flash"},
                    {"provider": "glm", "model": "glm-2"},
                    {"provider": "openai", "model": "gpt-4o-mini"},
                    {"provider": "google", "model": "gemini-1.5-flash"},
                    {"provider": "deepseek", "model": "deepseek-chat"}
                ],
                "tier": "LOW_LATENCY_FAST_EXTRACTION",
                "reason": "GLM-4 / GLM-2 / GPT-4o-mini selected for low latency and high throughput."
            }

        # Default Balanced Legal Route
        return {
            "provider_name": "deepseek",
            "provider": self._providers["deepseek"],
            "model": "deepseek-chat",
            "fallback_chain": [
                {"provider": "deepseek", "model": "deepseek-chat"},
                {"provider": "nvidia", "model": "nvidia/llama-3.1-nemotron-70b-instruct"},
                {"provider": "openai", "model": "gpt-4o-mini"},
                {"provider": "glm", "model": "glm-4"},
                {"provider": "google", "model": "gemini-1.5-flash"}
            ],
            "tier": "BALANCED_LEGAL",
            "reason": "Standard balanced legal inference route across multi-LLM mesh."
        }

    def execute_with_failover(
        self,
        task_type: str,
        prompt: str,
        system_policy: str = "Strict Indian Property Law Grounding",
        risk_level: str = "MEDIUM",
        temperature: float = 0.0,
        max_tokens: int = 2000
    ) -> Dict[str, Any]:
        """
        Executes generation across the fallback chain.
        If a provider/key hits a rate limit or error, automatically passes to the next provider.
        """
        route = self.route_task(task_type=task_type, risk_level=risk_level)
        fallback_chain = route.get("fallback_chain", [{"provider": route["provider_name"], "model": route["model"]}])
        
        attempt_errors = []

        for candidate in fallback_chain:
            p_name = candidate["provider"]
            model_name = candidate["model"]
            provider = self._providers.get(p_name)

            if not provider:
                continue

            try:
                logger.info(f"Dispatching task '{task_type}' to [{p_name}] model '{model_name}'")
                res = provider.generate(
                    prompt=prompt,
                    system_policy=system_policy,
                    model=model_name,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                res["routing_metadata"] = {
                    "task_type": task_type,
                    "provider_selected": p_name,
                    "model_selected": model_name,
                    "tier": route["tier"],
                    "failover_attempts": len(attempt_errors)
                }
                return res
            except Exception as ex:
                err_msg = f"Provider [{p_name}] with model '{model_name}' failed: {str(ex)}"
                logger.warning(f"Failover triggered: {err_msg}")
                attempt_errors.append(err_msg)
                continue

        # If all providers in chain fail, fallback to sovereign local
        logger.error(f"All providers in chain failed for task '{task_type}'. Falling back to local sovereign provider.")
        local_res = self._providers["local"].generate(prompt, system_policy, "local-llama3-legal-8b")
        local_res["routing_metadata"] = {
            "task_type": task_type,
            "provider_selected": "local",
            "model_selected": "local-llama3-legal-8b",
            "tier": "EMERGENCY_SOVEREIGN_FALLBACK",
            "failover_attempts": len(attempt_errors)
        }
        return local_res

    def get_provider(self, provider_name: str) -> LLMProvider:
        return self._providers.get(provider_name, self._providers["deepseek"])

model_router = ModelRouter()
