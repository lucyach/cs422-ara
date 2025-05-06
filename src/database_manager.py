'''
DatabaseManager class for managing database operations.
This class provides methods to save and load data from the database.
'''

import random, json, os, string
from pymongo.mongo_client import MongoClient
from datetime import datetime

class DatabaseManager:
    '''

    DatabaseManager: Database class, holds functionality for sending to the database and switching clients

    '''
    def __init__(self):
        self.db_name = None 

    def connect(self, db_username, db_password):
        uri = f"mongodb+srv://{db_username}:{db_password}@araproject.iepyikz.mongodb.net/?retryWrites=true&w=majority&appName=ARAProject"

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            print(f"Successfully connected as {db_username}")
            self.db_name = db_username
            
            self.db = self.client[self.db_name]
            return (True, "")
        except Exception as e:
            print(f"Failed to connect to database as {db_username}: {e}")
            self.client = None
            self.db = None
            return (False, e)

    def change_client(self, new_user:string, new_cred:string):
        print(f"Switching to {new_user}")
        success = self.connect(new_user, new_cred)
        return success


    def save_data(self, collectionname, data):
        if self.db == None:
            print("No database connection.")
            return None

        try:
            print(self.db_name)
            result = self.db[collectionname].insert_one(data)
            print(f"Data inserted into '{self.db_name}' with _id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"Failed to insert data: {e}")
            return None

    def load_data(self, active_pdf):
        if self.db is None:
            print("No database connection.")
            return None
        try:
            collection = self.db[active_pdf]
            result = collection.find({}, {"_id": 0})
            return  result

        except Exception as e:
            print(f"Failed to load data: {e}")
            return None

