from sqlalchemy import Column, Integer, String, ForeignKey, Boolean, Text
from sqlalchemy.orm import relationship
from db_dependency import Base
from pydantic import BaseModel

# !!!!! IF USE SQLALCHEMY CLASSES IN FASTAPI ROUTES IT GONNA RAISE AN ERROR 
# !!!!! CREATE A PYDANTIC SCHEME FOR FASTAPI
class TokenSchema(BaseModel):
    access_token: str
    token_type: str 
    
    # !!!!! from_attributes=True ALLOWS PYDANTIC TO READ SQLALCHEMY OBJECTS
    class Config: 
        from_attributes = True


class TokenData(Base):
    __tablename__ = "tokenData"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=True)
    
    
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    disabled = Column(Boolean, nullable=True)
    
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")
    
    
# !!!!! SAME FOR USER
class UserSchema(BaseModel):
    username: str
    password_hash: str
    disabled: bool | None
    
    # !!!!! from_attributes=True ALLOWS PYDANTIC TO READ SQLALCHEMY OBJECTS
    class Config: 
        from_attributes = True    
    
    
class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    username_task = Column(String(255), ForeignKey("user.username"), nullable=False)
    title = Column(String(255), nullable=False)
    description = Column(String(255), nullable=False)
    created_at = Column(String(255), nullable=False)
    created_by = Column(String(255), nullable=False)
    time = Column(String(255), nullable=False)
    date = Column(String(255), nullable=False)
    status = Column(String(255), nullable=False)
    UT = Column(Text, nullable=True)


    user = relationship("User", back_populates="tasks")