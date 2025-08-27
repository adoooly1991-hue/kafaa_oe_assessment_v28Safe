
import yaml, streamlit as st
from .bench import load_profile
def _eval_cond(cond: str, ctx: dict) -> bool:
    cond = cond.strip()
    if any(op in cond for op in ['>','<','==']):
        try:
            expr = cond.replace('benchmark_fpy', str(ctx.get('bench_fpy',98))).replace('mtbf_goal', str(ctx.get('bench_mtbf',1000)))
            expr = expr.replace('ct_bn', str(ctx.get('ct_bn',0))).replace('takt', str(ctx.get('takt',0)))
            return bool(eval(expr, {}, {}))
        except Exception: pass
    if cond.startswith(('>','<')):
        try:
            op, val = cond[0], float(cond[1:]); last=float(ctx.get('_last',0))
            return (last>val) if op=='>' else (last<val)
        except Exception: return False
    if cond.startswith('=='): return str(ctx.get('_last',''))==cond[2:]
    if cond == '< benchmark':
        bench = ctx.get('_bench'); last=ctx.get('_last')
        try: return float(last) < float(bench)
        except Exception: return False
    return False
def run_coach(tree_yaml_path: str, profile_key: str = "default"):
    prof = load_profile(profile_key)
    with open(tree_yaml_path, "r", encoding="utf-8") as f: tree = yaml.safe_load(f)
    stages = tree.get("stages", []); all_hints = []; per_stage = {}
    bench_fpy = prof.get("kpis",{}).get("fpy_best_practice_pct", 98)
    bench_mtbf = prof.get("kpis",{}).get("mtbf_hours_goal", 1000)
    for stage in stages:
        key=stage["key"]; title=stage["title"]
        with st.expander(f"◻︎ {title}", expanded=False):
            scoremap={}; answers={}
            for q in stage.get("questions", []):
                qid=q["id"]; qtype=q["type"]; label=q["text"]; val=None
                if qtype=="slider":
                    val=st.slider(label, min_value=int(q.get("min",0)), max_value=int(q.get("max",100)), value=int(q.get("value",0)), key=f"{key}_{qid}")
                elif qtype=="number":
                    val=st.number_input(label, value=float(q.get("value",0)), key=f"{key}_{qid}")
                elif qtype=="select":
                    val=st.selectbox(label, q.get("options",[]), key=f"{key}_{qid}")
                answers[qid]=val
                for fol in q.get("follow", []):
                    cond=fol.get("when"); ctx={"_last":val, "bench_fpy":bench_fpy, "bench_mtbf":bench_mtbf, "ct_bn":answers.get("ct_bn"), "takt":answers.get("takt")}
                    if _eval_cond(cond, ctx):
                        for fq in fol.get("ask", []):
                            fqid=fq["id"]; fqt=fq["type"]; flabel=fq["text"]; fval=None
                            if fqt=="slider":
                                fval=st.slider(flabel, min_value=int(fq.get("min",0)), max_value=int(fq.get("max",100)), value=int(fq.get("value",0)), key=f"{key}_{fqid}")
                            elif fqt=="number":
                                fval=st.number_input(flabel, value=float(fq.get("value",0)), key=f"{key}_{fqid}")
                            elif fqt=="select":
                                fval=st.selectbox(flabel, fq.get("options",[]), key=f"{key}_{fqid}")
                            answers[fqid]=fval
                for rule in q.get("map", []):
                    cond=rule.get("cond"); ctx={"_last":val, "bench_fpy":bench_fpy, "benchmark":prof.get("kpis",{}).get(q.get("benchmark_key")), "bench_mtbf":bench_mtbf, "ct_bn":answers.get("ct_bn"), "takt":answers.get("takt")}
                    if _eval_cond(cond, ctx):
                        w=rule.get("waste"); sc=rule.get("score",1); scoremap[w]=scoremap.get(w,0)+sc
            top=sorted(scoremap.items(), key=lambda t:t[1], reverse=True)[:3]
            per_stage[key]={"title":title, "answers":answers, "top_wastes":top}
            for w,sc in top: all_hints.append({"topic": title, "waste_hint": w, "score": sc})
            if top: st.success("Top wastes: " + ", ".join([f"{w} (score {sc})" for w,sc in top]))
            else: st.info("No significant wastes flagged by thresholds here.")
    st.session_state["coach_results"]=all_hints; st.session_state["coach_mode_results"]=per_stage
    return per_stage, all_hints
