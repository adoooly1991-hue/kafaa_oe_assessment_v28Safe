from components.boot import boot
mode = boot()

import streamlit as st
from components.audit import log, pandas as pd
from components.ai_actions import generate_actions_ai
st.set_page_config(page_title="Countermeasures", layout="wide")
st.title("🗂️ Countermeasures")
if st.button("🛠️ Propose with AI"):
    acts = generate_actions_ai(st.session_state); st.session_state["ai_actions_staged"]=acts; st.success("Generated proposals (staged). Edit or copy into your plan.")
if "ai_actions_staged" in st.session_state:
    st.subheader("Staged proposals"); import pandas as pd; st.dataframe(pd.DataFrame(st.session_state["ai_actions_staged"]), use_container_width=True)
st.subheader("Master action plan")\nst.caption("PACE auto-tags: Now (high impact/low effort), Next (high/high or med/med), Later (low impact or high effort). Totals roll up against the Cost Reduction Target.")
df = st.session_state.get("countermeasures_df")
if df is None: df = pd.DataFrame(columns=["title","owner","due","impact","effort","annual_savings_sar"])
edited = st.data_editor(df, use_container_width=True, num_rows="dynamic")
st.session_state["countermeasures_df"]=edited
st.session_state["countermeasures"] = edited.to_dict("records")


st.markdown("—")
st.subheader("PACE summary vs. Cost Reduction Target")
import math
def tag_pace(row):
    imp = float(row.get("impact") or 0); eff = float(row.get("effort") or 0)
    if imp>=70 and eff<=40: return "Now"
    if imp>=60 and eff<=70: return "Next"
    return "Later"
df = st.session_state.get("countermeasures_df")
if df is not None and not df.empty:
    tmp = df.copy()
    tmp["PACE"] = tmp.apply(tag_pace, axis=1)
    sums = tmp.groupby("PACE")["annual_savings_sar"].sum().to_dict()
    target = float(st.session_state.get("cost_reduction_target_sar") or 0.0)
    now = float(sums.get("Now",0.0)); nxt=float(sums.get("Next",0.0)); lat=float(sums.get("Later",0.0))
    colx,coly,colz = st.columns(3)
    with colx: st.metric("Now savings (SAR/yr)", f"{now:,.0f}")
    with coly: st.metric("Next savings (SAR/yr)", f"{nxt:,.0f}")
    with colz: st.metric("Later savings (SAR/yr)", f"{lat:,.0f}")
    st.progress(min(1.0, (now+nxt)/target if target else 0.0), text=f"Coverage vs target: {( (now+nxt)/target*100 if target else 0):.1f}%")
    st.session_state["pace_sums"]=sums
else:
    st.info("Add actions to see PACE rollup.")
