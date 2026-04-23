
# Legal Document Intelligence & Reasoning System

A Python-based system that extracts entities, clauses, and relationships from legal documents and performs cross-document reasoning to identify obligations, risks, and shared entities.

This project demonstrates the use of Large Language Models (LLMs) for structured legal information extraction and reasoning across multiple documents.

---

# Overview

Legal documents often contain complex relationships between parties, obligations, and legal clauses. Manual review is time-consuming and error-prone.

This system automates:

* Legal entity extraction
* Clause identification
* Relationship mapping
* Cross-document reasoning
* Natural language question answering

It supports multiple legal documents and enables structured reasoning across them.

---

# Key Features

* Supports multiple legal documents (.txt and .pdf)
* Intelligent document chunking for LLM compatibility
* Entity extraction (parties, dates, amounts, obligations)
* Clause detection (confidentiality, payment, termination, liability)
* Relationship extraction between entities
* Cross-document reasoning
* Natural language Q&A over processed documents
* Sample legal datasets included

---

# How It Works

1. Upload one or more legal documents.
2. Each document is parsed and split into manageable text chunks.
3. For each chunk:

   * Entities are extracted.
   * Clauses are identified.
   * Relationships are detected.
4. Extracted results are merged across chunks.
5. Cross-document reasoning identifies:

   * Shared entities
   * Obligations
   * Risks
6. Users can query the processed documents using natural language questions.

---

# Project Architecture


`<img width="494" height="768" alt="Image" src="https://github.com/user-attachments/assets/bbb5b06b-289d-418d-aa0f-ad205c1abe60" />

# Installation

Clone the repository:

```bash
git clone https://github.com/JahnviPaliwal/legal_doc_intelligence.git
cd legal_doc_intelligence
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Set the Groq API key:

Linux / macOS:

```bash
export GROQ_API_KEY=your_key_here
```

Windows:

```powershell
set GROQ_API_KEY=your_key_here
```

Run the system:

```bash
streamlit run app.py
```

---

# Input Format

Supported file formats:

* `.txt`
* `.pdf`

Multiple documents can be processed together to enable cross-document reasoning.

---

# Sample Data

The `data/` directory includes sample legal documents:

* `nda_sample.txt`
  A fictional Non-Disclosure Agreement.

* `service_agreement_sample.txt`
  A fictional Software Services Agreement.

These files can be used to test the system without preparing custom documents.

---

# Example Queries

After processing documents, users can ask questions such as:

* What are the confidentiality obligations?
* Which parties appear in multiple documents?
* What is the payment schedule?
* What happens in case of breach?
* Are there termination conditions?
* What risks exist across agreements?

---

# Core Modules

## parser.py

Responsible for:

* Reading PDF and TXT files
* Cleaning extracted text
* Splitting large documents into smaller chunks
* Preparing data for downstream processing

---

## extraction.py

Handles:

* Named entity extraction
* Clause identification
* Relationship detection
* Structured output generation

Uses LLM-based prompts to extract legal knowledge from document text.

---

## reasoning.py

Implements:

* Cross-document entity comparison
* Obligation tracking
* Risk identification
* Question answering over extracted knowledge

Enables reasoning across multiple legal documents.

---

## app.py

Acts as the main execution script.

Responsible for:

* Loading documents
* Running parsing and extraction
* Performing reasoning
* Handling user queries

---

# Technologies Used

* Python
* Large Language Models (LLMs)
* Groq API
* Natural Language Processing (NLP)
* Document Parsing
* Information Extraction
* Reasoning Systems

---

# Design Considerations

* Chunking ensures compatibility with LLM token limits.
* Modular architecture separates parsing, extraction, and reasoning.
* Designed to support multiple legal documents.
* Structured outputs enable scalable reasoning workflows.

---

# Limitations

* Extraction quality depends on LLM accuracy.
* Very large documents may increase processing time.
* Legal reasoning is heuristic-based and should not replace professional legal review.

---

# Future Improvements

* Knowledge graph generation
* Clause classification models
* Risk scoring system
* Export results to JSON or CSV
* Support for additional document formats
* Evaluation metrics for extraction accuracy
* Batch processing pipelines

---

# Use Cases

This system can be applied to:

* Contract review automation
* Legal document analysis
* Risk detection workflows
* Compliance monitoring
* Due diligence processes
* Legal research assistance

---

# Security Notes

Do not commit API keys to version control.

Use environment variables to store secrets.

Example:

```
GROQ_API_KEY=your_key_here
```

---

