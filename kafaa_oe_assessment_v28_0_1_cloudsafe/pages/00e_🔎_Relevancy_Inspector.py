from components.boot import boot
mode = boot()

import streamlit as st, json

st.set_page_config(page_title="Relevancy Inspector", layout="wide")
st.title("🔎 Document Relevancy Inspector")

ans = st.session_state.get("rag_last_answer", "")
srcs = st.session_state.get("rag_last_sources", [])
score = st.session_state.get("rag_last_score", {})

st.markdown("**RAG Draft (latest)**")
st.text_area("Draft", value=ans, height=200)

col1, col2, col3 = st.columns(3)
col1.metric("Faithfulness", f"{score.get('faithfulness','—')}")
col2.metric("Context Precision", f"{score.get('context_precision','—')}")
col3.metric("Sources", f"{len(srcs)}")

st.markdown("### Top Source Snippets")
if not srcs:
    st.info("No indexed sources yet. Go to **00d — RAG Documents** to add and index files.")
else:
    for i, s in enumerate(srcs[:5]):
        st.markdown(f"**Source {i+1}:**\n\n> {s}")

# Download bundle
bundle = {"draft": ans, "sources": srcs, "score": score}
st.download_button("Download RAG bundle (JSON)", data=json.dumps(bundle, ensure_ascii=False, indent=2), file_name="rag_bundle.json")
