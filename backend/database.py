from pymongo import MongoClient
from dotenv import load_dotenv
import os

# load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")

client = MongoClient(MONGO_URI)

db = client["chestxreasoner"]

users_collection = db["users"]
analysis_collection = db["analysis_history"]

print("MongoDB Atlas connected")