
import streamlit as st
st.title("Kafaa OE Assessment Platform")
st.caption("Start with the Guided Tour or open a saved workspace. Use Reviewer mode for approvals.")
st.page_link("pages/00i_👋_Guided_Tour.py", label="Start Guided Tour ➜")
st.page_link("pages/00j_🏠_Home_Gallery.py", label="Open Home Gallery ➜")

from components.boot import boot
mode = boot()

import streamlit as st
from PIL import Image
import os, json
from components.persist import import_session
st.set_page_config(page_title="Kafaa OE — Assessment", page_icon="✅", layout="wide")
try:
    st.logo(Image.open("assets/kafaa_logo.png"))
except Exception:
    pass
st.markdown("### OE Assessment Report Generator — v26.4")
st.caption("Universal app — AI Observations, AI Countermeasures, Coach Mode, Impact waterfalls, Vision evidence, RAG, PPTX & PDF exports.")

# Auto-load last workspace once per session
try:
    if not st.session_state.get("_loaded_last_workspace"):
        if os.path.exists("data/.last_workspace"):
            last = open("data/.last_workspace","r",encoding="utf-8").read().strip()
            if last and os.path.exists(os.path.join("data", last)):
                payload = json.load(open(os.path.join("data", last),"r",encoding="utf-8"))
                import_session(st.session_state, payload)
                st.session_state["last_workspace"]=last
                st.toast(f"Auto-loaded workspace: {last}")
        st.session_state["_loaded_last_workspace"]=True
except Exception as e:
    pass


with st.sidebar:
    st.header("Setup")
    st.session_state["factory_name"] = st.text_input("Factory name", st.session_state.get("factory_name","Your Factory"))
    st.session_state["year"] = st.number_input("Assessment year", value=int(st.session_state.get("year", 2025)))
    # Workspace quick-load
    files = [f for f in os.listdir("data") if f.endswith(".json")]
    if files:
        pick = st.selectbox("Load workspace", files, index=files.index(st.session_state.get("last_workspace","")) if st.session_state.get("last_workspace","") in files else 0)
        if st.button("📥 Load workspace"):
            with open(os.path.join("data", pick), "r", encoding="utf-8") as f:
                payload = json.load(f)
            import_session(st.session_state, payload)
            st.session_state["last_workspace"] = pick
            with open("data/.last_workspace","w",encoding="utf-8") as f2: f2.write(pick)
            st.success(f"Loaded {pick}")
    # Industry profile selector
    import glob
    prof_files = sorted([Path(p).stem for p in glob.glob("benchmarks/*.yml")])
    current = st.session_state.get("profile_key","default")
    st.session_state["profile_key"] = st.selectbox("Industry benchmark profile", prof_files, index=prof_files.index(current) if current in prof_files else 0, help="Sets targets for FPY, changeover, OTD, etc. Coach Mode uses this.")

st.markdown('<style>div.block-container{padding-top:1rem;} .stTabs [data-baseweb=tab]{font-weight:600}</style>', unsafe_allow_html=True)
# KPI mini-cards
def _pick_kpis(ss):
    takt = ss.get("takt_sec")
    if not takt:
        shift = ss.get("shift_sec") or 8*3600
        demand = ss.get("demand_per_shift")
        if demand:
            takt = shift/float(demand)
    ct = None
    if ss.get("ct_table"):
        try: ct = max([r.get("ct",0) for r in ss.get("ct_table")])
        except Exception: pass
    if not ct:
        prod = ss.get("coach_mode_results",{}).get("production",{}).get("answers",{})
        ct = prod.get("ct_bn")
    prod = ss.get("coach_mode_results",{}).get("production",{}).get("answers",{})
    fpy = prod.get("fpy_line") if isinstance(prod, dict) else None
    inv = ss.get("financials_inventory") or 0
    rate = ss.get("carrying_rate_pct") or 25
    carrying = inv * (float(rate)/100.0)
    return {"takt": takt, "ct_bn": ct, "fpy": fpy, "carrying": carrying}
st.markdown("#### Key KPIs (live)")
k = _pick_kpis(st.session_state)
c1,c2,c3,c4 = st.columns(4)
with c1: st.metric("Takt (sec)", f"{k.get('takt'):.1f}" if k.get('takt') else "—")
with c2: st.metric("Bottleneck CT (sec)", f"{k.get('ct_bn'):.1f}" if k.get('ct_bn') else "—")
with c3: st.metric("FPY (%)", f"{k.get('fpy'):.1f}" if k.get('fpy') else "—")
with c4: st.metric("Carrying Cost (SAR/yr)", f"{k.get('carrying'):,.0f}")

# --- Storytelling Hero ---
import plotly.graph_objects as go
def _step_done():
    steps = {
        "Financials": bool(st.session_state.get("financials_revenue")),
        "Champion": bool(st.session_state.get("champion_product")),
        "Coach": bool(st.session_state.get("coach_mode_results")),
        "Observations": bool(st.session_state.get("observations")),
        "Countermeasures": bool(st.session_state.get("countermeasures_df")),
        "Impact": bool(st.session_state.get("countermeasures") or st.session_state.get("financials_inventory")),
        "Export": False
    }
    return steps
steps = _step_done()
done = sum(1 for v in steps.values() if v)
total = len(steps)
fig = go.Figure(data=[go.Pie(values=[done, max(0,total-done)], labels=["Done","To go"], hole=.7, textinfo="none")])
fig.update_layout(height=220, margin=dict(l=0,r=0,t=0,b=0), showlegend=False, annotations=[dict(text=f"{int(done/total*100)}%", x=0.5, y=0.5, font_size=22, showarrow=False)])
cc1, cc2 = st.columns([1,3])
with cc1:
    st.plotly_chart(fig, use_container_width=True)
with cc2:
    st.markdown("#### Your journey")
    check = lambda b: "✅" if b else "⬜️"
    st.write(" • " + "  
 • ".join([f"{check(v)} {k}" for k,v in steps.items()]))
    # Next step CTA
    next_page = None
    order = [("Financials","pages/01a_📥_Financials.py"), ("Champion","pages/01b_📦_Product_Selection.py"), ("Coach","pages/02a_🧭_Coach_Mode_Value_Chain.py"),
             ("Observations","pages/06a_📝_Observations.py"), ("Countermeasures","pages/07a_🗂️_Countermeasures.py"),
             ("Impact","pages/03a_💥_Impact.py"), ("Export","pages/08a_📤_Export.py")]
    for k,link in order:
        if not steps[k]:
            next_page = link; break
    if next_page:
        st.page_link(next_page, label="→ Continue to next step", icon="➡️")
    else:
        st.success("All steps ready. Head to Export!")
st.divider()


# --- Assessment Journey (guided) ---
st.markdown("### Assessment Journey — follow these steps")
steps_info = [
    {"name":"Data Collection", "done": bool(st.session_state.get("financials_revenue") or st.session_state.get("product_table") or st.session_state.get("rag")), "link":"pages/01a_📥_Financials.py", "desc":"Collect financials, takt inputs; optionally add docs/photos."},
    {"name":"Financial Assessment", "done": bool(st.session_state.get("cost_reduction_target_sar")), "link":"pages/01a_📥_Financials.py", "desc":"Compute Cost Reduction target, cash ratios, inventory turns target."},
    {"name":"Product Selection", "done": bool(st.session_state.get("champion_product")), "link":"pages/01b_📦_Product_Selection.py", "desc":"Pick Champion product with weighted scoring & risk flags."},
    {"name":"VSM Charter", "done": bool(st.session_state.get("charter_objectives") or st.session_state.get("champion_product")), "link":"pages/04a_🧾_VSM_Charter.py", "desc":"Document scope, targets, and champion for sign-off."},
    {"name":"VSM Workshop (Value Chain)", "done": bool(st.session_state.get("coach_mode_results")), "link":"pages/02a_🧭_Coach_Mode_Value_Chain.py", "desc":"Guided questionnaire with benchmarks & follow-ups."},
    {"name":"Observation Generation", "done": bool(st.session_state.get("observations")), "link":"pages/06a_📝_Observations.py", "desc":"AI co-authors Gemba-style PQCDSM observations."},
    {"name":"Quantification", "done": bool(st.session_state.get("countermeasures") or st.session_state.get("financials_inventory")), "link":"pages/03a_💥_Impact.py", "desc":"Waterfalls for Savings, Frozen Cash, Sales Opportunity."},
    {"name":"Export Full Report", "done": False, "link":"pages/08a_📤_Export.py", "desc":"PPTX/PDF with branding, Charter, observations, actions, and evidence."}
]
cols = st.columns(4)
for i, s in enumerate(steps_info):
    with cols[i%4]:
        st.metric(s["name"], "✅ Done" if s["done"] else "⬜️ Pending")
        st.caption(s["desc"])
        st.page_link(s["link"], label="Open", icon="➡️")
st.divider()
