from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str | int
    password: str | int
    
class Task(BaseModel):
    title: str 
    description: str
    time: str
    date: str
    underTasks: List

