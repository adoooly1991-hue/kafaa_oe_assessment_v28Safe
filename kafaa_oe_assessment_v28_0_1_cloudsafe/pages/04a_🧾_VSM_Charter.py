from components.boot import boot
mode = boot()

import streamlit as st
from components.audit import log, pandas as pd
st.set_page_config(page_title="VSM Charter", layout="wide")
st.title("🧾 VSM Charter — auto-filled targets")

factory = st.session_state.get("factory_name","Factory")
year = st.session_state.get("year","")
champ = st.session_state.get("champion_product")
crt = st.session_state.get("cost_reduction_target_sar")
inv_red = st.session_state.get("inv_reduction_target_sar")
quick = st.session_state.get("quick_ratio")
curr = st.session_state.get("current_ratio")

st.markdown(f"**Factory:** {factory}    **Year:** {year}    **Champion Product:** {champ or '—'}")

col1,col2 = st.columns(2)
with col1:
    st.metric("Cost Reduction Target (SAR)", f"{(crt or 0):,.0f}")
    st.metric("Inventory Reduction Target (SAR)", f"{(inv_red or 0):,.0f}")
with col2:
    st.metric("Quick Ratio (≈ cash focus)", f"{quick:.2f}" if quick is not None else "—")
    st.metric("Current Ratio", f"{curr:.2f}" if curr is not None else "—")

st.divider()
st.subheader("Scope & Objectives")
scope = st.text_area("Scope (value stream / process family)", value=st.session_state.get("charter_scope",""))
obj = st.text_area("Objectives (measurable goals)", value=st.session_state.get("charter_objectives","Reduce lead time by 30%, Cut WIP by 40%, Increase FPY to ≥98%"))
st.session_state["charter_scope"]=scope
st.session_state["charter_objectives"]=obj

st.info("These charter metrics are injected into the PPTX/PDF exports automatically.")
