"""
Backward-compatible re-export. The real MongoDB connection logic lives in
`database/mongodb.py`; this module exists because several parts of the
original project skeleton import config paths for the DB.
"""
from database.mongodb import connect_to_mongo, close_mongo_connection, get_database  # noqa: F401
