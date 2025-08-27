from components.boot import boot
mode = boot()

import streamlit as st, plotly.graph_objects as go
from components.roi_bridge import rollup_impact, series_to_waterfall_data
st.set_page_config(page_title="Impact", layout="wide")
st.title("💥 Impact — Waterfalls")
data = rollup_impact(st.session_state)
cols = st.columns(3)
def draw(items, title):
    if not items:
        st.info(f"Add data/actions to compute: {title}."); return
    x,y,m = series_to_waterfall_data(items)
    fig = go.Figure(go.Waterfall(x=x, y=y, measure=m))
    fig.update_layout(title=title, height=360, margin=dict(l=8,r=8,t=40,b=8))
    st.plotly_chart(fig, use_container_width=True)
with cols[0]: draw(data.get("savings_items"), "Savings (SAR/yr)")
with cols[1]: draw(data.get("frozen_cash_items"), "Frozen Cash (SAR)")
with cols[2]: draw(data.get("sales_oppty_items"), "Sales Opportunity (SAR/yr)")
