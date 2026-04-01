from sentence_transformers import SentenceTransformer
import faiss, numpy as np, pickle

model = SentenceTransformer("all-MiniLM-L6-v2")

def create_index(docs):
    emb = model.encode(docs)
    index = faiss.IndexFlatL2(len(emb[0]))
    index.add(np.array(emb))
    pickle.dump(docs, open("docs.pkl","wb"))
    faiss.write_index(index,"index.faiss")

def load_index():
    return faiss.read_index("index.faiss"), pickle.load(open("docs.pkl","rb"))

def search(q,k=3):
    index,docs = load_index()
    q_emb = model.encode([q])
    _,I = index.search(np.array(q_emb),k)
    return [docs[i] for i in I[0]]
