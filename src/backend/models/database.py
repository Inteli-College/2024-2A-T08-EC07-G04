from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

<<<<<<< HEAD
DATABASE_URL = "postgresql://postgres:senha123@localhost:5432/postgres"
=======
DATABASE_URL = "postgresql://postgres:senha@localhost:5432/fillmore"
>>>>>>> 3fe7eeebb3a854a81334a9e9b75ebc07356c8c40
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
