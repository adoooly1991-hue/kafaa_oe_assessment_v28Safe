
import streamlit as st
import plotly.graph_objects as go

def _waterfall(title, items):
    fig = go.Figure(go.Waterfall(
        name = title,
        orientation = "v",
        measure = [it.get('measure','relative') for it in items],
        x = [it['label'] for it in items],
        text = [f"{it['value']:,.0f}" for it in items],
        y = [it['value'] for it in items]
    ))
    fig.update_layout(title=title, showlegend=False, height=360, margin=dict(l=30,r=20,t=50,b=40))
    st.plotly_chart(fig, use_container_width=True)

def waterfalls_from_state():
    savings = [
        {'label':'Now', 'value': float(st.session_state.get('pace_sums',{}).get('Now',0)), 'measure':'relative'},
        {'label':'Next', 'value': float(st.session_state.get('pace_sums',{}).get('Next',0)), 'measure':'relative'},
        {'label':'Later', 'value': float(st.session_state.get('pace_sums',{}).get('Later',0)), 'measure':'relative'},
        {'label':'Total', 'value': 0, 'measure':'total'}
    ]
    frozen = [
        {'label':'ABC-A', 'value': float(st.session_state.get('abc_A_value',0)), 'measure':'relative'},
        {'label':'ABC-B', 'value': float(st.session_state.get('abc_B_value',0)), 'measure':'relative'},
        {'label':'ABC-C', 'value': float(st.session_state.get('abc_C_value',0)), 'measure':'relative'},
        {'label':'Total', 'value': 0, 'measure':'total'}
    ]
    sales = [
        {'label':'Lost due CT>takt', 'value': float(st.session_state.get('lost_sales_ct_gap',0)), 'measure':'relative'},
        {'label':'Changeover losses', 'value': float(st.session_state.get('lost_sales_changeover',0)), 'measure':'relative'},
        {'label':'Quality losses', 'value': float(st.session_state.get('lost_sales_quality',0)), 'measure':'relative'},
        {'label':'Total', 'value': 0, 'measure':'total'}
    ]
    st.subheader("Savings (SAR/yr)"); _waterfall("Savings", savings)
    st.subheader("Frozen Cash (Inventory SAR)"); _waterfall("Frozen Cash", frozen)
    st.subheader("Sales Opportunity (SAR/yr)"); _waterfall("Sales Opportunity", sales)
