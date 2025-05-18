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
from phishnet.utils.ml_utils.model.estimator import PhishnetModel
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
phishnetapp = FastAPI()
origins = ["*"]

phishnetapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from fastapi.templating import Jinja2Templates
templates = Jinja2Templates(directory="./templates")

@phishnetapp.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url="/docs")

@phishnetapp.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return Response("Training completed successfully.")
    except Exception as e:
        raise PhishnetException(e, sys)
    
@phishnetapp.post("/predict")
async def predict_route(request:Request, file: UploadFile = File(...)):
    try:
        df = pd.read_csv(file.file)
        #print(df)
        preprocesor = load_object("final_model/preprocessor.pkl")
        final_model=load_object("final_model/model.pkl")
        network_model = PhishnetModel(preprocessor=preprocesor,model=final_model)
        print(df.iloc[0])
        y_pred = network_model.predict(df)
        print(y_pred)
        df['predicted_column'] = y_pred
        print(df['predicted_column'])
        #df['predicted_column'].replace(-1, 0)
        #return df.to_json()
        df.to_csv('prediction_output/output.csv')
        table_html = df.to_html(classes='table table-striped')
        #print(table_html)
        return templates.TemplateResponse("table.html", {"request": request, "table": table_html})
        
    except Exception as e:
            raise PhishnetException(e,sys)


if __name__ == "__main__":
    app_run(phishnetapp, host="localhost", port=8000)
