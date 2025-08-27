
import streamlit as st, os, io
from typing import List, Dict
def draw_vsm(steps: List[dict]):
    """Render a simple VSM lane with push/pull icons.
    steps: [{'name':..., 'ct_sec':..., 'wip':..., 'mode':'push|pull'}]
    """
    import graphviz as gv
    dot = gv.Digraph(graph_attr={'rankdir':'LR','splines':'spline'})
    for i, s in enumerate(steps):
        label = f"{s.get('name','Step')}\nCT: {s.get('ct_sec','?')}s\nWIP: {s.get('wip','?')}"
        dot.node(f"n{i}", label, shape='record', style='rounded,filled', fillcolor='#F2FAF9')
        if i>0:
            style = 'dashed' if s.get('mode','push')=='push' else 'bold'
            label = 'PUSH' if s.get('mode','push')=='push' else 'PULL'
            dot.edge(f"n{i-1}", f"n{i}", label=label, style=style, color='#117B77')
    st.graphviz_chart(dot)

def takt_ct_bars(steps: List[dict], takt_sec: float):
    import plotly.graph_objects as go
    x = [s['name'] for s in steps]
    ct = [float(s.get('ct_sec',0)) for s in steps]
    colors = ['crimson' if c>takt_sec else '#117B77' for c in ct]
    fig = go.Figure()
    fig.add_trace(go.Bar(x=x, y=ct, name='CT (s)', marker_color=colors))
    fig.add_hline(y=takt_sec, line_dash='dash', annotation_text=f"Takt {takt_sec:.1f}s", annotation_position='top left')
    fig.update_layout(height=380, margin=dict(l=30,r=20,t=50,b=40))
    st.plotly_chart(fig, use_container_width=True)
