'''
DatabaseManager class for managing database operations.
This class provides methods to save and load data from the database.
'''

import random, json, os, string
from pymongo.mongo_client import MongoClient
from datetime import datetime

'''
CLASS DEFINITIONS

User: Local data about the client

Database: Database class

'''

class User:
    def __init__(self):

        self.user_data = { 
            "FTS_completed" : False, #First time setup
            "user_id" : None,
            "server_connection" : False,
            "disable_prompts" : False,
            "offline_mode" : False,
            "tutorial_complete" : False,
            "login": "None"
        }


    def FirstTimeSetup(self):
        '''
        Initiates first time setup
        Generates a new user ID and updates needed parameters within the user_data dictionary

        Stores that user_data dictionary to a new JSON file by the name 'userdata'

        '''
        characters = string.ascii_letters + string.digits
        new_user_id = ''.join(random.choice(characters) for _ in range(16))
        

        self.user_data["user_id"] = new_user_id
        self.user_data["FTS_completed"] = True

        filename = "userdata"

        with open(filename, 'w') as file:
            json.dump(self.user_data, file, indent = 4)

        print(f"User ID: {new_user_id}")

    def SaveUserJSON(self, filename = "userdata"):
            with open(filename, 'r') as file:
                self.user_data = json.load(file)
                #print(self.user_data)
                return True

    def LoadUserJSON(self, filename = "userdata"):
        '''
    
        Loads the User's userdata JSON
        if it fails, run FirstTimeSetup to create it
        
        '''
        try:
            with open(filename, 'r') as file:
                self.user_data = json.load(file)
                #print(self.user_data)
                return True     
        except FileNotFoundError:
            #print("ERROR NO JSON FILE FOUND")
            self.FirstTimeSetup()

class DatabaseManager:
    def __init__(self, db_username="ARAUser1", db_password="CREDENTIALS", db_name="Notes"):
        self.db_name = db_name
        self.connect(db_username, db_password)

    def connect(self, db_username, db_password):
        uri = f"mongodb+srv://{db_username}:{db_password}@araproject.iepyikz.mongodb.net/?retryWrites=true&w=majority&appName=ARAProject"

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=7000)
            self.client.admin.command('ping')
            print(f"Successfully connected as {db_username}")
            self.db = self.client[self.db_name]
        except Exception as e:
            print(f"Failed to connect to database as {db_username}: {e}")
            self.client = None
            self.db = None

    def change_client(self, new_user:string, new_cred:string):
        print(f"Switching to {new_user}")
        self.connect(new_user, new_cred)


    def save_data(self, collection_name, data):
        if not self.db:
            print("No database connection.")
            return None

        try:
            result = self.db[collection_name].insert_one(data)
            print(f"Data inserted into '{collection_name}' with _id: {result.inserted_id}")
            return result.inserted_id
        except Exception as e:
            print(f"Failed to insert data: {e}")
            return None

    def load_data(self, collection_name, query={}):
        if not self.db:
            print("No database connection.")
            return None

        try:
            collection = self.db[collection_name]
            result = collection.find_one(query)
            print(f"Loaded '{collection_name}': {result}")
            return result
        
        except Exception as e:
            print(f"Failed to load data: {e}")
            return None

