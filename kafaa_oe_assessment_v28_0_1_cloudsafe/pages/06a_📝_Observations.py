from components.boot import boot
mode = boot()

import streamlit as st
from components.rag import RAGHelper
from components.rag_eval import eval_rag

from components.ai_observations import generate_observations_ai
st.set_page_config(page_title="Observations", layout="wide")
st.title("📝 Observations (PQCDSM)")
if st.button("🧠 Draft with AI"):
    obs = generate_observations_ai(st.session_state); st.session_state["observations"]=obs; st.success(f"AI drafted {len(obs)} sections.")
obs = st.session_state.get("observations", [])
if obs:
    for o in obs:
        st.markdown(f"**{o.get('section','')} — {o.get('title','')}**")
        st.write(o.get("text",""))
        st.caption(f"Confidence — Measured: {o.get('measured_count',0)} | Inferred: {o.get('inferred_count',0)}")
else:
    st.info("Click 'Draft with AI' to generate observations using your current inputs and Coach Mode hints.")


# RAG grounding
helper = RAGHelper();
# If user uploaded docs earlier, index them via Data Collection page; here we just ensure store exists.
_ctx = []
for k in ('gemba_memos','photo_evidence'):
    v = st.session_state.get(k)
    if isinstance(v,list): _ctx.append(str(v))
q = 'Draft PQCDSM observations grounded in metrics and memos.'
ans = helper.answer(q, extra_context='\n'.join(_ctx))
score = eval_rag(ans.get('answer',''), '\n'.join(ans.get('source_nodes',[])))
st.session_state['rag_last_answer'] = ans.get('answer','')
st.session_state['rag_last_sources'] = ans.get('source_nodes', [])
st.session_state['rag_last_score'] = score
st.caption(f"RAG faithfulness≈{score['faithfulness']}, context precision≈{score['context_precision']}")


# --- Confidence gating ---
MIN_FAITH = float(st.session_state.get("rag_min_faithfulness", 0.70))
LOW_CONFIDENCE_RAG = score.get("faithfulness", 0) < MIN_FAITH
st.session_state["obs_low_confidence"] = LOW_CONFIDENCE_RAG
if LOW_CONFIDENCE_RAG:
    st.warning(f"RAG faithfulness {score.get('faithfulness'):.2f} < {MIN_FAITH:.2f}. Some observations may be marked low-confidence in exports.")
