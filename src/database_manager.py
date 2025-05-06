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

    def connect(self, db_username, db_password): # MongoDB connection string
        uri = f"mongodb+srv://{db_username}:{db_password}@araproject.iepyikz.mongodb.net/?retryWrites=true&w=majority&appName=ARAProject"

        try: # Attempt to connect to the database
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000) # 5 second timeout
            self.client.admin.command('ping') # Ping the server to check if it's available
            print(f"Successfully connected as {db_username}") # Print success message
            self.db_name = db_username # Set the database name to the username
            self.db = self.client[self.db_name] # Set the database to the username
            return (True, "")
        except Exception as e: # If connection fails, print the error
            print(f"Failed to connect to database as {db_username}: {e}") # Print error message
            self.client = None
            self.db = None
            return (False, e)

    def change_client(self, new_user:string, new_cred:string): # Change the database client to a new user
        print(f"Switching to {new_user}") # Print message indicating the switch
        success = self.connect(new_user, new_cred) # Attempt to connect to the new database
        return success # Return success status


    def save_data(self, collectionname, data): # Save data to the database
        if self.db == None: # Check if the database is connected
            print("No database connection.")
            return None

        try: # Attempt to insert data into the specified collection
            print(self.db_name)
            result = self.db[collectionname].insert_one(data) # Insert data into the collection
            print(f"Data inserted into '{self.db_name}' with _id: {result.inserted_id}")
            return result.inserted_id # Return the ID of the inserted data
        except Exception as e: # If insertion fails, print the error
            print(f"Failed to insert data: {e}") # Print error message
            return None

    def load_data(self, active_pdf): # Load data from the database
        if self.db is None: # Check if the database is connected
            print("No database connection.")
            return None
        try: # Attempt to find all documents in the specified collection
            collection = self.db[active_pdf] # Get the collection for the active PDF
            result = collection.find({}, {"_id": 0}) # Find all documents, excluding the ID field
            return result

        except Exception as e: # If loading fails, print the error
            print(f"Failed to load data: {e}")
            return None

