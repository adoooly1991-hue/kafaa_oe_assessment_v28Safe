from components.boot import boot
mode = boot()

import streamlit as st, json, pathlib, random, time

st.set_page_config(page_title="Seed Demo", layout="wide")
st.title("🚀 One‑click Seed Demo")

st.markdown("Populate the app with plausible demo data for a quick end‑to‑end run.")

choice = st.selectbox("Scenario", ["Manufacturing — Defense (Unmanned Systems)","Manufacturing — Metal Fabrication","Manufacturing — Electronics Assembly"], index=0)

def seed_defense():
    st.session_state.update({
        "brand_mode":"co_brand",
        "client_profile":{"name_en":"Serb Advanced Industries","logo":"assets/serb.png"},
        "client_name":"Serb Advanced Industries",
        "client_logo_path":"assets/serb.png",
        "target_profit_sar":7200000,
        "cost_reduction_target_sar":3600000,
        "revenue_sar":38500000,
        "champion_product":"VT-Alpha (Surveillance UAS)",
        "product_series":[
            {"label":"Sales Value (SAR M)","x":["Q1","Q2","Q3","Q4"],"y":[7.5,8.3,9.1,9.8]},
            {"label":"Sales Volume (Units)","x":["Q1","Q2","Q3","Q4"],"y":[18,22,25,27]},
        ],
        "tp_current":22,"tp_future":16,"tp_ideal":8,
        "lt_days_current":68,"lt_days_future":44,"lt_hrs_ideal":16,
        "va_pct_current":0.42,"va_pct_future":0.58,"va_pct_ideal":0.65,
        "takt_sec":90.0,
        "changeover_min":35,
        "fpy_current":97.6,
        "wip_total":340,
        "abc_A_value":2200000,"abc_B_value":1300000,"abc_C_value":600000,
        "lost_sales_ct_gap":5400000,"lost_sales_changeover":1250000,"lost_sales_quality":850000,
        "pace_sums":{"Now":1200000,"Next":900000,"Later":650000},
        "vsm_steps":[
            {"name":"Kitting","ct_sec":70},
            {"name":"Assembly","ct_sec":120},
            {"name":"Integration","ct_sec":95},
            {"name":"Calibration","ct_sec":80},
            {"name":"Flight Test","ct_sec":140},
        ],
        "gemba_memos":[
            "Observed 3 pallets of WIP near integration bay; safety cones in place but no FIFO tag.",
            "Two rework loops after environmental test; primary causes: cabling strain relief, IMU mounting torque."
        ],
        "observations":[
            "Significant WIP buffers between Assembly and Integration cause waiting and motion; average queue 28 units (~3.5 days).",
            "Changeover on UAS variants >35 min; lack of externalized setup tasks leads to extended downtime.",
            "First-pass-yield at environmental test ~97.6%; rework mainly connectors and fasteners."
        ],
    })

def seed_metal():
    st.session_state.update({
        "brand_mode":"kafaa",
        "client_profile":{"name_en":"MetalWorks Co.","logo":None},
        "client_name":"MetalWorks Co.",
        "target_profit_sar":4200000,"cost_reduction_target_sar":1800000,"revenue_sar":26500000,
        "champion_product":"Beam-X200",
        "product_series":[{"label":"Sales Value","x":["Q1","Q2","Q3","Q4"],"y":[5.1,5.4,5.8,6.0]}],
        "tp_current":18,"tp_future":13,"tp_ideal":6,
        "lt_days_current":52,"lt_days_future":31,"lt_hrs_ideal":12,
        "takt_sec":75.0,"changeover_min":28,"fpy_current":96.4,
        "pace_sums":{"Now":800000,"Next":600000,"Later":450000},
        "abc_A_value":1500000,"abc_B_value":900000,"abc_C_value":350000,
        "lost_sales_ct_gap":3200000,"lost_sales_changeover":700000,"lost_sales_quality":400000,
    })

def seed_electronics():
    st.session_state.update({
        "brand_mode":"kafaa",
        "client_profile":{"name_en":"Al-Nour Electronics","logo":None},
        "client_name":"Al-Nour Electronics",
        "target_profit_sar":5600000,"cost_reduction_target_sar":2500000,"revenue_sar":41000000,
        "champion_product":"SmartHub-X",
        "product_series":[{"label":"Sales Value","x":["Q1","Q2","Q3","Q4"],"y":[9.3,9.7,10.1,10.6]}],
        "tp_current":24,"tp_future":14,"tp_ideal":7,
        "lt_days_current":34,"lt_days_future":21,"lt_hrs_ideal":10,
        "takt_sec":55.0,"changeover_min":12,"fpy_current":99.0,
        "pace_sums":{"Now":1150000,"Next":900000,"Later":300000},
        "abc_A_value":1800000,"abc_B_value":700000,"abc_C_value":250000,
        "lost_sales_ct_gap":4700000,"lost_sales_changeover":350000,"lost_sales_quality":150000,
    })

col1, col2, col3 = st.columns(3)
with col1:
    if st.button("Seed now"):
        if "Defense" in choice: seed_defense()
        elif "Metal" in choice: seed_metal()
        else: seed_electronics()
        st.success("Seeded demo data into session. Go to Export to see the completeness jump.")
with col2:
    if st.button("Load SERB workspace template"):
        p = pathlib.Path("workspaces/serb_workspace.json")
        if p.exists():
            import json
            payload = json.loads(p.read_text(encoding="utf-8"))
            # minimal mapping into session for quick use
            st.session_state["brand_mode"] = payload.get("brand_mode","co_brand")
            st.session_state["client_profile"] = payload.get("client",{})
            st.session_state["client_name"] = payload.get("client",{}).get("name_en","Client")
            st.session_state["client_logo_path"] = payload.get("client",{}).get("logo")
            f = payload.get("financials",{})
            st.session_state["target_profit_sar"] = f.get("target_profit_sar",0)
            st.session_state["cost_reduction_target_sar"] = f.get("cost_reduction_target_sar",0)
            st.session_state["revenue_sar"] = f.get("revenue_sar",0)
            sel = payload.get("product_selection",{})
            st.session_state["champion_product"] = sel.get("champion","—")
            st.session_state["product_series"] = sel.get("series",[])
            v = payload.get("vsm",{})
            st.session_state["tp_current"] = v.get("current",{}).get("touch_points",0)
            st.session_state["tp_future"] = v.get("future",{}).get("touch_points",0)
            st.session_state["tp_ideal"] = v.get("ideal",{}).get("touch_points",0)
            st.session_state["lt_days_current"] = v.get("current",{}).get("lead_time_days",0)
            st.session_state["lt_days_future"] = v.get("future",{}).get("lead_time_days",0)
            st.session_state["lt_hrs_ideal"] = v.get("ideal",{}).get("lead_time_hrs",0)
            st.success("Loaded SERB workspace into the session.")
        else:
            st.error("serb_workspace.json not found.")
with col3:
    if st.button("Clear seeded data"):
        keys = list(st.session_state.keys())
        for k in keys:
            if any(x in k for x in ["target_profit","cost_reduction","revenue_sar","champion_product","product_series","tp_","lt_","va_pct","takt_sec","changeover_min","fpy_current","abc_","lost_sales","pace_sums","vsm_steps","gemba_memos","observations","client_"]):
                st.session_state.pop(k, None)
        st.warning("Cleared seeded keys from session.")
