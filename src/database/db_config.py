import os 
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(
	DATABASE_URL,
	pool_pre_ping=True,
	pool_recycle=300,
    echo=True
)
SessionLocal = sessionmaker(autoflush=False, bind=engine)
Base = declarative_base()