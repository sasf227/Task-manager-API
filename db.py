from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from db_dependency import Base

class Token(Base):
    __tablename__ = "token"
    
    id = Column(Integer, primary_key=True)
    access_token = Column(String, unique=True, nullable=False)
    token_type = Column(String, nullable=False)
    
class TokenData(Base):
    __tablename__ = "tokenData"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=True)
    
    
    
class User(Base):
    __tablename__ = "user"
    
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=True)
    
    tasks = relationship("Tasks", back_populates="user", cascade="all, delete-orphan")
    
class Tasks(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True)
    username_task = Column(String, ForeignKey("user.username"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    created_at = Column(String, nullable=False)
    updated_at = Column(String, nullable=False)
    completed_at = Column(String, nullable=False)
    deleted_at = Column(String, nullable=False)
    due_to = Column(String, nullable=False)
    update_log = Column(String, nullable=False)

    user = relationship("User", back_populates="tasks")