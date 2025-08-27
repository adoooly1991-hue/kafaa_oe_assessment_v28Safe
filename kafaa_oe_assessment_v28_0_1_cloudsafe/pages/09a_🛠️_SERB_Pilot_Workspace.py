from components.boot import boot
mode = boot()

import streamlit as st, os, json
st.set_page_config(page_title="SERB Pilot Workspace", layout="wide")
st.title("🛠️ SERB Pilot Workspace")

st.caption("This is a client-specific launcher. **Branding remains Kafaa** across the app; exports co-brand by placing SERB as a secondary mark.")

path = "data/Serb_Advanced_Industries_Unmanned_Pilot.json"
col1, col2 = st.columns([1,3])
with col1:
    if st.button("📥 Load SERB workspace", use_container_width=True):
        if os.path.exists(path):
            payload = json.load(open(path,"r",encoding="utf-8"))
            for k,v in payload.items(): st.session_state[k]=v
            st.session_state['last_workspace'] = os.path.basename(path)
            open("data/.last_workspace","w",encoding="utf-8").write(os.path.basename(path))
            st.success("Loaded SERB workspace and set as default.")
        else:
            st.error("Workspace JSON not found.")
with col2:
    st.info("After loading, visit **Home** → Assessment Journey or go straight to **Exports** to view co-branded output.")

# Quick glance metrics if loaded
if st.session_state.get("financials_revenue"):
    st.markdown("### Snapshot")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Revenue", f"{st.session_state['financials_revenue']:,.0f} SAR")
    crt = st.session_state.get("cost_reduction_target_sar")
    c2.metric("Cost Reduction Target", f"{crt:,.0f} SAR" if crt else "—" )
    c3.metric("Inventory", f"{st.session_state.get('financials_inventory',0):,.0f} SAR" )
    c4.metric("Champion", st.session_state.get("champion_product","—"))
