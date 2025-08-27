
import streamlit as st

def compute_confidence_for_observation(text:str)->dict:
    """Heuristic: count measured metrics available vs inferred.
    Measured keys we look for in state: takt_sec, by_step, fpy_current, inventory_value, lead_time_sec.
    """
    measured_keys = ['takt_sec','by_step','fpy_current','financials_inventory','lead_time_sec','ct_bottleneck_sec']
    measured = sum(1 for k in measured_keys if st.session_state.get(k) not in (None, '', [], {}))
    inferred = max(1, 5 - measured)  # simple scale out of 5 facts
    return {'measured': measured, 'inferred': inferred}

def bulk_confidences(observations):
    if not observations: return []
    return [compute_confidence_for_observation(o if isinstance(o,str) else str(o)) for o in observations]

def draw_confidence_bar_streamlit(conf:dict, width_px=420):
    m, i = conf.get('measured',0), conf.get('inferred',0)
    tot = max(1, m+i)
    m_w = int(width_px * (m/tot)); i_w = width_px - m_w
    import streamlit as st
    st.markdown(f"""
<div style='display:flex;width:{width_px}px;height:12px;border-radius:6px;overflow:hidden;border:1px solid #e0e0e0'>
  <div style='width:{m_w}px;background:#1b9f97' title='Measured'></div>
  <div style='width:{i_w}px;background:#d0d4d9' title='Inferred'></div>
</div>
<small>Measured: {m} • Inferred: {i}</small>
""", unsafe_allow_html=True)
