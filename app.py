from fastapi import FastAPI, UploadFile, HTTPException
from pydantic import BaseModel
from llm import generate_answer
from rag import build_rag_prompt
from detector import hallucination_analysis
from pdf_loader import extract_text
from embeddings import create_index
from db import chats
from auth import signup, login
from sse_starlette.sse import EventSourceResponse

app = FastAPI()

class Query(BaseModel):
    question:str
    mode:str
    user_id:str="user1"

@app.post("/auth/signup")
def _signup(body:dict):
    token = signup(body.get("email"), body.get("password"))
    if not token: raise HTTPException(400, "User exists")
    return {"token": token}

@app.post("/auth/login")
def _login(body:dict):
    token = login(body.get("email"), body.get("password"))
    if not token: raise HTTPException(401, "Invalid")
    return {"token": token}

@app.post("/ask")
def ask(q:Query):
    if q.mode=="rag":
        prompt,docs = build_rag_prompt(q.question)
        ans = generate_answer(prompt)
        res = hallucination_analysis(q.question,ans,docs)
    else:
        ans = generate_answer(q.question)
        res = hallucination_analysis(q.question,ans)
        docs=[]
    chats.insert_one({"user_id":q.user_id,"q":q.question,"a":ans,"analysis":res})
    return {"answer":ans,"analysis":res,"sources":docs}

@app.get("/stream")
async def stream(q: str):
    async def gen():
        text = generate_answer(q)
        for ch in text:
            yield {"data": ch}
    return EventSourceResponse(gen())

@app.post("/upload")
async def upload(file:UploadFile):
    text = extract_text(file.file)
    chunks = [text[i:i+300] for i in range(0,len(text),300)]
    create_index(chunks)
    return {"status":"indexed"}

@app.get("/history/{user_id}")
def history(user_id:str):
    return list(chats.find({"user_id":user_id},{"_id":0}))
