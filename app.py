import os
import sys

# Third-party imports
from dotenv import load_dotenv
import certifi
import pymongo
import pandas as pd
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from starlette.responses import RedirectResponse
from uvicorn import run as app_run

# Internal imports
from phishnet.exception.exception import PhishnetException
from phishnet.logging.logger import logging
from phishnet.pipeline.training_pipeline import TrainingPipeline
from phishnet.utils.main_utils.utils import load_object
from phishnet.constant.training_pipeline import (
    DATA_INGESTION_COLLECTION_NAME,
    DATA_INGESTION_DATABASE_NAME,
)

# Load environment variables
load_dotenv()
mongo_url = os.getenv("MONGO_URL_KEY")
print(mongo_url)

# Setup MongoDB client with SSL certificate
ca = certifi.where()
client = pymongo.MongoClient(mongo_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
collection = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app setup
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training completed successfully.")
    except Exception as e:
        raise PhishnetException(e, sys)

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
