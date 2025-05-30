import os
import sys
import json 
import certifi
import pymongo
import numpy as np
import pandas as pd
from dotenv import load_dotenv
from phishnet.logging.logger import logging
from phishnet.exception.exception import PhishnetException

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")

ca = certifi.where()

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise PhishnetException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            df = pd.read_csv(file_path)
            df.reset_index(drop=True, inplace=True)
            records = list(json.loads(df.T.to_json()).values())
            return records
        except Exception as e:
            raise PhishnetException(e, sys)
        
    def insert_data_to_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGODB_URL)
            self.database = self.mongo_client[self.database]

            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)

            return(len(self.records))
        
        except Exception as e:
            raise PhishnetException(e, sys)

if __name__ == '__main__':
    FILE_PATH = 'network_data\phisingData.csv'
    DATABASE = "phishnetdb" # database name in mongodb
    Collection = "NetworkData" # collection name in database
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_to_mongodb(records, DATABASE, Collection)
    print("Total number of record is: ", no_of_records)
