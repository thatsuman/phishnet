from pymongo import MongoClient
import certifi

# MongoDB Atlas connection URI
uri = "mongodb+srv://suman:catchfish@phishnet-cluster.nnrstjp.mongodb.net/?retryWrites=true&w=majority"

# Create a MongoClient instance with SSL certificate verification using certifi
client = MongoClient(uri, tlsCAFile=certifi.where())

try:
    # Ping the MongoDB deployment to verify connection
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)