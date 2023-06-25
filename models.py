from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Define the table structure
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    age = Column(Integer)

    

# Create the database engine and session
engine = create_engine("postgresql://postgres:2010@localhost:5432/postgres")
Session = sessionmaker(bind=engine)
session = Session()

# Create the table in the database
Base.metadata.create_all(engine)

