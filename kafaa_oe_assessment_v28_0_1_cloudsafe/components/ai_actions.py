
import json
from pathlib import Path
from .ai_client import chat
PROMPT_CM = (Path(__file__).resolve().parent.parent/'prompts'/'countermeasures.txt').read_text(encoding='utf-8')
def build_context(state: dict) -> str:
    ctx = {
        "top_wastes": [h.get("waste_hint") for h in state.get("coach_results",[]) if h.get("waste_hint")],
        "kpis": state.get("kpis"),
        "ct_table": state.get("ct_table"),
        "benchmarks": state.get("benchmarks"),
        "demand_per_shift": state.get("demand_per_shift"),
        "shift_sec": state.get("shift_sec")
    }
    return json.dumps(ctx, ensure_ascii=False, indent=2)
def generate_actions_ai(state: dict) -> list[dict]:
    sys = {"role":"system","content":"Be practical, Lean-oriented, and quantify benefits/costs."}
    user = {"role":"user","content": PROMPT_CM + "\n\nINPUTS:\n" + build_context(state)}
    out = chat([sys,user])
    try:
        data = json.loads(out)
        if isinstance(data, list): return data
    except Exception: pass
    return [{"title":"Review flow and implement FIFO controls","impact":60,"effort":30,"owner":"Ops","due":""}]
