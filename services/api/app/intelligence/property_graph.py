# Temporal Property Knowledge Graph Engine
# Models Persons, Parcels, Documents, Transactions, Mortgages, and Claims with temporal validity

import time
from typing import Dict, List, Any, Optional

class PropertyKnowledgeGraph:
    """Graph structure with temporal validity (valid_from, valid_to) and provenance on all edges."""

    def __init__(self):
        # Nodes: { node_id: { type, properties } }
        self._nodes: Dict[str, Dict[str, Any]] = {}
        # Edges: [ { source_id, target_id, relation, valid_from, valid_to, provenance_doc, properties } ]
        self._edges: List[Dict[str, Any]] = []
        self._initialize_benchmark_graph()

    def _initialize_benchmark_graph(self):
        """Populates benchmark matter #mat_001 property graph."""
        # Nodes
        self.add_node("person_venkatappa", "PERSON", {"name": "Venkatappa", "father_name": "Late Muniyappa", "role": "Original Vendor"})
        self.add_node("person_krishnappa", "PERSON", {"name": "Krishnappa", "father_name": "Late Venkataramanappa", "role": "Purchaser 1985"})
        self.add_node("person_ramesh", "PERSON", {"name": "Ramesh Kumar", "father_name": "Krishnappa", "role": "Current Title Holder"})
        self.add_node("bank_sbi", "ORGANIZATION", {"name": "State Bank of India", "role": "Secured Creditor"})
        self.add_node("parcel_sy42_1", "PROPERTY_PARCEL", {"survey_number": "42/1", "hissa": "2", "village": "Devanahalli", "total_root_extent": "2 Acres 24 Guntas"})
        self.add_node("doc_sale_1985", "DOCUMENT", {"title": "Registered Sale Deed 1985", "reg_number": "1234/1985-86", "extent_conveyed": "2 Acres 24 Guntas"})
        self.add_node("doc_sale_2018", "DOCUMENT", {"title": "Registered Sale Deed 2018", "reg_number": "4567/2018-19", "extent_conveyed": "2 Acres 10 Guntas"})
        self.add_node("doc_mortgage_2010", "DOCUMENT", {"title": "Simple Mortgage 2010", "amount": "₹50,00,000", "bank": "SBI"})
        self.add_node("auth_2023_insc_891", "LEGAL_AUTHORITY", {"citation": "2023 INSC 891", "title": "Anandram vs LAO", "court": "Supreme Court of India"})

        # Temporal Edges
        self.add_edge("person_venkatappa", "parcel_sy42_1", "OWNS", "1950-01-01", "1985-11-14", "doc_sale_1985")
        self.add_edge("person_venkatappa", "person_krishnappa", "TRANSFERRED_TO", "1985-11-14", "1985-11-14", "doc_sale_1985", {"extent": "2A 24G", "consideration": "₹45,000"})
        self.add_edge("person_krishnappa", "parcel_sy42_1", "OWNS", "1985-11-14", "2018-10-18", "doc_sale_1985")
        self.add_edge("person_krishnappa", "bank_sbi", "MORTGAGED_TO", "2010-06-22", "9999-12-31", "doc_mortgage_2010", {"amount": "₹50,00,000", "status": "UNDISCHARGED"})
        self.add_edge("person_krishnappa", "person_ramesh", "TRANSFERRED_TO", "2018-10-18", "2018-10-18", "doc_sale_2018", {"extent": "2A 10G", "deficit": "14 Guntas"})
        self.add_edge("person_ramesh", "parcel_sy42_1", "OWNS", "2018-10-18", "9999-12-31", "doc_sale_2018")
        self.add_edge("doc_sale_2018", "doc_sale_1985", "CONTRADICTS", "2018-10-18", "9999-12-31", "doc_sale_2018", {"discrepancy": "14 Guntas Area Shortage"})
        self.add_edge("auth_2023_insc_891", "doc_sale_2018", "SUPPORTS", "2023-11-20", "9999-12-31", "auth_2023_insc_891", {"remedy": "Revenue Durasti Overrides Deed Recital"})

    def add_node(self, node_id: str, node_type: str, properties: Dict[str, Any]):
        self._nodes[node_id] = {"id": node_id, "type": node_type, "properties": properties}

    def add_edge(
        self,
        source_id: str,
        target_id: str,
        relation: str,
        valid_from: str,
        valid_to: str,
        provenance_doc: str,
        properties: Optional[Dict[str, Any]] = None
    ):
        self._edges.append({
            "source_id": source_id,
            "target_id": target_id,
            "relation": relation,
            "valid_from": valid_from,
            "valid_to": valid_to,
            "provenance_doc": provenance_doc,
            "properties": properties or {}
        })

    def query_ownership_history(self, parcel_id: str = "parcel_sy42_1") -> List[Dict[str, Any]]:
        """Answers: 'Who owned Survey 42/1 over time?'"""
        history = []
        for edge in self._edges:
            if edge["target_id"] == parcel_id and edge["relation"] == "OWNS":
                owner_node = self._nodes.get(edge["source_id"], {})
                history.append({
                    "owner_name": owner_node.get("properties", {}).get("name", edge["source_id"]),
                    "valid_from": edge["valid_from"],
                    "valid_to": edge["valid_to"],
                    "provenance_document": edge["provenance_doc"]
                })
        history.sort(key=lambda x: x["valid_from"])
        return history

    def query_discrepancies(self) -> List[Dict[str, Any]]:
        """Answers: 'Which document introduced the 14-Gunta discrepancy?'"""
        discrepancies = []
        for edge in self._edges:
            if edge["relation"] == "CONTRADICTS":
                discrepancies.append({
                    "source_doc": edge["source_id"],
                    "contradicts_doc": edge["target_id"],
                    "details": edge["properties"]
                })
        return discrepancies

    def query_supporting_claims(self, claim_target_id: str = "doc_sale_2018") -> List[Dict[str, Any]]:
        """Answers: 'Which documents/precedents support the current owner's claim?'"""
        supporters = []
        for edge in self._edges:
            if edge["target_id"] == claim_target_id and edge["relation"] == "SUPPORTS":
                supporter_node = self._nodes.get(edge["source_id"], {})
                supporters.append({
                    "authority": supporter_node.get("properties", {}).get("citation", edge["source_id"]),
                    "title": supporter_node.get("properties", {}).get("title"),
                    "remedy": edge["properties"].get("remedy")
                })
        return supporters

property_graph = PropertyKnowledgeGraph()
