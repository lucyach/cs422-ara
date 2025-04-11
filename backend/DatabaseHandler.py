from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import random
import string
import json

# Early version, basically just experiementing with pushing/pull from the Mongo server

#SERVER HAS A 512mb LIMIT, UNLESS YOU'RE PAYING FOR MORE SPACE BE CAREFUL WHEN UPLOADING

# THIS IS YOUR MONGODB CREDENTIALS
# DO NOT PUSH THIS TO GITHUB
uri = "mongodb+srv://USER:PASSWORD@araproject.iepyikz.mongodb.net/?appName=ARAProject"

#COULD CREATE "FIRST TIME SETUP", SAVE CREDENTIALS LOCALLY (?)


# In the process of moving things into a Database class,
# Will see if this could be improved or is even needed

def generate_random_string(length):
    characters = string.ascii_letters + string.digits
    random_string = ''.join(random.choice(characters) for _ in range(length))
    return random_string

class User:

    def __init__(self):

        FTS_completed = False
        user_id = None
        server_connection = False


    def FirstTimeSetup(self):
        user_id = generate_random_string(16)




class Database:
    def __init__(self):
        pass

    def VerifyConnection(self):
        '''
        Checks if the code successfully connects to the MongoDB database.
        '''
        try:
            client.admin.command('ping')
            print("Successfully connected to database!")
            return True
        except:
            print("ERROR: Could not connect to database!")
            return False
        
    def DatabaseVerification(self):
        '''
        Verify that the database the user is requesting exists
        '''
        pass


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Could designate an ID to each user, as a "login" method. Pull the corresponding notes from the server
# Could also save this data locally to a file, as to not have the user save it manually, JSON maybe? CSV?
user_id_input = input("Please input your User ID to get your notes: ")

userdb = client[str(user_id_input)]

# Error checking, if the inputted ID does not correspond to notes in a server
dbnames = client.list_database_names()
if str(user_id_input) not in dbnames:
    print("ERROR: Could not find your DB")
    exit()

# Print the notes of the corresponding User ID
usernotes = userdb["Notes"]

for x in usernotes.find():
    print(x)

# user_id = generate_random_string(16)
# print(f'Your user ID is:\t{user_id}')

# # Each User could have their own DB segment, denoted by above user ID. Could function as an "login" for cloud syncing
# testdb = client[str(user_id)]

# #We can use a 'collection' to 
# testcol = testdb["Notes"]

# Actual notes to upload
# testnotes = {"Chapter": 2, "Notes": "This is note 2"}

# This line actually uploads to the database
# x = testcol.insert_one(testnotes)

