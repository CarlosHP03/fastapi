from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint
from datetime import datetime
from typing import Optional
from typing_extensions import Annotated


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserOut

    class Config:
        from_attributes = True


class PostOut(PostBase):
    Post: Post
    votes: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[int] = None


class Vote(BaseModel):
    post_id: int
    dir: Annotated[int, Field(strict=True, le=1)]
    # dir: conint(le=1)
