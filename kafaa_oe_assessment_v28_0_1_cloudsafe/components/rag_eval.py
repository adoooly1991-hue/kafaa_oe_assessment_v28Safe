
def eval_rag(answer:str, context:str) -> dict:
    """Optional RAGAS-like metrics placeholder.
    Returns simple heuristic scores when ragas lib isn't installed."""
    try:
        from ragas import evaluate
        # (pseudo; integrate with Dataset and metrics if library present)
        return {"faithfulness": 0.8, "context_precision": 0.75}
    except Exception:
        # Heuristic: more overlap -> higher 'faithfulness'
        inter = len(set(answer.lower().split()) & set(context.lower().split()))
        denom = max(1, len(set(answer.lower().split())))
        f = round(min(1.0, inter/denom + 0.2), 2)
        return {"faithfulness": f, "context_precision": round(min(1.0, f*0.9),2)}
