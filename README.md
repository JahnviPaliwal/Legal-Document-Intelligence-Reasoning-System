# Legal Document Intelligence & Reasoning System

Extract entities, clauses, and relationships from legal documents and reason across them.

## Setup

```bash
cd legal_doc_intelligence
pip install -r requirements.txt
export GROQ_API_KEY=your_key_here
streamlit run app.py
```

## How It Works

1. Upload one or more legal documents (.txt or .pdf)
2. Each document is chunked into LLM-friendly segments
3. Entities, clauses, and relationships are extracted per chunk, then merged
4. Cross-document reasoning identifies common entities, key obligations, and risks
5. A Q&A interface lets you ask questions about the documents

## Sample Data

Two sample documents are included in `data/`:
- `nda_sample.txt` – A fictional Non-Disclosure Agreement
- `service_agreement_sample.txt` – A fictional Software Services Agreement

Use the **"Load sample legal documents"** button in the sidebar to process them instantly.

## Sample Questions to Ask

- *What are the confidentiality obligations?*
- *Which parties appear in multiple documents?*
- *What is the payment schedule?*
- *What happens if there is a breach?*

## File Structure

| File | Purpose |
|---|---|
| `app.py` | Streamlit UI |
| `parser.py` | PDF/text reading and chunking |
| `extraction.py` | LLM-based entity, clause, relation extraction |
| `reasoning.py` | Cross-document reasoning and Q&A |
| `data/` | Sample legal text files |
| `requirements.txt` | Python dependencies |



<img width="494" height="768" alt="Image" src="https://github.com/user-attachments/assets/bbb5b06b-289d-418d-aa0f-ad205c1abe60" />
