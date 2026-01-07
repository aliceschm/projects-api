# Database connection and get_db dependency

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Fetch variables
DATABASE_URL = os.getenv("DATABASE_URL")  # the database connection string

# Create the SQLAlchemy engine
# The engine is the core interface to the database, handling connections
engine = create_engine(DATABASE_URL)

# Create a configured "Session" class
# SessionLocal will be used to create individual database sessions
# autocommit=False: changes won't auto-commit; you control commit manually
# autoflush=False: changes are not auto-flushed to the DB until commit
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for SQLAlchemy models
# You inherit from this Base when defining tables with SQLAlchemy ORM
Base = declarative_base()


# get_db is a dependency used in FastAPI endpoints
# It's a Python generator that yields a database session for each request
# Ensures the session is properly closed after the request finishes
def get_db():
    db = SessionLocal()  # create a new session
    try:
        yield db  # provide the session to the route
    finally:
        db.close()  # close session after request is done


# # Test the connection
# try:
#     with engine.connect() as connection:
#         print("Connection successful!")
# except Exception as e:
#     print(f"Failed to connect: {e}")
