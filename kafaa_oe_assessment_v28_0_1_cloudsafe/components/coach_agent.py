
import streamlit as st

def compute_takt():
    try:
        shift = float(st.session_state.get('shift_sec', 8*3600))
        demand = float(st.session_state.get('demand_per_shift', 400))
        return shift / max(1.0, demand)
    except Exception:
        return 60.0

def find_bottleneck(steps):
    if not steps: return None
    m = max(steps, key=lambda x: float(x.get('ct_sec',0)))
    return m.get('name'), float(m.get('ct_sec',0))

def query_benchmarks():
    prof = st.session_state.get('profile_key','default')
    # simple defaults; use YAML in your profiles page
    return {'fpy_best': 98.0, 'changeover_best_min': 10}

def draft_countermeasures(topic:str):
    lib = {
        'changeover': ['Map internal vs external (SMED)','Shadow board for tools','Wheel-of-time scheduling'],
        'wip': ['Right-size batches','Supermarkets with kanban cards','Heijunka leveling'],
        'defects': ['Poka-yoke fixtures','Autostop (Jidoka) on test fails','Layered audits at handoff']
    }
    return lib.get(topic, ['5S at point-of-use','Standard work w/ visuals','Daily tier boards'])


def recommend_with_trace(steps:list)->list:
    """Return list of {action, because, tags} based on metrics/benchmarks."""
    t = compute_takt()
    bn = find_bottleneck(steps)
    bm = query_benchmarks()
    out = []
    if bn:
        name, ct = bn
        if ct > t:
            out.append({
                "action": "Reduce bottleneck CT at " + str(name),
                "because": f"Bottleneck CT {ct:.1f}s exceeds takt {t:.1f}s; throughput capped.",
                "tags": ["Now","Capacity","Flow"]
            })
    chg = float(st.session_state.get("changeover_min", 0))
    if chg and chg > bm.get("changeover_best_min", 10):
        out.append({
            "action": "Run SMED on top 1–2 families",
            "because": f"Changeover {chg:.0f} min > best practice {bm.get('changeover_best_min')} min; sequence losses likely.",
            "tags": ["Now","SMED","Availability"]
        })
    fpy = float(st.session_state.get("fpy_current", 0) or 0)
    if fpy and fpy < bm.get("fpy_best", 98.0):
        out.append({
            "action": "Jidoka at test & Poka‑yoke on feeders",
            "because": f"FPY {fpy:.1f}% < best practice {bm.get('fpy_best')}%; rework load indicated.",
            "tags": ["Next","Quality","Jidoka"]
        })
    wip = float(st.session_state.get("wip_total", 0) or 0)
    if wip and wip > 0:
        out.append({
            "action": "Kanban supermarkets + batch right‑sizing",
            "because": f"WIP={wip:.0f} suggests queues; leveling and pull can reduce waiting.",
            "tags": ["Next","WIP","Pull"]
        })
    if not out:
        out.append({"action":"Standardize Work + 5S sustain","because":"No critical gaps detected; stabilize and visualize.","tags":["Later","Standards","5S"]})
    return out
