
import os, base64, requests
def _maybe_import_openai():
    try:
        import openai
        return openai
    except Exception:
        return None
def get_provider():
    return os.environ.get("AI_PROVIDER") or "openai"
def get_model(kind="chat"):
    if kind=="embed": return os.environ.get("AI_EMBED_MODEL","text-embedding-3-small")
    if kind=="vision": return os.environ.get("AI_VISION_MODEL","gpt-4o-mini")
    return os.environ.get("AI_CHAT_MODEL","gpt-4o-mini")
def openai_client():
    openai = _maybe_import_openai()
    if not openai: raise RuntimeError("openai package not installed")
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key: raise RuntimeError("OPENAI_API_KEY not set")
    openai.api_key = api_key
    base = os.environ.get("OPENAI_BASE_URL")
    if base: openai.base_url = base
    return openai
def ollama_url():
    return os.environ.get("OLLAMA_URL","http://localhost:11434")
def chat(messages, tools=None):
    prov = get_provider()
    if prov == "ollama":
        url = f"{ollama_url()}/api/chat"; model = get_model("chat")
        payload = {"model": model, "messages": messages, "stream": False}
        r = requests.post(url, json=payload, timeout=120); r.raise_for_status()
        return r.json().get("message",{}).get("content","")
    openai = openai_client(); model = get_model("chat")
    resp = openai.chat.completions.create(model=model, messages=messages, tools=tools)
    return resp.choices[0].message.content
def vision_describe(image_bytes: bytes, prompt: str) -> str:
    prov = get_provider()
    if prov == "ollama":
        return "Vision not supported on this Ollama config."
    openai = openai_client(); model = get_model("vision")
    b64 = base64.b64encode(image_bytes).decode("utf-8")
    messages = [
        {"role":"system","content":"You are a manufacturing waste inspector. Be precise and concise."},
        {"role":"user","content":[
            {"type":"text","text": prompt},
            {"type":"image_url","image_url":{"url": f"data:image/png;base64,{b64}"}}
        ]}
    ]
    resp = openai.chat.completions.create(model=model, messages=messages)
    return resp.choices[0].message.content
def embed_texts(texts):
    prov = get_provider()
    if prov == "ollama":
        url = f"{ollama_url()}/api/embeddings"; model = os.environ.get("OLLAMA_EMBED_MODEL","mxbai-embed-large")
        out = []
        for t in texts:
            r = requests.post(url, json={"model": model, "prompt": t}, timeout=60); r.raise_for_status()
            out.append(r.json().get("embedding", []))
        return out
    openai = openai_client(); model = get_model("embed")
    resp = openai.embeddings.create(model=model, input=texts)
    return [d.embedding for d in resp.data]
