from components.boot import boot
mode = boot()

import streamlit as st, os, tempfile, pandas as pd, numpy as np
st.set_page_config(page_title="Client & Project", layout="wide")
st.title("👤 Client & Project — branding & seed demo")

col1,col2 = st.columns([2,1])
with col1:
    st.session_state["client_name"] = st.text_input("Client name", st.session_state.get("client_name","Serb Advanced Industries"))
    st.session_state["project_name"] = st.text_input("Project name", st.session_state.get("project_name","Unmanned Systems Value Stream"))
with col2:
    upl = st.file_uploader("Client logo (PNG/JPG)", type=["png","jpg","jpeg"])
    if upl:
        import tempfile, os
        tmp = tempfile.mkdtemp(); path = os.path.join(tmp, upl.name)
        with open(path,"wb") as f: f.write(upl.getbuffer())
        st.session_state["client_logo_path"]=path
    if st.session_state.get("client_logo_path"):
        st.image(st.session_state["client_logo_path"], caption="Current client logo", width=200)

st.divider()
st.subheader("Seed demo")
st.caption("Loads realistic sample data across Financials, Product Selection, Coach Mode hints, Observations, Countermeasures + a few photos.")
if st.button("Load seed demo"):
    # Financials
    st.session_state.update({
        "factory_name":"Kafaa Demo Plant",
        "year":2025,
        "financials_revenue": 48_000_000.0,
        "financials_cogs": 31_500_000.0,
        "financials_ga": 6_200_000.0,
        "financials_dep": 2_100_000.0,
        "financials_finexp": 1_100_000.0,
        "financials_inventory": 9_500_000.0,
        "current_assets": 18_000_000.0,
        "current_liabilities": 9_200_000.0,
        "sales_target": 55_000_000.0,
        "bud_cogs": 30_000_000.0,
        "bud_ga": 6_000_000.0,
        "bud_dep": 2_000_000.0,
        "bud_finexp": 1_000_000.0,
        "target_profit": 7_500_000.0,
        "carrying_rate_pct": 24.0,
        "shift_sec": 8*3600,
        "demand_per_shift": 480,
        "takt_sec": (8*3600)/480,
        # ABC splits
        "abc_A_pct": 50.0, "abc_B_pct": 30.0, "abc_C_pct": 20.0,
        "abc_A_carry_pct": 20.0, "abc_B_carry_pct": 25.0, "abc_C_carry_pct": 28.0
    })
    # Product table
    import pandas as pd
    df = pd.DataFrame({
        "Product":["Recon Drone","Gimbal","Battery Pack","Control Unit","Airframe"],
        "CostPerUnit":[4200, 1600, 450, 2800, 3800],
        "ProfitPerUnit":[1300, 700, 160, 900, 1100],
        "MarginPerUnit":[1300,700,160,900,1100],
        "TotalSales":[9_800_000, 6_200_000, 3_900_000, 8_400_000, 7_600_000],
        "Quantity":[1700, 3200, 8000, 2100, 1900],
        "ManufacturingTimeHr":[3.8, 1.2, 0.6, 2.6, 3.2],
        "TouchPoints":[12, 8, 6, 10, 14]
    })
    st.session_state["product_table"]=df
    st.session_state["champion_product"]="Recon Drone"
    # Coach Mode minimal answers (bottleneck, fpy)
    st.session_state.setdefault("coach_mode_results",{})
    st.session_state["coach_mode_results"]["production"]={"title":"Production","answers":{"ct_bn":75,"takt":60,"fpy_line":95}}
    st.session_state["ct_table"]=[{"step":"Machining","ct":55},{"step":"Assembly","ct":75},{"step":"Test","ct":65}]
    # Observations (seeded text)
    st.session_state["observations"]=[
        {"section":"Production","title":"Flow and bottlenecks","text":"Material travels through machining→assembly→test with frequent stops. Assembly is the pacemaker at 75s CT vs 60s takt creating WIP buffers before test.", "measured_count":3, "inferred_count":2},
        {"section":"Quality","title":"FPY & rework","text":"Line FPY averages 95% with top defects in wiring continuity and gimbal alignment. Rework averages 42 min / unit, ~2 operators.", "measured_count":2, "inferred_count":2},
        {"section":"Cost","title":"Inventory & carrying","text":"Inventory is SAR 9.5M with 24% carrying (~SAR 2.28M/yr). ABC mix skews to A (50%) indicating high-value immobilized cash.", "measured_count":2, "inferred_count":1}
    ]
    # Countermeasures (seeded plan)
    import pandas as pd
    cm = pd.DataFrame([
        {"title":"SMED on assembly changeover","owner":"Ops","due":"2025-10-30","impact":80,"effort":45,"annual_savings_sar":1_200_000},
        {"title":"Kanban + supermarkets for kitting","owner":"Supply","due":"2025-09-15","impact":65,"effort":30,"annual_savings_sar":600_000},
        {"title":"Mistake-proofing on wiring station","owner":"Quality","due":"2025-08-31","impact":55,"effort":25,"annual_savings_sar":350_000}
    ])
    st.session_state["countermeasures_df"]=cm
    st.session_state["countermeasures"]=cm.to_dict("records")
    # Vision evidence (placeholder images created in assets)
    import tempfile, os
    st.success("Seed demo loaded. Go to Financials ▶ Product ▶ Coach ▶ Observations ▶ Countermeasures ▶ Impact ▶ Exports.")

from components.heatmap_util import generate_and_store_heatmap
_generate_heat = True
try:
    generate_and_store_heatmap()
except Exception:
    pass
