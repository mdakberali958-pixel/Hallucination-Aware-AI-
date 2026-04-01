from embeddings import search

def build_rag_prompt(q):
    docs = search(q)
    context = "\n".join(docs)
    return f"Use context:\n{context}\n\nQuestion:{q}", docs
