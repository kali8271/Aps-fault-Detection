from pymongo import MongoClient

# TODO: Replace with your actual MongoDB connection string
mongo_client = MongoClient("mongodb://localhost:27017/")

# Set the correct target column name from the CSV header
TARGET_COLUMN = "class"
