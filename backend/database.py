from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

URL_DATABASE= 'postgresql://postgres:root@localhost:5433/PDF_Reader'

engine = create_engine(URL_DATABASE)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables defined by Base subclasses
Base.metadata.create_all(bind=engine)


# Dependency for FastAPI to get a DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
