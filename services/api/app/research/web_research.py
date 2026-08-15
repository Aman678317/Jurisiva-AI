# Web & External Legal Researcher Engine
# Connects to external legal search providers and curated statutory/judgment databases.

from typing import Dict, List, Any, Optional
from app.research.research_provider import external_research_provider

class WebResearcher:
    """Executes real external research over verified statutory and judicial repositories."""

    def search_external_legal_sources(
        self,
        query: str,
        jurisdiction: Optional[Dict[str, str]] = None,
        max_sources: int = 4
    ) -> List[Dict[str, Any]]:
        state = jurisdiction.get("state", "Karnataka") if jurisdiction else "Karnataka"
        results = external_research_provider.search_legal_sources(query, state=state, max_results=max_sources)
        return results

web_researcher = WebResearcher()
