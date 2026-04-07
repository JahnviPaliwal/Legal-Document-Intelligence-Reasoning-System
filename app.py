"""
app.py – Streamlit frontend for Legal Document Intelligence & Reasoning
Run with:  streamlit run app.py
"""

import os
import json
import streamlit as st
from parser     import read_uploaded_file, chunk_text, read_file
from extraction import extract_from_chunk, merge_extractions
from reasoning  import cross_document_reasoning, answer_legal_question

# ── Page config ─────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Legal Document Intelligence",
    page_icon="⚖️",
    layout="wide",
)

st.title("⚖️ Legal Document Intelligence & Reasoning System")
st.markdown(
    "Upload one or more legal documents (.txt or .pdf). "
    "The system will extract **entities, clauses, and relationships**, "
    "then perform **cross-document reasoning** and let you ask questions."
)

# ── API key check ────────────────────────────────────────────────────────────
if not os.environ.get("GROQ_API_KEY"):
    st.error("⚠️  Please set the `GROQ_API_KEY` environment variable before running.")
    st.stop()

# ── Session state init ───────────────────────────────────────────────────────
if "doc_extractions" not in st.session_state:
    st.session_state["doc_extractions"] = {}
if "cross_doc_analysis" not in st.session_state:
    st.session_state["cross_doc_analysis"] = None

# ── Sidebar – load sample docs ───────────────────────────────────────────────
st.sidebar.header("📂 Quick-load Sample Documents")
if st.sidebar.button("Load sample legal documents"):
    sample_dir = os.path.join(os.path.dirname(__file__), "data")
    samples = ["nda_sample.txt", "service_agreement_sample.txt"]
    loaded = []
    for fname in samples:
        fpath = os.path.join(sample_dir, fname)
        if os.path.exists(fpath):
            text   = read_file(fpath)
            chunks = chunk_text(text)
            exts   = []
            for chunk in chunks:
                ext = extract_from_chunk(chunk, doc_name=fname)
                exts.append(ext)
            merged = merge_extractions(exts)
            st.session_state["doc_extractions"][fname] = merged
            loaded.append(fname)
    if loaded:
        st.sidebar.success(f"Loaded: {', '.join(loaded)}")
    else:
        st.sidebar.warning("Sample files not found in data/")

# ── File uploader ────────────────────────────────────────────────────────────
uploaded_files = st.file_uploader(
    "Upload legal documents (.txt or .pdf)",
    type=["txt", "pdf"],
    accept_multiple_files=True,
)

if uploaded_files and st.button("🔬 Extract from Uploaded Documents", type="primary"):
    for uf in uploaded_files:
        with st.spinner(f"Processing {uf.name}…"):
            text   = read_uploaded_file(uf)
            chunks = chunk_text(text)
            exts   = []
            for i, chunk in enumerate(chunks):
                ext = extract_from_chunk(chunk, doc_name=uf.name)
                exts.append(ext)
            merged = merge_extractions(exts)
            st.session_state["doc_extractions"][uf.name] = merged
    st.success(f"Processed {len(uploaded_files)} document(s).")
    # Reset cross-doc analysis when new docs are loaded
    st.session_state["cross_doc_analysis"] = None

# ── Display per-document results ─────────────────────────────────────────────
if st.session_state["doc_extractions"]:
    st.divider()
    st.subheader("📑 Per-Document Extraction Results")

    for doc_name, ext in st.session_state["doc_extractions"].items():
        with st.expander(f"📄 {doc_name}", expanded=False):
            tab1, tab2, tab3, tab4 = st.tabs(
                ["🏷️ Entities", "📜 Clauses", "🔗 Relations", "📦 Raw JSON"]
            )

            with tab1:
                entities = ext.get("entities", [])
                if entities:
                    for e in entities:
                        st.markdown(
                            f"**{e.get('name')}** "
                            f"*(type: {e.get('type', 'unknown')})*  \n"
                            f"{e.get('description', '')}"
                        )
                        st.divider()
                else:
                    st.write("No entities extracted.")

            with tab2:
                clauses = ext.get("clauses", [])
                if clauses:
                    for c in clauses:
                        st.markdown(f"### {c.get('clause_type', 'Clause')}")
                        st.write(f"**Summary:** {c.get('summary', '')}")
                        st.write(f"**Obligations:** {c.get('obligations', '')}")
                        st.divider()
                else:
                    st.write("No clauses extracted.")

            with tab3:
                relations = ext.get("relations", [])
                if relations:
                    for r in relations:
                        if len(r) == 3:
                            st.markdown(
                                f"- `{r[0]}` → **{r[1]}** → `{r[2]}`"
                            )
                else:
                    st.write("No relations extracted.")

            with tab4:
                st.json(ext)

# ── Cross-document reasoning ─────────────────────────────────────────────────
if len(st.session_state["doc_extractions"]) >= 1:
    st.divider()
    st.subheader("🧠 Cross-Document Reasoning")

    if st.button("🔍 Run Cross-Document Analysis"):
        with st.spinner("Analysing across all documents…"):
            analysis = cross_document_reasoning(
                st.session_state["doc_extractions"]
            )
            st.session_state["cross_doc_analysis"] = analysis

    if st.session_state["cross_doc_analysis"]:
        analysis = st.session_state["cross_doc_analysis"]

        st.subheader("📋 Executive Summary")
        st.info(analysis.get("summary", "No summary available."))

        col1, col2, col3 = st.columns(3)

        with col1:
            st.subheader("🔗 Common Entities")
            for e in analysis.get("common_entities", []):
                st.markdown(f"- {e}")

        with col2:
            st.subheader("📌 Key Obligations")
            for o in analysis.get("key_obligations", []):
                st.markdown(f"- {o}")

        with col3:
            st.subheader("⚠️ Risks & Gaps")
            for r in analysis.get("risks", []):
                st.markdown(f"- {r}")

    # ── Q&A section ──────────────────────────────────────────────────────────
    st.divider()
    st.subheader("💬 Ask a Question About the Documents")
    question = st.text_input(
        "Enter your question:",
        placeholder="e.g. What are the confidentiality obligations?",
    )
    if st.button("Ask") and question:
        with st.spinner("Thinking…"):
            answer = answer_legal_question(
                question,
                st.session_state["doc_extractions"],
            )
        st.markdown("**Answer:**")
        st.write(answer)
