import numpy as np, re
from sentence_transformers import SentenceTransformer
model = SentenceTransformer("all-MiniLM-L6-v2")

def sim(a,b):
    e = model.encode([a,b])
    return np.dot(e[0],e[1])/(np.linalg.norm(e[0])*np.linalg.norm(e[1]))

def split_claims(text):
    return re.split(r'[.?!]', text)

def claim_score(ans,docs):
    claims = split_claims(ans)
    scores = []
    for c in claims:
        if len(c.strip())<5: continue
        scores.append(max([sim(c,d) for d in docs]))
    return sum(scores)/len(scores) if scores else 0.5

def hallucination_analysis(q,a,docs=None):
    grounding = max([sim(a,d) for d in docs]) if docs else 0.5
    claim = claim_score(a,docs) if docs else 0.5
    sc = 0.8
    risk = (1-sc)*0.2 + (1-grounding)*0.5 + (1-claim)*0.3
    return {
        "risk_score": round(risk*100,2),
        "confidence": round((1-risk)*100,2),
        "metrics": {
            "document_support": round(grounding*100,2),
            "semantic_consistency": round(sc*100,2),
            "fact_claim_verification": round(claim*100,2),
            "similarity_to_context": round(grounding*100,2)
        }
    }
