
import json
from pathlib import Path
from .ai_client import chat
PROMPT_OBS = (Path(__file__).resolve().parent.parent/'prompts'/'observations_pqcdsm.txt').read_text(encoding='utf-8')
def build_context(state: dict) -> str:
    import math
    ctx = {
        "factory": state.get("factory_name"),
        "year": state.get("year"),
        "takt_sec": state.get("takt_sec"),
        "ct_table": state.get("ct_table"),
        "kpis": state.get("kpis"),
        "inventory_value": state.get("financials_inventory") or state.get("inventory_value"),
        "coach_results": state.get("coach_results"),
        "benchmarks": state.get("benchmarks"),
        "demand_per_shift": state.get("demand_per_shift"),
        "shift_sec": state.get("shift_sec")
    }
    return json.dumps(ctx, ensure_ascii=False, indent=2)
def generate_observations_ai(state: dict) -> list[dict]:
    sys = {"role":"system","content":"Be precise, quantify, and keep a professional Gemba tone."}
    user = {"role":"user","content": PROMPT_OBS + "\n\nINPUTS:\n" + build_context(state)}
    out = chat([sys,user])
    try:
        data = json.loads(out)
        if isinstance(data, list): return data
    except Exception: pass
    return [{"section":"Production","title":"Automated observations (fallback)","text": out,"measured_count":0,"inferred_count":1}]
