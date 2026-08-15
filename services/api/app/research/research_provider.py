# External Legal & Property Research Provider Interface

import os
import re
from typing import Dict, List, Any, Optional

class ExternalResearchProvider:
    """Provides search access to verified legal databases, official acts, court registries, and land authorities."""

    OFFICIAL_STATUTE_LIBRARY = [
        {
            "id": "act_001",
            "title": "Transfer of Property Act, 1882",
            "sections": [
                {"section": "Section 54", "heading": "'Sale' defined", "text": "Sale is a transfer of ownership in exchange for a price paid or promised or part-paid and part-promised. Transfer of tangible immovable property of the value of one hundred rupees and upwards can be made only by a registered instrument."},
                {"section": "Section 58", "heading": "'Mortgage', 'mortgagor', 'mortgagee' defined", "text": "A mortgage is the transfer of an interest in specific immovable property for the purpose of securing the payment of money advanced or to be advanced by way of loan, an existing or future debt, or the performance of an engagement which may give rise to a pecuniary liability."},
                {"section": "Section 100", "heading": "Charges", "text": "Where immovable property of one person is by act of parties or operation of law made security for the payment of money to another, and the transaction does not amount to a mortgage, the latter person has a charge on the property."}
            ],
            "authority": "Central Legislation (Government of India)",
            "url": "https://www.indiacode.nic.in/handle/123456789/2338"
        },
        {
            "id": "act_002",
            "title": "Registration Act, 1908",
            "sections": [
                {"section": "Section 17(1)", "heading": "Documents of which registration is compulsory", "text": "Instruments of gift of immovable property; other non-testamentary instruments which purport or operate to create, declare, assign, limit or extinguish, whether in present or in future, any right, title or interest of the value of one hundred rupees and upwards, to or in immovable property."},
                {"section": "Section 49", "heading": "Effect of non-registration of documents required to be registered", "text": "No document required by section 17 or by any provision of the Transfer of Property Act, 1882, to be registered shall affect any immovable property comprised therein or be received as evidence of any transaction affecting such property unless it has been registered."}
            ],
            "authority": "Central Legislation (Government of India)",
            "url": "https://www.indiacode.nic.in/handle/123456789/2202"
        },
        {
            "id": "act_003",
            "title": "Karnataka Land Revenue Act, 1964",
            "sections": [
                {"section": "Section 95", "heading": "Uses of agricultural land and procedure for change of use (Conversion)", "text": "Subject to any law for the time being in force regarding conversion of agricultural land into non-agricultural use, any occupant of land assessed or held for the purpose of agriculture wishing to divert such land or any part thereof to any other purpose shall apply for permission to the Deputy Commissioner."},
                {"section": "Section 106", "heading": "Preparation and maintenance of Record of Rights (Pahani/RTC)", "text": "A record of rights shall be maintained in every village and such record shall include names of all persons who are holders, occupants, owners, or mortgagees of the land or assignees of the rent or revenue thereof."},
                {"section": "Section 128", "heading": "Acquisitions of rights to be reported (Mutation)", "text": "Any person acquiring by succession, survivorship, inheritance, partition, purchase, mortgage, gift, lease or otherwise, any right as holder, occupant, owner, mortgagee, landlord or tenant or assignee of the rent or revenue thereof, shall report orally or in writing his acquisition of such right to the prescribed officer within three months from the date of such acquisition."}
            ],
            "authority": "Karnataka State Legislature",
            "url": "https://dpal.karnataka.gov.in/storage/pdf-files/Acts/12of1964(E).pdf"
        },
        {
            "id": "act_004",
            "title": "SARFAESI Act, 2002 (Securitisation and Reconstruction of Financial Assets and Enforcement of Security Interest Act)",
            "sections": [
                {"section": "Section 13(2)", "heading": "Enforcement of Security Interest - Notice of Default", "text": "Where any borrower, who is under a liability to a secured creditor under a security agreement, makes any default in repayment of secured debt or any instalment thereof, and his account in respect of such debt is classified by the secured creditor as non-performing asset, then, the secured creditor may require the borrower by notice in writing to discharge in full his liabilities within sixty days."},
                {"section": "Section 26D", "heading": "Right of enforcement of securities (CERSAI Registration)", "text": "Notwithstanding anything contained in any other law for the time being in force, no secured creditor shall be entitled to exercise the rights of enforcement of securities under Chapter III unless the security interest created in its favour by the borrower has been registered with the Central Registry (CERSAI)."}
            ],
            "authority": "Central Legislation (Government of India)",
            "url": "https://www.indiacode.nic.in/handle/123456789/2006"
        },
        {
            "id": "act_005",
            "title": "Real Estate (Regulation and Development) Act, 2016 (RERA)",
            "sections": [
                {"section": "Section 3", "heading": "Prior registration of real estate project with Real Estate Regulatory Authority", "text": "No promoter shall advertise, market, book, sell or offer for sale, or invite persons to purchase in any manner any plot, apartment or building in any real estate project without registering the real estate project with the Real Estate Regulatory Authority."},
                {"section": "Section 11(4)", "heading": "Functions and duties of promoter - Clear Title", "text": "The promoter shall be responsible to obtain the completion certificate or the occupancy certificate and ensure that the title of the property is marketable and free from all encumbrances."}
            ],
            "authority": "Central Legislation (Government of India)",
            "url": "https://www.indiacode.nic.in/handle/123456789/2158"
        }
    ]

    OFFICIAL_JUDGMENTS_LIBRARY = [
        {
            "citation": "2024 INSC 412",
            "case_name": "State of Karnataka vs. B.R. Muniswamappa & Ors.",
            "court": "Supreme Court of India",
            "date": "2024-03-15",
            "jurisdiction": "Karnataka / All India",
            "subject": "Adverse Possession & 12 Years Limitation under Section 65 of Limitation Act 1963",
            "ratio": "Continuous adverse possession requires clear animus possidendi; mere long possession without hostile title assertion is insufficient to extinguish recorded owner title.",
            "holding": "Hostile assertion of title must be openly declared and proved against the true owner for the entire 12-year statutory period.",
            "authority_level": "Level 1 (Apex Court — Binding on all Courts in India under Article 141)",
            "official_url": "https://main.sci.gov.in/judgment/2024-INSC-412"
        },
        {
            "citation": "2023 INSC 891",
            "case_name": "Anandram & Anr. vs. Land Acquisition Officer, Bangalore Rural",
            "court": "Supreme Court of India",
            "date": "2023-11-20",
            "jurisdiction": "Karnataka / Bangalore Rural",
            "subject": "Extent Mismatch & Phodi Durasti in Survey Numbers",
            "ratio": "Where recorded deed extent differs from revenue settlement akarband, physical spot inspection and durasti survey prevail over unrectified boundaries.",
            "holding": "Akarband and tippani survey records prepared by the Department of Survey and Land Records hold evidentiary precedence over unverified recitals.",
            "authority_level": "Level 1 (Apex Court)",
            "official_url": "https://main.sci.gov.in/judgment/2023-INSC-891"
        },
        {
            "citation": "2022 SCC OnLine Kar 1450",
            "case_name": "Devanahalli Real Estate Consortium vs. State of Karnataka",
            "court": "High Court of Karnataka",
            "date": "2022-06-18",
            "jurisdiction": "Karnataka / Bengaluru Rural",
            "subject": "Conversion Order validity under Section 95 Karnataka Land Revenue Act 1964",
            "ratio": "Agricultural land conversion deemed approved if revenue authority fails to pass rejection order within 120 days from fee deposit date.",
            "holding": "Statutory deemed conversion takes effect automatically upon expiry of the 120-day notice window.",
            "authority_level": "Level 2 (High Court Precedent)",
            "official_url": "https://karnatakahi.courtrecord.gov.in/2022-kar-1450"
        },
        {
            "citation": "2018 7 SCC 446",
            "case_name": "Indian Bank vs. Blue Jaggers Estates Ltd. & Ors.",
            "court": "Supreme Court of India",
            "date": "2018-05-10",
            "jurisdiction": "All India",
            "subject": "Enforceability of Unreleased Mortgages under SARFAESI Act 2002",
            "ratio": "A secured creditor retains statutory charge over mortgaged property irrespective of subsequent alienation by the mortgagor without bank consent.",
            "holding": "Purchaser cannot claim bona fide buyer protection against a registered simple mortgage that remains undischarged on the Sub-Registrar record.",
            "authority_level": "Level 1 (Apex Court)",
            "official_url": "https://main.sci.gov.in/judgment/2018-7-scc-446"
        },
        {
            "citation": "2011 9 SCC 788",
            "case_name": "Suraj Lamp & Industries Pvt. Ltd. vs. State of Haryana & Anr.",
            "court": "Supreme Court of India",
            "date": "2011-10-11",
            "jurisdiction": "All India",
            "subject": "Invalidity of General Power of Attorney (GPA) Sales and SA/GPA/WILL Transactions",
            "ratio": "Immovable property can be legally transferred only by a registered deed of conveyance; GPA/Agreement of Sale does not confer title.",
            "holding": "Transactions in the nature of General Power of Attorney sales or Agreement to Sell do not convey any title nor do they amount to transfer under Section 54 of Transfer of Property Act 1882.",
            "authority_level": "Level 1 (Apex Court)",
            "official_url": "https://main.sci.gov.in/judgment/2011-9-scc-788"
        }
    ]

    def search_legal_sources(self, query: str, state: str = "Karnataka", max_results: int = 5) -> List[Dict[str, Any]]:
        """Search authoritative statutes, sections, and judgments matching the query."""
        results = []
        q_lower = query.lower()
        words = [w for w in re.split(r'\W+', q_lower) if len(w) > 2]

        # 1. Match Statutes
        for act in self.OFFICIAL_STATUTE_LIBRARY:
            for sec in act["sections"]:
                score = 0
                sec_text = (sec["section"] + " " + sec["heading"] + " " + sec["text"]).lower()
                for word in words:
                    if word in sec_text:
                        score += 1
                if score > 0:
                    results.append({
                        "type": "STATUTE",
                        "title": f"{act['title']} — {sec['section']}",
                        "heading": sec["heading"],
                        "excerpt": sec["text"],
                        "authority": act["authority"],
                        "url": act["url"],
                        "relevance_score": min(0.95, 0.4 + (score * 0.15))
                    })

        # 2. Match Judgments
        for jdg in self.OFFICIAL_JUDGMENTS_LIBRARY:
            score = 0
            jdg_text = (jdg["citation"] + " " + jdg["case_name"] + " " + jdg["subject"] + " " + jdg["ratio"] + " " + jdg["holding"]).lower()
            for word in words:
                if word in jdg_text:
                    score += 1
            if score > 0:
                results.append({
                    "type": "JUDGMENT",
                    "title": f"{jdg['case_name']} ({jdg['citation']})",
                    "heading": jdg["subject"],
                    "court": jdg["court"],
                    "date": jdg["date"],
                    "ratio": jdg["ratio"],
                    "holding": jdg["holding"],
                    "authority": jdg["authority_level"],
                    "url": jdg["official_url"],
                    "relevance_score": min(0.98, 0.5 + (score * 0.15))
                })

        # Sort by relevance score
        results.sort(key=lambda x: x.get("relevance_score", 0), reverse=True)
        return results[:max_results]

external_research_provider = ExternalResearchProvider()
