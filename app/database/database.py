from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# З'єднання з базою даних
DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(DATABASE_URL)

# Створення сесії бази даних
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Базовий клас для декларативної бази даних
Base = declarative_base()
