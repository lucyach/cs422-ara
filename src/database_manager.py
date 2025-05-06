'''
DatabaseManager class for managing database operations.
This class provides methods to save and load data from the database.
'''

import random, json, os, string
from pymongo.mongo_client import MongoClient
from datetime import datetime
import certifi

class DatabaseManager:
    '''

    DatabaseManager: Database class, holds functionality for sending to the database and switching clients

    '''
    def __init__(self):
        self.db_name = None 

    def connect(self, db_username, db_password):
        uri = f"mongodb+srv://{db_username}:{db_password}@araproject.iepyikz.mongodb.net/?retryWrites=true&w=majority&appName=ARAProject"

        try:
            self.client = MongoClient(uri, serverSelectionTimeoutMS=5000, tlsCAFile=certifi.where()) # Connect to the MongoDB server
            self.client.admin.command('ping')
            print(f"Successfully connected as {db_username}")
            self.db_name = db_username
            
            self.db = self.client[self.db_name]
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
        
    def update_data(self, collectionname, filter, data):
        if self.db == None:
            print("No database connection.")
            return None

        try:
            print(self.db_name)
            result = self.db[collectionname].update_one(filter, {"$set": data})
            print(f"Data updated in '{self.db_name}")
            return True
        except Exception as e:
            print(f"Failed to update data: {e}")
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
        
    def load_notes_from_menu(self, label, pdf):
        try:
            parts = label.split(" - ")
            if len(parts) != 2:
                print("Invalid label format. Expected 'chapter_title - section_heading'")
                return None

            chapter_title, section_heading = parts

            collection = self.db[pdf]

            doc = collection.find_one({
                "chapter_title": chapter_title,
                "section_heading": section_heading
            }, {"notes": 1, "_id": 0})

            if doc:
                notes_text = doc["notes"]
                return notes_text
            else:
                print("No matching note found.")
                return None

        except Exception as e:
            print(f"Error retrieving notes: {e}")
            return None



