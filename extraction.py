"""
extraction.py
Calls the LLM to extract structured legal entities, clauses, and
relationships from text chunks.
"""

import re
import json
from groq import Groq

client = Groq()
MODEL  = "llama-3.1-8b-instant"


def extract_from_chunk(chunk: str, doc_name: str = "unknown") -> dict:
    """
    Sends one text chunk to the LLM and asks it to extract legal structure.

    Returns a dict with:
        entities  : list of {name, type, description}
        clauses   : list of {clause_type, summary, obligations}
        relations : list of [party_a, relationship, party_b]
    """
    prompt = f"""You are a legal document analyst.
Analyse the following excerpt from a legal document called "{doc_name}".

Extract:
1. Entities – parties, dates, monetary values, locations, organisations.
2. Clauses – type (e.g. Indemnity, Confidentiality, Termination, Payment),
   a one-sentence summary, and key obligations.
3. Relationships – pairs of entities and how they are related.

Return ONLY valid JSON – no prose, no markdown fences – in this exact format:
{{
  "entities": [
    {{"name": "...", "type": "...", "description": "..."}}
  ],
  "clauses": [
    {{"clause_type": "...", "summary": "...", "obligations": "..."}}
  ],
  "relations": [
    ["Party A", "relationship", "Party B"]
  ]
}}

Document excerpt:
\"\"\"
{chunk}
\"\"\"
"""
    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
    )

    raw = response.choices[0].message.content.strip()
    # Strip markdown fences
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)

    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        return {"entities": [], "clauses": [], "relations": []}


def merge_extractions(extractions: list[dict]) -> dict:
    """
    Merges extraction results from multiple chunks of the same document.
    Deduplicates entities by name and clauses by type+summary.
    """
    all_entities  = {}  # name → entity dict (dedup by name)
    all_clauses   = []
    all_relations = set()

    for ext in extractions:
        for entity in ext.get("entities", []):
            key = entity.get("name", "").lower()
            if key and key not in all_entities:
                all_entities[key] = entity

        for clause in ext.get("clauses", []):
            # Simple dedup: same type + same first 60 chars of summary
            sig = (clause.get("clause_type", ""),
                   clause.get("summary", "")[:60])
            if not any(
                (c.get("clause_type"), c.get("summary", "")[:60]) == sig
                for c in all_clauses
            ):
                all_clauses.append(clause)

        for rel in ext.get("relations", []):
            if len(rel) == 3:
                all_relations.add(tuple(rel))

    return {
        "entities":  list(all_entities.values()),
        "clauses":   all_clauses,
        "relations": [list(r) for r in all_relations],
    }
