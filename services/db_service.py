# from pymongo import MongoClient
# from config import config

# MONGO_URI = "mongodb+srv://shilpishuklajp:0Q8oKpebO3TNBuwf@cluster0.118s8.mongodb.net/"  # Replace with your actual MongoDB URI

# client = MongoClient(MONGO_URI)
# db = client["ats-db"]
# # try:
# #     client = MongoClient(MONGO_URI)
# #     # Try to get the database
# #     db = client.get_database()  # Replace with your database name if necessary
# #     print("Connection successful!")
# # except Exception as e:
# #     print(f"Connection failed: {str(e)}")

# # client = MongoClient(config.MONGO_URI)
# # db = client.get_database()

# def insert_application(data):
#     applications = db.applications
#     return applications.insert_one(data)

# def get_all_applications():
#     applications = db.applications
#     return list(applications.find())



# from pymongo import MongoClient
# from pymongo.errors import ConnectionError
from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
from config import config
 

try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)  # Set a timeout for connection
    # Check if the server is available
    client.admin.command('ping')
    print("Connected to MongoDB successfully.")
except ServerSelectionTimeoutError as e:
    print(f"Failed to connect to MongoDB: {e}")
    raise
 
db = client["ats-db"]
def is_email_unique(email):
    """Check if the email already exists in the database."""
    # Replace with the actual database query
    existing_record = db.applications.find_one({"email": email})
    return existing_record is None
def insert_application(data):
    applications = db.applications
    return applications.insert_one(data)
 
def get_all_applications():
    # Assuming you have already set up your MongoDB connection
    applications = db.applications

    # Define the projection to fetch specific fields
    projection = {
        "name": 1,
        "email": 1,
        "resume.is_ats_friendly": 1  # Fetching only the is_ats_friendly field from the resume array
    }

    # Query the database with the projection
    application_list = applications.find({}, projection)

    # Convert the cursor to a list and return
    return list(application_list)
