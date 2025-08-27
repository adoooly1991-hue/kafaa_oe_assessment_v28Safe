
import faiss, numpy as np
from .ai_client import embed_texts
class MiniRAG:
    def __init__(self):
        self.index=None; self.chunks=[]
    def _chunk_text(self, text: str, max_chars=800):
        return [text[i:i+max_chars] for i in range(0,len(text),max_chars)]
    def add_document(self, text: str):
        parts=self._chunk_text(text); vecs=embed_texts(parts)
        arr=np.array(vecs).astype('float32')
        if self.index is None: self.index=faiss.IndexFlatIP(arr.shape[1])
        self.index.add(arr); self.chunks.extend(parts)
    def search(self, query: str, k=5):
        if self.index is None: return []
        q=np.array(embed_texts([query])).astype('float32')
        D,I=self.index.search(q,k); res=[]
        for idx,score in zip(I[0],D[0]):
            if 0<=idx<len(self.chunks): res.append((self.chunks[idx], float(score)))
        return res
