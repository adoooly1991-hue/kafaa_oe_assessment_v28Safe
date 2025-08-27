import streamlit as st
from components.boot import boot

st.set_page_config(page_title="Kafaa OE Assessment", layout="wide")
mode = boot()

st.title("Kafaa OE Assessment Platform")
st.caption("Start with the Guided Tour or open a saved workspace. Use Reviewer mode for approvals.")

# Quick entry points
st.page_link("pages/00i_👋_Guided_Tour.py", label="Start Guided Tour ➜")
st.page_link("pages/00j_🏠_Home_Gallery.py", label="Open Home Gallery ➜")
st.page_link("pages/00h_🗂️_Workspace_Manager.py", label="Workspace Manager ➜")
st.page_link("pages/08a_📤_Export.py", label="Export ➜")

st.markdown("---")
st.subheader("What to expect")

steps = [
    "01a — Data Collection (inputs & uploads)",
    "02a — Financial Assessment (targets & cash ratios)",
    "03a — Product Selection (champion product)",
    "03b — VSM Charter (scope & goals)",
    "04a — Value Chain Assessment (benchmarks & follow-ups)",
    "05a — Observations (PQCDSM with confidence)",
    "07a — Quantification (savings, frozen cash, opportunity)",
    "08a — Export (full PPTX/PDF, brand modes, appendix)"
]
for s in steps:
    st.write(f"• {s}")
