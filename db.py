from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["hallucination_ai"]
chats = db["chats"]
users = db["users"]
