from components.boot import boot
mode = boot()

import streamlit as st
from components.vsm_draw import draw_vsm, takt_ct_bars

st.set_page_config(page_title="Auto VSM Draw", layout="wide")
st.title("🗺️ Auto-drawn Value Stream Diagram (lanes & takt vs CT)")

takt = float(st.session_state.get("takt_sec", 60))
# Build steps from session or fallback demo
steps = st.session_state.get("vsm_steps") or [
    {"name":"Receive RM","ct_sec":20,"wip":120,"mode":"push"},
    {"name":"Kitting","ct_sec":45,"wip":60,"mode":"pull"},
    {"name":"Assembly","ct_sec":85,"wip":40,"mode":"push"},
    {"name":"Test","ct_sec":50,"wip":25,"mode":"pull"},
    {"name":"Pack","ct_sec":30,"wip":30,"mode":"pull"},
]

col1,col2 = st.columns([1,1])
with col1:
    st.markdown("**Material & Information Flow** (push dashed / pull bold)")
    draw_vsm(steps)
with col2:
    st.markdown("**Takt vs Cycle Times** (bottlenecks in red)")
    takt_ct_bars(steps, takt)
