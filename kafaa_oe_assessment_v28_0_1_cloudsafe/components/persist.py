
import json, os
import pandas as pd

ALLOWED_PREFIXES = ("financials_", "bud_", "abc_", "champion_", "coach_", "kpis", "ct_", "pace_", "inventory_", "price_", "shift_", "demand_", "takt_", "factory_", "year", "charter_", "client_", "project_", "carrying_", "current_", "sales_target", "target_", "observations", "countermeasures", "countermeasures_df", "product_table", "vision_evidence")

def _is_serializable(x):
    try:
        json.dumps(x); return True
    except Exception:
        return False

def _pack_df(df: pd.DataFrame):
    return {"__type__": "dataframe", "columns": list(df.columns), "data": df.to_dict(orient="records")}

def _unpack_df(obj):
    import pandas as pd
    return pd.DataFrame(obj["data"], columns=obj["columns"])

def export_session(ss: dict) -> dict:
    out = {}
    for k,v in ss.items():
        if not any(k.startswith(p) for p in ALLOWED_PREFIXES):
            continue
        if isinstance(v, pd.DataFrame):
            out[k] = _pack_df(v)
        elif _is_serializable(v):
            out[k] = v
        else:
            # skip non-serializable entries (e.g., file handles)
            continue
    return out

def import_session(ss: dict, payload: dict):
    for k,v in payload.items():
        if isinstance(v, dict) and v.get("__type__")=="dataframe":
            ss[k] = _unpack_df(v)
        else:
            ss[k] = v
