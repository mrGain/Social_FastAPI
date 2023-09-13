from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True 

class UserCreate(BaseModel):
    email: EmailStr
    password: str   
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config():
        orm_mode = True
class PostCreate(PostBase):
    pass 

class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut
    class Config():
        orm_mode = True
class PostOut(BaseModel):
    post: Post
    votes: int
    class Config():
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str        

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] | None

class Vote(BaseModel):
    post_id: int
    dir: conint(ge=0, le=1)