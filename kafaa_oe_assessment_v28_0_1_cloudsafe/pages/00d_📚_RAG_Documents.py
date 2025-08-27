from components.boot import boot
mode = boot()

import streamlit as st, os, json, pathlib, shutil
from components.rag import RAGHelper

st.set_page_config(page_title="RAG Documents", layout="wide")
st.title("📚 RAG Documents — manage sources for grounded answers")

docs_dir = pathlib.Path("rag_docs"); docs_dir.mkdir(exist_ok=True)
manifest = docs_dir/"manifest.json"
if not manifest.exists(): manifest.write_text("[]", encoding="utf-8")

def load_manifest():
    try: return json.loads(manifest.read_text(encoding="utf-8"))
    except Exception: return []

def save_manifest(items): manifest.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding="utf-8")

st.sidebar.info("Tip: Add SOPs, standards, financial policies, or customer-specific procedures. The Observation engine will consult these.")

up = st.file_uploader("Upload documents (PDF/DOCX/TXT supported by your runtime)", accept_multiple_files=True)
if up:
    items = load_manifest()
    for f in up:
        out = docs_dir / f.name
        with open(out, "wb") as w: w.write(f.getbuffer())
        items.append({"name": f.name, "path": str(out)})
    save_manifest(items)
    st.success(f"Added {len(up)} document(s).")

st.markdown("### Current Library")
items = load_manifest()
if items:
    for it in items:
        st.write("• ", it["name"])
else:
    st.info("No documents yet.")

helper = RAGHelper()
if st.button("🔎 Index / Rebuild Vector Store", type="primary"):
    paths = [it["path"] for it in load_manifest()]
    mode = helper.index_paths(paths)
    st.success(f"Indexed in mode: {mode}.")
    st.caption("If QDRANT_URL is set, the index is stored in Qdrant; otherwise it uses local storage/fallback.")

if st.button("🗑️ Clear Library and RAG store"):
    shutil.rmtree(docs_dir, ignore_errors=True); docs_dir.mkdir(exist_ok=True)
    shutil.rmtree(helper.base, ignore_errors=True); helper.base.mkdir(exist_ok=True)
    save_manifest([])
    st.warning("Cleared documents and vector store.")
