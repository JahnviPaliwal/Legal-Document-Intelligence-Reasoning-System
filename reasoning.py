"""
reasoning.py
Cross-document reasoning and summarisation.
Given structured extractions from multiple legal documents,
the LLM connects entities, spots overlaps, and writes a summary.
"""

import json
from groq import Groq

client = Groq()
MODEL  = "llama-3.1-8b-instant"


def cross_document_reasoning(doc_extractions: dict[str, dict]) -> dict:
    """
    Performs cross-document analysis over all uploaded documents.

    Parameters
    ----------
    doc_extractions : {filename: merged_extraction_dict, ...}

    Returns
    -------
    dict with:
        summary          : str – natural language executive summary
        common_entities  : list[str] – entities appearing in multiple docs
        key_obligations  : list[str] – important obligations across all docs
        risks            : list[str] – potential risks or conflicts identified
    """
    # Build a compact context for the LLM
    context_parts = []
    for doc_name, ext in doc_extractions.items():
        entities  = [e["name"] for e in ext.get("entities", [])]
        clause_summaries = [c["summary"] for c in ext.get("clauses", [])]
        context_parts.append(
            f"Document: {doc_name}\n"
            f"Entities: {', '.join(entities[:20])}\n"
            f"Clause summaries: {'; '.join(clause_summaries[:10])}"
        )

    context = "\n\n---\n\n".join(context_parts)

    prompt = f"""You are a senior legal analyst reviewing multiple contracts.

Here is a structured summary of the documents:

{context}

Please provide:
1. A concise executive summary (3-5 sentences) covering all documents.
2. Entities that appear across multiple documents (cross-document links).
3. The most important obligations found.
4. Any potential risks, conflicts, or gaps you notice.

Return ONLY valid JSON – no prose, no markdown fences:
{{
  "summary": "...",
  "common_entities": ["Entity1", "Entity2"],
  "key_obligations": ["Obligation 1", "Obligation 2"],
  "risks": ["Risk 1", "Risk 2"]
}}
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )

    import re
    raw = response.choices[0].message.content.strip()
    raw = re.sub(r"^```[a-z]*\n?", "", raw)
    raw = re.sub(r"\n?```$", "", raw)

    try:
        result = json.loads(raw)
    except json.JSONDecodeError:
        # Graceful fallback
        result = {
            "summary":         raw,
            "common_entities": [],
            "key_obligations": [],
            "risks":           [],
        }

    return result


def answer_legal_question(question: str,
                           doc_extractions: dict[str, dict]) -> str:
    """
    Answers a specific question about the uploaded legal documents.
    """
    context = json.dumps(doc_extractions, indent=2)[:4000]  # trim for safety

    prompt = f"""You are a legal document assistant.
Based on the extracted information from the following legal documents,
answer the question as accurately as possible.

Extracted data:
{context}

Question: {question}

Give a clear, concise answer. If the information is not available, say so.
"""

    response = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
    )
    return response.choices[0].message.content.strip()
