import jwt, datetime
from config import JWT_SECRET
from db import users

def create_token(user_id):
    payload = {"sub": user_id, "exp": datetime.datetime.utcnow() + datetime.timedelta(days=7)}
    return jwt.encode(payload, JWT_SECRET, algorithm="HS256")

def signup(email, password):
    if users.find_one({"email": email}):
        return None
    users.insert_one({"email": email, "password": password})
    return create_token(email)

def login(email, password):
    u = users.find_one({"email": email, "password": password})
    if not u: return None
    return create_token(email)
