
def rollup_impact(state: dict) -> dict:
    s = state or {}
    out = {"savings_items": [], "frozen_cash_items": [], "sales_oppty_items": []}
    acts = s.get("countermeasures", []); cm_total=0.0
    for a in acts:
        val = float(a.get("annual_savings_sar") or a.get("benefit_sar_year") or 0)
        if val: cm_total += val; out["savings_items"].append((a.get("title","Action"), val))
    if cm_total: out["savings_items"].append(("Total (actions)", cm_total))
    inv_df = s.get("inventory_df"); frozen=[]
    if inv_df is not None and hasattr(inv_df,"columns"):
        df = inv_df.copy()
        if "OnHandQty" in df.columns and "UnitCost" in df.columns:
            df["ValueSAR"] = df["OnHandQty"]*df["UnitCost"]
            if "Excess" in df.columns:
                frozen.append(("Excess", float(df.loc[df["Excess"],"ValueSAR"].sum())))
            if "Obsolete" in df.columns:
                frozen.append(("Obsolete", float(df.loc[df["Obsolete"],"ValueSAR"].sum())))
    else:
        inv = float(s.get("financials_inventory") or s.get("inventory_value") or 0.0)
        if inv: frozen.append(("Inventory (est.)", inv*0.3))
    out["frozen_cash_items"] = [(k,v) for (k,v) in frozen if v>0]
    sales=[]; takt=s.get("takt_sec"); ct_table=s.get("ct_table", [])
    bn = max([r.get("ct",0) for r in ct_table], default=0)
    if takt and bn and bn>takt:
        shift_sec=s.get("shift_sec") or 8*3600; shifts_per_year=2*5*52
        out_rate_bn=shift_sec/bn; out_rate_takt=shift_sec/takt
        lost_units=max(0, out_rate_takt - out_rate_bn)
        price=float(s.get("price_per_unit_sar") or s.get("avg_selling_price_sar") or 0.0)
        sales.append(("Missed capacity (year)", float(lost_units*shifts_per_year*price)))
    out["sales_oppty_items"] = [(k,v) for (k,v) in sales if v>0]
    return out
def series_to_waterfall_data(items):
    x,y,m=[],[],[]; total=0.0
    for label,val in items: x.append(label); y.append(val); m.append("relative"); total+=val
    if items: x.append("TOTAL"); y.append(total); m.append("total")
    return x,y,m
