
import streamlit as st
from components.obs_conf import draw_confidence_bar_streamlit, compute_confidence_for_observation

def approvals_panel():
    st.header("Reviewer — Approvals")
    obs_list = st.session_state.get("observations", []) or []
    appr = st.session_state.get("approvals", {})
    for i, obs in enumerate(obs_list):
        st.markdown(f"**Observation {i+1}**")
        draw_confidence_bar_streamlit(compute_confidence_for_observation(obs))
        key = f"approve_{i}"
        prev = appr.get(str(i))
        choice = st.radio("Decision", ["Pending","Approve","Request changes"], index=["Pending","Approve","Request changes"].index(prev) if prev in ["Pending","Approve","Request changes"] else 0, key=key)
        comment = st.text_area("Comment", value=appr.get(f"comment_{i}",""), key=f"comment_{i}")
        if st.button(f"Save decision {i+1}"):
            appr[str(i)] = choice
            appr[f"comment_{i}"] = comment
            st.session_state["approvals"] = appr
            st.success("Saved.")

def reviewer_header():
    if st.session_state.get("app_mode") == "Reviewer":
        st.info("Reviewer Mode: slide notes and confidence flags are prioritized. Use the Approvals page to lock decisions.")
