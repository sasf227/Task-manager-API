from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker, Session
from typing import Annotated
from fastapi import Depends

engine = create_engine(
    "mariadb+mariadbconnector://root:root@127.0.0.1:3306/task_manager_db"
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
def create_tables():
    Base.metadata.create_all(bind=engine)
    
db_dependency = Annotated[Session, Depends(get_db)]

