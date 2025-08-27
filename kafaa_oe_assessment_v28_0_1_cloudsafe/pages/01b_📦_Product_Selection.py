from components.boot import boot
mode = boot()

import streamlit as st, pandas as pd, numpy as np
st.set_page_config(page_title="Champion Product", layout="wide")
st.title("🏆 Champion Product Selection")
st.caption("Paste or load a product table and rank with weighted criteria. Highest score becomes the Champion for VSM.")

with st.expander("How scoring works"):
    st.markdown("""
    We normalize each numeric column 0–1 and apply your weights. **Higher is better** for Margin and Sales; **Lower is better** for Manufacturing Time and Touch Points (we invert those).
    Defaults: Margin 35%, Sales 35%, Mfg Time 15% (inverted), Touch Points 15% (inverted).
    """)

df = st.session_state.get("product_table")
if df is None:
    st.info("Paste a CSV-style table below (headers required).")
    txt = st.text_area("CSV", value="Product,CostPerUnit,ProfitPerUnit,MarginPerUnit,TotalSales,Quantity,ManufacturingTimeHr,TouchPoints\nA,50,20,20,500000,10000,0.5,6\nB,80,30,30,900000,15000,0.7,8")
    if st.button("Load table"):
        from io import StringIO
        df = pd.read_csv(StringIO(txt)); st.session_state["product_table"]=df
else:
    st.dataframe(df, use_container_width=True, height=240)

if df is not None:
    st.subheader("Weights")
    c1,c2,c3,c4 = st.columns(4)
    w_margin = c1.slider("Margin / unit", 0, 100, 35)
    w_sales = c2.slider("Sales (SAR)", 0, 100, 35)
    w_time = c3.slider("Mfg time (lower is better)", 0, 100, 15)
    w_touch = c4.slider("Touch points (lower is better)", 0, 100, 15)

    numeric_cols = df.select_dtypes(include="number").columns
    eps = 1e-9
    norm = (df[numeric_cols]-df[numeric_cols].min())/(df[numeric_cols].max()-df[numeric_cols].min()+eps)

    def get(col): return norm.get(col, pd.Series([0]*len(df)))
    inv_time = 1 - get("ManufacturingTimeHr")
    inv_touch = 1 - get("TouchPoints")

    score = (get("MarginPerUnit")*(w_margin/100.0) +
             get("TotalSales")*(w_sales/100.0) +
             inv_time*(w_time/100.0) +
             inv_touch*(w_touch/100.0))

    out = df.copy(); out["ChampionScore"]=score.round(3); out = out.sort_values("ChampionScore", ascending=False)
    st.subheader("Ranking")
    st.dataframe(out, use_container_width=True)

    # Save top picks
    picks = list(out["Product"] if "Product" in out.columns else out.index.astype(str))
    st.session_state["champion_product"] = picks[0] if picks else None
    st.session_state["champion_alt2"] = picks[1] if len(picks)>1 else None
    st.session_state["champion_alt3"] = picks[2] if len(picks)>2 else None
    st.success(f"Champion: {st.session_state['champion_product']} | 2nd: {st.session_state.get('champion_alt2')} | 3rd: {st.session_state.get('champion_alt3')}")


# Champion risk flags
from components.bench import load_profile
prof = load_profile("default")
bench_fpy = prof.get("kpis",{}).get("fpy_best_practice_pct", 98)
changeover_best = prof.get("kpis",{}).get("changeover_best_min", 10)
prod = st.session_state.get("coach_mode_results",{}).get("production",{}).get("answers",{})
ct_bn = prod.get("ct_bn"); takt = prod.get("takt"); fpy = prod.get("fpy_line"); chg = prod.get("changeover_min", st.session_state.get("changeover_min"))
warns = []
if ct_bn and takt and ct_bn>takt: warns.append(f"Bottleneck CT ({ct_bn}s) exceeds takt ({takt}s) → flow risk.")
if fpy and fpy < bench_fpy: warns.append(f"FPY {fpy}% is below best-practice {bench_fpy}% → quality risk.")
if chg and changeover_best and chg > 3*changeover_best: warns.append(f"Changeover {chg} min is high vs best {changeover_best} min → SMED opportunity.")
if warns:
    st.warning("Champion risk flags:\n- " + "\n- ".join(warns))

from components.audit import log

if st.session_state.get('champion_product') and not st.session_state.get('_champion_logged'):
    log("Champion set", {"product": st.session_state['champion_product']})
    st.session_state['_champion_logged']=True

from components.heatmap_util import generate_and_store_heatmap
_generate_heat = True
try:
    generate_and_store_heatmap()
except Exception:
    pass
