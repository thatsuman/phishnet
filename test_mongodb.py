import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient

# Load environment variables from .env file
load_dotenv()

# MongoDB Atlas connection URI
uri = os.getenv("MONGODB_URL")

if not uri:
    raise ValueError("MONGODB_URL environment variable is not set.")

client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)