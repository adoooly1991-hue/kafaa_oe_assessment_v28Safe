from components.boot import boot
mode = boot()

import streamlit as st
from components.coach_agent import recommend_with_trace
from components.vsm_draw import takt_ct_bars

st.set_page_config(page_title="Coach — Why these?", layout="wide")
st.title("🧭 Coach — Why these recommendations?")

# Build dummy steps from state
steps = st.session_state.get("vsm_steps") or [
    {"name":"Kitting","ct_sec":45},
    {"name":"Assembly","ct_sec":85},
    {"name":"Test","ct_sec":50}
]

recs = recommend_with_trace(steps)
for r in recs:
    st.markdown(f"**{r['action']}**  
<small>{r['because']}</small>  
`{', '.join(r['tags'])}`", unsafe_allow_html=True)
st.caption("Coach justifies each action with current takt/CT, changeover, FPY, and WIP where available.")

st.markdown("### Visual — Takt vs CT")
takt = float(st.session_state.get("takt_sec", 60.0))
from components.vsm_draw import takt_ct_bars
takt_ct_bars(steps, takt)
