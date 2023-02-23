from pydantic import BaseModel, EmailStr
from datetime import datetime


class TweetCreate(BaseModel):
    content: str


class TweetResponse(BaseModel):
    id: int
    content: str
    created_at: datetime
    
    class Config:
        orm_mode = True



class UserCreate(BaseModel):
    handle: str
    email: EmailStr
    first_name: str
    last_name: str
    password: str

class UserResponse(BaseModel):
    id: int
    handle: str
    first_name: str
    last_name: str

    class Config:
        orm_mode = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str