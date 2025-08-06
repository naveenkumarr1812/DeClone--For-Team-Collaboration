from sqlalchemy import Column, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "sqlite:///./files.db"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class FileHash(Base):
    __tablename__ = "file_hashes"
    hash = Column(String, primary_key=True)
    filename = Column(String, nullable=False)

Base.metadata.create_all(bind=engine)
