from components.boot import boot
mode = boot()

import streamlit as st
from components.ai_rag import MiniRAG
from components.ai_client import chat
st.set_page_config(page_title="Ask Your Docs", layout="wide")
st.title("📚 Ask Your Docs (RAG)")
rag = st.session_state.setdefault("rag", MiniRAG())
txt = st.text_area("Paste text", height=200)
if st.button("Add to index"):
    if txt.strip(): rag.add_document(txt); st.success("Indexed.")
    else: st.warning("Paste some text first.")
q = st.text_input("Ask a question")
if st.button("Search & answer"):
    hits = rag.search(q, k=5); ctx = "\n\n".join([h[0] for h in hits])
    ans = chat([{"role":"system","content":"Answer using the provided context only. If unknown, say unknown."},
                {"role":"user","content": f"CONTEXT:\n{ctx}\n\nQUESTION: {q}"}])
    st.write(ans)
