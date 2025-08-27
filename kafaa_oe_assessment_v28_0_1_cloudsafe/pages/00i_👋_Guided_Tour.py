from components.boot import boot
mode = boot()

import streamlit as st
from components.progress import compute_progress, CORE_STEPS

st.set_page_config(page_title="Guided Tour", layout="wide")
st.title("👋 Guided Tour")

st.caption("Follow the steps below. We’ll track your progress and take you to the next missing item.")

overall, rows = compute_progress()
st.progress(overall)
st.write(f"Overall progress: **{int(overall*100)}%**")

def _link_for(step_name):
    # Best-effort mapping to pages
    mapping = {
        "Data Collection": "pages/01a_📥_Data_Collection.py",
        "Financial Assessment": "pages/02a_💰_Financial_Assessment.py",
        "Product Selection": "pages/03a_🏆_Product_Selection.py",
        "VSM Charter": "pages/03b_📝_VSM_Charter.py",
        "Value Chain / Assessment": "pages/04a_🔍_Value_Chain_Assessment.py",
        "Observations": "pages/05a_🧠_Observations.py",
        "Quantification": "pages/07a_📊_Quantification.py",
        "Export": "pages/08a_📤_Export.py",
    }
    return mapping.get(step_name, "pages/08a_📤_Export.py")

for r in rows:
    pct = int(r["pct"]*100)
    with st.expander(f"{r['step']} — {pct}%"):
        st.write(f"Keys complete: {r['done']} / {r['total']}")
        st.page_link(_link_for(r["step"]), label=f"Go to {r['step']}")

# Smart next-step button
incomplete = [r for r in rows if r["pct"] < 1.0]
if incomplete:
    nxt = incomplete[0]["step"]
    st.success(f"Next recommended step: {nxt}")
    st.page_link(_link_for(nxt), label=f"Go to {nxt} ➜")
else:
    st.balloons()
    st.success("All steps complete! Proceed to Export.")
    st.page_link("pages/08a_📤_Export.py", label="Go to Export ➜")
