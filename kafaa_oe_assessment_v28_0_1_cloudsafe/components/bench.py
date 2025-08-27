
import yaml, os
def load_profile(name: str, base_path="benchmarks"):
    path = os.path.join(base_path, f"{name}.yml")
    if not os.path.exists(path):
        return {"label":"Custom","kpis":{}}
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)
def percentile(value, target, higher_is_better=True):
    if value is None or target is None: return None
    try:
        if higher_is_better: return round(min(99, max(1, (value/target)*100)),1)
        else: return round(min(99, max(1, (target/value)*100)),1)
    except Exception: return None
