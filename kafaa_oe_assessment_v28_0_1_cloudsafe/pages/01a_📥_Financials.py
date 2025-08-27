from components.boot import boot
mode = boot()

import streamlit as st, pandas as pd, math
st.set_page_config(page_title="Financials", layout="wide")
st.title("📥 Financials — targets, variances & ratios")

with st.expander("What this does"):
    st.markdown("""
    - Captures **actuals vs. budgets** to compute a **Cost Reduction Target** for the VSM charter.
    - Computes **Current Ratio**, **Quick Ratio** (≈ cash-focused for inventory analysis), and **Carrying Cost**.
    - Suggests an **Inventory Reduction Target** based on a target inventory turns goal.
    """)

with st.form("fin"):
    col1,col2,col3 = st.columns(3)
    with col1:
        rev = st.number_input("Revenue (SAR)", value=float(st.session_state.get("financials_revenue",0.0)))
        cogs = st.number_input("COGS (SAR)", value=float(st.session_state.get("financials_cogs",0.0)))
        ga = st.number_input("G&A (SAR)", value=float(st.session_state.get("financials_ga",0.0)))
        dep = st.number_input("Depreciation (SAR)", value=float(st.session_state.get("financials_dep",0.0)))
        finexp = st.number_input("Financial Expenses (SAR)", value=float(st.session_state.get("financials_finexp",0.0)))
    with col2:
        inv = st.number_input("Inventory (SAR)", value=float(st.session_state.get("financials_inventory",0.0)))
        cur_assets = st.number_input("Current Assets (SAR)", value=float(st.session_state.get("current_assets",0.0)))
        cur_liab = st.number_input("Current Liabilities (SAR)", value=float(st.session_state.get("current_liabilities",0.0)))
        carrying = st.number_input("Carrying cost %", value=float(st.session_state.get("carrying_rate_pct",25.0)))
        price = st.number_input("Avg selling price / unit (SAR)", value=float(st.session_state.get("price_per_unit_sar",0.0)))
    with col3:
        sales_target = st.number_input("Sales Target (SAR)", value=float(st.session_state.get("sales_target",0.0)))
        bud_cogs = st.number_input("Budgeted COGS (SAR)", value=float(st.session_state.get("bud_cogs",0.0)))
        bud_ga = st.number_input("Budgeted G&A (SAR)", value=float(st.session_state.get("bud_ga",0.0)))
        bud_dep = st.number_input("Budgeted Depreciation (SAR)", value=float(st.session_state.get("bud_dep",0.0)))
        bud_finexp = st.number_input("Budgeted Financial Expenses (SAR)", value=float(st.session_state.get("bud_finexp",0.0)))
        target_profit = st.number_input("Targeted Profit (SAR)", value=float(st.session_state.get("target_profit",0.0)))

    st.markdown("—")
    col4,col5 = st.columns(2)
    with col4:
        shift = st.number_input("Shift seconds", value=float(st.session_state.get("shift_sec",8*3600)))
    with col5:
        demand = st.number_input("Demand per shift (units)", value=float(st.session_state.get("demand_per_shift",0.0)))
    target_turns = st.number_input("Target Inventory Turns (per year)", value=float(st.session_state.get("target_turns",6.0)))

    submitted = st.form_submit_button("Save & compute")

if submitted:
    st.session_state.update({
        "financials_revenue":rev, "financials_cogs":cogs, "financials_inventory":inv,
        "financials_dep":dep, "financials_ga":ga, "financials_finexp":finexp,
        "carrying_rate_pct":carrying, "price_per_unit_sar":price,
        "current_assets":cur_assets, "current_liabilities":cur_liab,
        "sales_target":sales_target, "bud_cogs":bud_cogs, "bud_ga":bud_ga, "bud_dep":bud_dep, "bud_finexp":bud_finexp,
        "target_profit":target_profit, "shift_sec":shift, "demand_per_shift":demand, "takt_sec": (shift/demand if demand else st.session_state.get("takt_sec")),
        "target_turns": target_turns
    })
    st.success("Saved.")

# ---- Calculations ----
rev = st.session_state.get("financials_revenue",0.0)
cogs = st.session_state.get("financials_cogs",0.0)
ga = st.session_state.get("financials_ga",0.0)
dep = st.session_state.get("financials_dep",0.0)
finexp = st.session_state.get("financials_finexp",0.0)
inv = st.session_state.get("financials_inventory",0.0)
cur_assets = st.session_state.get("current_assets",0.0)
cur_liab = st.session_state.get("current_liabilities",0.0)
carrying = st.session_state.get("carrying_rate_pct",25.0)
target_profit = st.session_state.get("target_profit",0.0)
bud = {
    "COGS": st.session_state.get("bud_cogs",0.0),
    "G&A": st.session_state.get("bud_ga",0.0),
    "Depreciation": st.session_state.get("bud_dep",0.0),
    "FinancialExp": st.session_state.get("bud_finexp",0.0),
}

gp = rev - cogs
op = gp - ga - dep
profit = op - finexp
st.session_state["profit_actual"] = profit

current_ratio = (cur_assets/cur_liab) if cur_liab else None
quick_ratio = ((cur_assets - inv)/cur_liab) if cur_liab else None
carrying_cost_sar = inv * (carrying/100.0)

# Inventory reduction target via turns
turns_actual = (cogs / inv) if inv else None
turns_target = st.session_state.get("target_turns",6.0) or 6.0
target_avg_inventory = (cogs / turns_target) if turns_target else None
inv_reduction_target = max(0.0, inv - (target_avg_inventory or 0.0))

# Cost Reduction Target (two lenses)
gap_to_target_profit = max(0.0, target_profit - profit)
cost_over_budget = max(0.0, cogs - bud["COGS"]) + max(0.0, ga - bud["G&A"]) + max(0.0, dep - bud["Depreciation"]) + max(0.0, finexp - bud["FinancialExp"])
st.session_state["cost_reduction_target_sar"] = max(gap_to_target_profit, cost_over_budget)
st.session_state["quick_ratio"] = quick_ratio
st.session_state["current_ratio"] = current_ratio
st.session_state["inventory_carrying_cost"] = carrying_cost_sar
st.session_state["inv_reduction_target_sar"] = inv_reduction_target

st.markdown("### Results")
k1,k2,k3,k4 = st.columns(4)
with k1: st.metric("Actual Profit (SAR)", f"{profit:,.0f}")
with k2: st.metric("Cost Reduction Target (SAR)", f"{st.session_state['cost_reduction_target_sar']:,.0f}")
with k3: st.metric("Quick Ratio (≈ cash focus)", f"{quick_ratio:.2f}" if quick_ratio is not None else "—")
with k4: st.metric("Carrying Cost / year (SAR)", f"{carrying_cost_sar:,.0f}")

st.markdown("—")
st.subheader("Inventory levers")
c1,c2,c3 = st.columns(3)
with c1: st.metric("Turns (actual)", f"{turns_actual:.2f}" if turns_actual else "—")
with c2: st.metric("Turns (target)", f"{turns_target:.2f}")
with c3: st.metric("Reduction target (SAR)", f"{inv_reduction_target:,.0f}")
st.caption("We estimate savings from carrying cost on the reduction target inside the Impact waterfalls.")


st.markdown("—")
st.subheader("ABC inventory profile (optional)")
cA,cB,cC = st.columns(3)
with cA:
    a_pct = st.number_input("A-class inventory %", value=float(st.session_state.get("abc_A_pct",0.0)))
    a_carry = st.number_input("A-class carrying %", value=float(st.session_state.get("abc_A_carry_pct",0.0)))
with cB:
    b_pct = st.number_input("B-class inventory %", value=float(st.session_state.get("abc_B_pct",0.0)))
    b_carry = st.number_input("B-class carrying %", value=float(st.session_state.get("abc_B_carry_pct",0.0)))
with cC:
    c_pct = st.number_input("C-class inventory %", value=float(st.session_state.get("abc_C_pct",0.0)))
    c_carry = st.number_input("C-class carrying %", value=float(st.session_state.get("abc_C_carry_pct",0.0)))

if a_pct+b_pct+c_pct > 0:
    st.session_state.update({"abc_A_pct":a_pct,"abc_B_pct":b_pct,"abc_C_pct":c_pct,
                             "abc_A_carry_pct":a_carry,"abc_B_carry_pct":b_carry,"abc_C_carry_pct":c_carry})
    inv = st.session_state.get("financials_inventory",0.0)
    A_val = inv*(a_pct/100.0); B_val = inv*(b_pct/100.0); C_val = inv*(c_pct/100.0)
    weighted_carry = A_val*(a_carry/100.0) + B_val*(b_carry/100.0) + C_val*(c_carry/100.0)
    st.metric("Weighted carrying cost (SAR/yr)", f"{weighted_carry:,.0f}")
    st.caption("If provided, this replaces the simple inventory×carrying% calc in waterfalls.")
    st.session_state["inventory_carrying_cost_weighted"] = weighted_carry
