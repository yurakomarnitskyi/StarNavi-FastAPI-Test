"""
Database confirguration sqlalchemy.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import sqlalchemy


DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base = sqlalchemy.orm.declarative_base()
