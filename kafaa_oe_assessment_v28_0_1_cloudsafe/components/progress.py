
import streamlit as st

CORE_STEPS = [
    ("Data Collection", ["target_profit_sar","revenue_sar"]),
    ("Financial Assessment", ["cost_reduction_target_sar"]),
    ("Product Selection", ["champion_product"]),
    ("VSM Charter", ["tp_current","tp_future","lt_days_current","lt_days_future"]),
    ("Value Chain / Assessment", ["takt_sec","fpy_current"]),
    ("Observations", ["observations"]),
    ("Quantification", ["pace_sums","abc_A_value","lost_sales_ct_gap"]),
    ("Export", []),
]

def check_step(keys):
    done = 0
    for k in keys:
        v = st.session_state.get(k, None)
        if v not in (None, "", [], {}, 0, 0.0): done += 1
    return done, len(keys)

def compute_progress():
    rows = []
    total_w = 0; have = 0
    for name, keys in CORE_STEPS:
        d, t = check_step(keys)
        # weight each step equally but allow empty keys
        w = max(1, len(keys))  # weight
        total_w += w; have += d if t>0 else 1  # treat empty step as done baseline
        pct = (d / t) if t else 1.0
        rows.append({"step": name, "done": d, "total": t, "pct": pct})
    overall = have / total_w if total_w else 1.0
    return overall, rows
