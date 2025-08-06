from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Path to your SQLite file
DATABASE_URL = "sqlite:///./files.db"

# Create the engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the table
class FileHash(Base):
    __tablename__ = "file_hashes"
    hash = Column(String, primary_key=True)
    filename = Column(String, nullable=False)

# Create the table if it doesn't exist
Base.metadata.create_all(bind=engine)
