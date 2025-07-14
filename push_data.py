import os
from dotenv import load_dotenv
from pymongo.mongo_client import MongoClient


# Load environment variables from .env file
load_dotenv()

uri = os.getenv("MONGO_DB_URL")