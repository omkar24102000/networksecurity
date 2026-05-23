import os
import sys

from dotenv import load_dotenv
load_dotenv()

mongo_db_uri=os.getenv("MONGO_DB_URI")
print(mongo_db_uri)


import certifi
#ca = certificate authority
ca = certifi.where()

import pandas as pd
import pymongo
import numpy as np
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException 

class  NetworkDataExtract():
    def __init__(self):
        try:
            logging.info("Entered the NetworkDataExtract class")
            self.mongo_db_uri = mongo_db_uri
            self.client = pymongo.MongoClient(self.mongo_db_uri, tlsCAFile=ca)
            logging.info("Connected to MongoDB successfully")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        

    def cv_to_json_convertor(self,file_path):
        try:
            data =pd.read_csv(file_path)
            logging.info("CSV file read successfully")
            data.reset_index(drop=True,inplace=True)
            records = list(data.T.to_dict().values())
            logging.info("CSV file converted to JSON successfully")
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def insert_data_to_mongodb(self,records,database,collection):
        try:
            self.database = database
            self.records = records
            self.collection = collection
            self.mongo_client = pymongo.MongoClient(self.mongo_db_uri, tlsCAFile=ca)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            logging.info("Data inserted to MongoDB successfully")
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=='__main__':
    try:
        file_path ="/home/omkar/mixed/learning /ML_project_2/Network_Data/phisingData.csv"
        database = "omkarAI"
        collection = "NetworkData"
        network_obj = NetworkDataExtract()
        records = network_obj.cv_to_json_convertor(file_path)
        inserted_records_count = network_obj.insert_data_to_mongodb(records, database, collection)
        print(f"Inserted {inserted_records_count} records to MongoDB successfully")
        logging.info(f"Inserted {inserted_records_count} records to MongoDB successfully")
    except Exception as e:
        raise NetworkSecurityException(e,sys)