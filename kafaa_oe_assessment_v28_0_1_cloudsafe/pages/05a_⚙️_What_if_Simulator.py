from components.boot import boot
mode = boot()

import streamlit as st
st.set_page_config(page_title="What-if", layout="wide")
st.title("⚙️ What‑if Simulator (analytic)")
with st.form("sim"):
    demand_per_shift = st.number_input("Demand per shift (units)", value= st.session_state.get("demand_per_shift", 500))
    steps = st.number_input("Number of steps", value= int(st.session_state.get("sim_steps", 5)))
    ct = st.text_area("Cycle times per step (sec, comma separated)", value= st.session_state.get("sim_cts","60,55,70,58,62"))
    fpy = st.slider("FPY (%)", 70, 100, int(st.session_state.get("sim_fpy",96)))
    takt = st.number_input("Takt time (sec)", value= float(st.session_state.get("takt_sec",60)))
    submitted = st.form_submit_button("Run")
if submitted:
    cts = [float(x.strip()) for x in ct.split(",") if x.strip()]
    bn = max(cts) if cts else 0
    shift_sec = st.session_state.get("shift_sec", 8*3600)
    out_rate_bn = shift_sec / bn if bn else 0
    out_rate_takt = shift_sec / takt if takt else 0
    tp_units = min(out_rate_bn, out_rate_takt) * (fpy/100.0)
    res = {"throughput_units": round(tp_units,1), "bottleneck_ct": bn, "lead_time_proxy_sec": round(sum(cts),1), "utilization_pct": [round((c/takt)*100,1) for c in cts]}
    st.session_state["sim_result"]=res; st.success(f"Throughput ≈ {res['throughput_units']} units/shift; Bottleneck CT = {res['bottleneck_ct']}s"); st.write(res)
from components.ai_client import chat
sim = st.session_state.get("sim_result")
if sim and st.button("💡 Explain with AI"):
    ans = chat([{"role":"system","content":"Be a Lean coach; be clear and actionable."},
                {"role":"user","content": f"Explain these simulation outputs. DATA: {sim}"}])
    st.write(ans)

from components.heatmap_util import generate_and_store_heatmap
_generate_heat = True
try:
    generate_and_store_heatmap()
except Exception:
    pass
