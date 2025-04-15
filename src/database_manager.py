'''
DatabaseManager class for managing database operations.
This class provides methods to save and load data from the database.
'''

# from sqlalchemy import create_engine, text  # Import text for raw SQL queries
# from sqlalchemy.orm import sessionmaker

import random, json, os, string
from pymongo.mongo_client import MongoClient

class User:
    def __init__(self):

        self.user_data = { 
            "FTS_completed" : False, #First time setup
            "user_id" : None,
            "server_connection" : False,
            "disable_prompts" : False,
            "offline_mode" : False,
            "tutorial_complete" : False
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

    def SaveUserJSON(self, filename):
        pass

    def LoadUserJSON(self, filename = "userdata"):
        '''
    
        Loads the User's userdata JSON
        if it fails, run FirstTimeSetup to create it
        
        '''
        try:
            with open(filename, 'r') as file:
                self.user_data = json.load(file)
                print(self.user_data)
                return True
                
                
        except FileNotFoundError:
            print("ERROR NO JSON FILE FOUND")
            self.FirstTimeSetup()

class DatabaseManager:
    def __init__(self):
        pass

    def _initialize_database(self):
        pass

    def save_data(self, query, params):
        pass

    def load_data(self, query, params):
        pass



# class DatabaseManager:
#     def __init__(self):
#         self.engine = create_engine('sqlite:///ara.db')  # SQLite database
#         self.Session = sessionmaker(bind=self.engine)
#         self._initialize_database()

#     def _initialize_database(self):  # Initialize the database
#         """Initialize the database with the required tables."""
#         with self.engine.connect() as connection:
#             connection.execute(text("""
#                 CREATE TABLE IF NOT EXISTS notes (
#                     id INTEGER PRIMARY KEY AUTOINCREMENT,
#                     content TEXT NOT NULL
#                 )
#             """))

#     def save_data(self, query, params):
#         """Save data to the database."""
#         session = self.Session()
#         try:
#             session.execute(text(query), params)  # Ensure params is a dictionary
#             session.commit()  # Commit the transaction
#             print("Data saved successfully.")
#         except Exception as e:
#             session.rollback()  # Rollback in case of an error
#             print(f"Error saving data: {e}")
#         finally:
#             session.close()  # Ensure the session is closed

#     def load_data(self, query, params=None):
#         """Load data from the database."""
#         session = self.Session()
#         try:
#             if params is None:
#                 params = {}
#             result = session.execute(text(query), params)  # Pass params for parameterized queries
#             return [dict(row._mapping) for row in result]  # Use _mapping for dictionary-like access
#         except Exception as e:
#             print(f"Error loading data: {e}")
#             return []
#         finally:
#             session.close()  # Ensure the session is closed